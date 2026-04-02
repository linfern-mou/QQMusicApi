"""MQTT 5.0 over WebSocket 通用客户端实现模块."""

import logging
import ssl
import threading
from collections.abc import AsyncGenerator, Callable
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING, Any

import anyio
import anyio.from_thread
import anyio.lowlevel
import anyio.to_thread
import httpx
import orjson as json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from .retry import AsyncRetrying

if TYPE_CHECKING:
    from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
    from paho.mqtt.client import MQTTMessage

logger = logging.getLogger("qqmusicapi.MQTTClient")
_MQTT_RETRY_EXCEPTIONS = (ConnectionError, TimeoutError, OSError, ssl.SSLError)


class MqttRedirectError(Exception):
    """MQTT 5.0 重定向异常.

    Attributes:
        new_address: 服务端返回的新地址(通常为 `host:port`).
        reason_code: MQTT CONNACK 原因码.
    """

    def __init__(self, new_address: str, reason_code: int = 0x9D) -> None:
        """初始化重定向异常.

        Args:
            new_address: 服务端返回的新地址.
            reason_code: CONNACK 原因码,默认 0x9D.
        """
        self.new_address = new_address
        self.reason_code = reason_code
        super().__init__(f"Server moved to {new_address}")


class PropertyId(IntEnum):
    """MQTT 5.0 属性 ID 枚举."""

    SERVER_KEEP_ALIVE = 0x13
    SERVER_REFERENCE = 0x1C
    REASON_STRING = 0x1F
    AUTH_METHOD = 0x15
    USER_PROPERTY = 0x26


class _MqttSubackError(ConnectionError):
    """SUBACK 返回失败码异常."""


@dataclass(frozen=True, slots=True)
class MqttMessage:
    """通用的 MQTT 消息对象.

    Attributes:
        topic: 消息主题.
        payload: 原始二进制载荷.
        qos: QoS 等级.
        properties: 解析后的用户属性.
    """

    topic: str
    payload: bytes
    qos: int
    properties: dict[str, str] = field(default_factory=dict)

    @property
    def json(self) -> Any | None:
        """尝试将 payload 解析为 JSON 对象.

        Returns:
            Any | None: 解析成功返回 JSON 对象,失败返回 `None`.
        """
        try:
            return json.loads(self.payload)
        except json.JSONDecodeError:
            return None


@dataclass(slots=True)
class _PendingSuback:
    """订阅确认等待记录."""

    event: threading.Event = field(default_factory=threading.Event)
    result: list[Any] | None = None
    error: Exception | None = None


@dataclass(slots=True)
class _ConnectOutcome:
    """单次连接尝试的结果."""

    event: threading.Event = field(default_factory=threading.Event)
    reason_code: int | None = None
    properties: dict[int, Any] = field(default_factory=dict)
    error: Exception | None = None


class Client:
    """通用、轻量级的 MQTT 5.0 over WebSocket 客户端.

    该实现以 `paho-mqtt` 作为底层协议客户端, 对外保留项目现有的
    `connect` / `subscribe` / `messages` 异步接口.
    """

    def __init__(
        self,
        client_id: str,
        host: str,
        port: int,
        path: str = "/mqtt",
        keep_alive: int = 45,
        session: httpx.AsyncClient | None = None,
        max_redirects: int = 3,
        heartbeat_idle_ratio: float = 0.8,
        ping_timeout: float | None = None,
        writer_queue_size: int = 0,
    ) -> None:
        """初始化客户端.

        Args:
            client_id: MQTT Client ID.
            host: WebSocket 主机名.
            port: WebSocket 端口.
            path: 握手路径.
            keep_alive: MQTT keep alive 秒数.
            session: 兼容保留参数,当前实现不会复用该 HTTP 会话.
            max_redirects: 最大重定向次数.
            heartbeat_idle_ratio: 兼容保留参数,当前实现不再使用.
            ping_timeout: 兼容保留参数,当前实现不再使用.
            writer_queue_size: 兼容保留参数,当前实现不再使用.

        Raises:
            ValueError: `heartbeat_idle_ratio` 不在合法范围时抛出.
        """
        self.client_id = client_id
        self.host = host
        self.port = port
        self.path = path
        self.keep_alive = keep_alive
        self._session = session
        self._max_redirects = max_redirects

        if not (0.0 < heartbeat_idle_ratio <= 1.0):
            raise ValueError("heartbeat_idle_ratio 必须在 (0, 1] 范围内")

        self._heartbeat_idle_ratio = heartbeat_idle_ratio
        self._ping_timeout = ping_timeout
        self._writer_queue_size = max(0, writer_queue_size)
        self._publish_queue_size = 8192

        self._close_lock = anyio.Lock()
        self._exit_stack = AsyncExitStack()

        self._publish_send_stream: MemoryObjectSendStream | None = None
        self._publish_receive_stream: MemoryObjectReceiveStream | None = None
        self._pending_subacks: dict[int, _PendingSuback] = {}

        self._epoch = 0
        self._closing = False
        self._connected = False
        self._reader_error: Exception | None = None
        self._writer_error: Exception | None = None
        self._current_connect: _ConnectOutcome | None = None
        self._current_headers: dict[str, str] | None = None
        self._event_loop_token: anyio.lowlevel.EventLoopToken | None = None

        self._mqtt_client: mqtt.Client | None = None

    async def __aenter__(self) -> "Client":
        """进入异步上下文.

        Returns:
            Client: 当前实例.
        """
        await self._exit_stack.__aenter__()
        self._event_loop_token = anyio.lowlevel.current_token()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """退出异步上下文并关闭连接.

        Args:
            exc_type: 异常类型.
            exc_val: 异常值.
            exc_tb: 异常回溯.
        """
        try:
            await self.disconnect()
        finally:
            await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    def _create_paho_client(self) -> mqtt.Client:
        """创建底层 Paho 客户端实例."""
        client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=self.client_id,
            protocol=mqtt.MQTTv5,
            transport="websockets",
        )
        # QQ 音乐二维码 MQTT 服务运行在 443 端口, 这里必须启用 TLS 才会走 wss.
        client.tls_set_context(ssl.create_default_context())
        client.enable_logger(logger)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.on_subscribe = self._on_subscribe
        client.on_disconnect = self._on_disconnect
        return client

    @staticmethod
    def _build_redirect_path(path: str, server_reference: str) -> str:
        """根据 `serverReference` 生成重定向后的握手路径.

        Args:
            path: 当前握手路径.
            server_reference: 服务端返回的新节点地址.

        Returns:
            str: 新握手路径.
        """
        parts = path.rstrip("/").split("/")
        if parts and ":" in parts[-1]:
            parts[-1] = server_reference
            return "/".join(parts)
        return f"{path.rstrip('/')}/{server_reference}"

    @staticmethod
    def _reason_code_value(reason_code: Any) -> int:
        """提取 Paho ReasonCode 的整型值."""
        if isinstance(reason_code, int):
            return reason_code
        value = getattr(reason_code, "value", None)
        if isinstance(value, int):
            return value
        try:
            return int(reason_code)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _build_paho_properties(packet_type: int, properties: dict[Any, Any] | None) -> Properties | None:
        """将现有属性字典转换为 Paho MQTT 5 Properties."""
        if not properties:
            return None

        paho_props = Properties(packet_type)
        for pid, value in properties.items():
            if pid == PropertyId.AUTH_METHOD:
                paho_props.AuthenticationMethod = value
            elif pid == PropertyId.USER_PROPERTY:
                paho_props.UserProperty = list(value)
        return paho_props

    @staticmethod
    def _decode_connack_properties(properties: Any) -> dict[int, Any]:
        """从 Paho CONNACK 属性对象提取项目关心的字段."""
        if properties is None:
            return {}

        decoded: dict[int, Any] = {}
        if (server_reference := getattr(properties, "ServerReference", None)) is not None:
            decoded[PropertyId.SERVER_REFERENCE] = server_reference
        if (server_keep_alive := getattr(properties, "ServerKeepAlive", None)) is not None:
            decoded[PropertyId.SERVER_KEEP_ALIVE] = server_keep_alive
        if (reason_string := getattr(properties, "ReasonString", None)) is not None:
            decoded[PropertyId.REASON_STRING] = reason_string
        return decoded

    @staticmethod
    def _decode_user_properties(properties: Any) -> dict[str, str]:
        """从 Paho PUBLISH 属性对象提取 UserProperty."""
        pairs = getattr(properties, "UserProperty", None)
        if not pairs:
            return {}
        return {str(key): str(value) for key, value in pairs}

    def _new_message_stream(self) -> None:
        """创建当前连接代次使用的消息流."""
        if self._publish_receive_stream:
            self._publish_receive_stream.close()
        if self._publish_send_stream:
            self._publish_send_stream.close()
        self._publish_send_stream, self._publish_receive_stream = anyio.create_memory_object_stream(
            self._publish_queue_size,
        )

    def _signal_messages_done(self, exc: Exception | None = None) -> None:
        """发送消息队列结束信号, 并尽量保证消费者可退出."""
        if exc is not None and self._reader_error is None:
            self._reader_error = exc
        if self._publish_send_stream:
            self._publish_send_stream.close()

    def _fail_pending_subacks(self, exc: Exception) -> None:
        """让所有待完成的订阅请求立即失败."""
        for record in self._pending_subacks.values():
            record.error = exc
            record.event.set()

    def _set_connect_outcome(
        self,
        *,
        reason_code: int | None = None,
        properties: dict[int, Any] | None = None,
        error: Exception | None = None,
    ) -> None:
        """设置当前连接尝试的结果."""
        if self._current_connect is None:
            return
        if reason_code is not None:
            self._current_connect.reason_code = reason_code
        if properties is not None:
            self._current_connect.properties = properties
        if error is not None:
            self._current_connect.error = error
        self._current_connect.event.set()

    def _dispatch_to_async(self, callback: Callable[..., Any], *args: Any) -> None:
        """从 Paho 线程切回当前事件循环."""
        if self._event_loop_token is None:
            return
        try:
            anyio.from_thread.run_sync(callback, *args, token=self._event_loop_token)
        except RuntimeError:
            logger.debug("Event loop already closed, dropping callback result")

    def _on_connect(self, _client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, properties: Any) -> None:
        """处理连接结果回调."""
        code = self._reason_code_value(reason_code)
        decoded_props = self._decode_connack_properties(properties)
        self._set_connect_outcome(reason_code=code, properties=decoded_props)

    def _on_message(self, _client: mqtt.Client, _userdata: Any, message: "MQTTMessage") -> None:
        """处理下行 PUBLISH 消息."""
        msg = MqttMessage(
            topic=message.topic,
            payload=bytes(message.payload),
            qos=int(message.qos),
            properties=self._decode_user_properties(getattr(message, "properties", None)),
        )
        self._dispatch_to_async(self._send_message_nowait, msg)

    def _send_message_nowait(self, msg: MqttMessage) -> None:
        """将消息写入异步缓冲队列."""
        if not self._publish_send_stream:
            return
        try:
            self._publish_send_stream.send_nowait(msg)
        except anyio.WouldBlock:
            logger.debug("Publish queue is full, dropping incoming message to prevent OOM", exc_info=True)
        except anyio.ClosedResourceError:
            logger.debug("Publish stream is already closed")

    def _on_subscribe(
        self,
        _client: mqtt.Client,
        _userdata: Any,
        mid: int,
        reason_code_list: list[Any],
        _properties: Any,
    ) -> None:
        """处理订阅确认回调."""
        record = self._pending_subacks.get(mid)
        if record is None:
            return
        record.result = list(reason_code_list)
        record.event.set()

    def _on_disconnect(
        self,
        _client: mqtt.Client,
        _userdata: Any,
        flags: Any,
        reason_code: Any,
        properties: Any,
    ) -> None:
        """处理非预期断开连接回调."""
        code = self._reason_code_value(reason_code)
        from_server = bool(getattr(flags, "is_disconnect_packet_from_server", False))
        if self._closing or (code == 0 and from_server):
            return
        reason = getattr(properties, "ReasonString", None)
        message = f"MQTT disconnected unexpectedly. reason_code={hex(code)}, from_server={from_server}"
        if isinstance(reason, str) and reason:
            message = f"{message}, reason={reason}"
        err = ConnectionError(message)
        logger.debug(
            "MQTT unexpected disconnect. reason_code=%s, from_server=%s, reason=%s",
            hex(code),
            from_server,
            reason,
        )
        self._reader_error = err
        self._writer_error = err
        self._fail_pending_subacks(err)
        self._dispatch_to_async(self._signal_messages_done, err)

    async def _wait_threading_event(self, event: threading.Event, wait_seconds: float) -> bool:
        """异步等待 threading.Event."""
        return await anyio.to_thread.run_sync(event.wait, wait_seconds)

    async def _connect_candidate(
        self,
        *,
        current_path: str,
        headers: dict[str, str] | None,
        connect_props: Properties | None,
        connect_timeout: float,
    ) -> tuple[mqtt.Client, int, dict[int, Any]]:
        """执行单次 MQTT 连接尝试并返回连接结果."""
        connect_outcome = _ConnectOutcome()
        self._current_connect = connect_outcome
        candidate = self._create_paho_client()
        candidate.ws_set_options(path=current_path, headers=headers)

        try:
            candidate.connect(
                self.host,
                self.port,
                self.keep_alive,
                clean_start=True,
                properties=connect_props,
            )
        except Exception as exc:
            self._current_connect = None
            raise ConnectionError(f"MQTT connection failed: {exc}") from exc

        candidate.loop_start()
        connected = await self._wait_threading_event(connect_outcome.event, connect_timeout)
        if not connected:
            await self._stop_paho_client(candidate, should_disconnect=True)
            self._current_connect = None
            raise TimeoutError("MQTT connect timed out")

        if connect_outcome.error is not None:
            await self._stop_paho_client(candidate, should_disconnect=True)
            self._current_connect = None
            raise ConnectionError(f"MQTT connection failed: {connect_outcome.error}") from connect_outcome.error

        reason_code = connect_outcome.reason_code
        if reason_code is None:
            await self._stop_paho_client(candidate, should_disconnect=True)
            self._current_connect = None
            raise ConnectionError("MQTT connect finished without CONNACK")

        return candidate, reason_code, connect_outcome.properties

    async def connect(self, properties: dict[Any, Any] | None = None, headers: dict[str, str] | None = None) -> None:
        """建立 WebSocket 连接并发送 MQTT CONNECT 报文.

        Args:
            properties: CONNECT 属性.
            headers: WebSocket 握手请求头.

        Raises:
            ConnectionError: 握手或协议校验失败.
            MqttRedirectError: 超过最大重定向次数.
        """
        await self.disconnect_ws_only(notify_messages=False)

        redirect_count = 0
        connect_timeout = max(float(self.keep_alive), 5.0)
        current_path = self.path
        self._current_headers = headers
        connect_props = self._build_paho_properties(PacketTypes.CONNECT, properties)

        retrying = AsyncRetrying(
            max_attempts=3,
            retry_exceptions=_MQTT_RETRY_EXCEPTIONS,
            wait_multiplier=0.5,
            wait_exp_base=2.0,
            log=logger,
        )

        while True:
            logger.debug("Connecting to wss://%s:%s%s...", self.host, self.port, current_path)
            try:
                candidate, reason_code, connack_properties = await retrying(
                    self._connect_candidate,
                    current_path=current_path,
                    headers=headers,
                    connect_props=connect_props,
                    connect_timeout=connect_timeout,
                )
            except _MQTT_RETRY_EXCEPTIONS as exc:
                self._current_connect = None
                if isinstance(exc, ConnectionError):
                    raise
                raise ConnectionError(f"MQTT connection failed: {exc}") from exc
            if reason_code == 0x00:
                if isinstance(connack_properties.get(PropertyId.SERVER_KEEP_ALIVE), int):
                    self.keep_alive = connack_properties[PropertyId.SERVER_KEEP_ALIVE]
                self.path = current_path
                self._mqtt_client = candidate
                self._connected = True
                self._reader_error = None
                self._writer_error = None
                self._closing = False
                self._epoch += 1
                self._new_message_stream()
                self._current_connect = None
                logger.debug("Connected.")
                return

            new_server = connack_properties.get(PropertyId.SERVER_REFERENCE)
            if reason_code in {0x9C, 0x9D} and isinstance(new_server, str) and new_server:
                await self._stop_paho_client(candidate, should_disconnect=True)
                if redirect_count >= self._max_redirects:
                    self._current_connect = None
                    raise MqttRedirectError(new_server, reason_code=reason_code)
                redirect_count += 1
                current_path = self._build_redirect_path(current_path, new_server)
                logger.debug("Received redirect reason code: %s, follow to %s", hex(reason_code), new_server)
                continue

            await self._stop_paho_client(candidate, should_disconnect=True)
            self._current_connect = None
            raise ConnectionError(f"MQTT Connect Failed. Reason Code: {hex(reason_code)}")

    async def subscribe(self, topic: str, properties: dict[Any, Any] | None = None) -> None:
        """发送 SUBSCRIBE 报文并等待匹配的 SUBACK.

        Args:
            topic: 订阅主题.
            properties: SUBSCRIBE 属性.

        Raises:
            ConnectionError: 连接状态异常或订阅失败.
            _MqttSubackError: SUBACK 返回失败码.
        """
        if not self._connected or self._mqtt_client is None:
            raise ConnectionError("MQTT is not connected")

        suback = _PendingSuback()
        subscribe_props = self._build_paho_properties(PacketTypes.SUBSCRIBE, properties)
        result, packet_id = self._mqtt_client.subscribe(topic, qos=0, options=None, properties=subscribe_props)
        if result != mqtt.MQTT_ERR_SUCCESS:
            raise ConnectionError(f"MQTT subscribe failed to start: rc={result}")
        if packet_id is None:
            raise ConnectionError("MQTT subscribe did not return packet id")

        self._pending_subacks[packet_id] = suback
        try:
            subscribed = await self._wait_threading_event(suback.event, max(float(self.keep_alive), 5.0))
            if not subscribed:
                err = TimeoutError(f"Subscribe to {topic} timed out")
                suback.error = err
                raise err
        finally:
            self._pending_subacks.pop(packet_id, None)

        if suback.error is not None:
            raise suback.error

        reason_codes = suback.result or []
        if any(self._reason_code_value(code) >= 0x80 for code in reason_codes):
            raise _MqttSubackError(
                f"SUBACK rejected. Reason codes: {[hex(self._reason_code_value(code)) for code in reason_codes]}",
            )

    async def _stop_paho_client(self, client: mqtt.Client | None, *, should_disconnect: bool) -> None:
        """停止底层 Paho 网络循环."""
        if client is None:
            return

        def _stop() -> None:
            if should_disconnect:
                try:
                    client.disconnect()
                except Exception:
                    logger.debug("Ignore disconnect error while stopping client", exc_info=True)
            client.loop_stop()

        await anyio.to_thread.run_sync(_stop)

    async def disconnect_ws_only(
        self,
        *,
        notify_messages: bool = True,
    ) -> None:
        """终止当前 MQTT 连接.

        该方法保留原兼容接口名, 但当前实现会停止底层 MQTT 连接与网络循环,
        并通知 `messages()` 消费者退出, 不再暴露精确的 WebSocket 生命周期控制.

        Args:
            notify_messages: 是否向 `messages()` 广播结束信号.
        """
        async with self._close_lock:
            client = self._mqtt_client
            self._mqtt_client = None
            self._closing = True
            self._connected = False
            self._current_connect = None

            if client is not None:
                await self._stop_paho_client(client, should_disconnect=True)

            self._fail_pending_subacks(ConnectionError("WebSocket closed"))
            self._pending_subacks.clear()
            self._epoch += 1

            if self._publish_receive_stream:
                self._publish_receive_stream.close()
            if self._publish_send_stream:
                self._publish_send_stream.close()

            self._publish_receive_stream = None
            self._publish_send_stream = None
            self._closing = False

            if notify_messages:
                self._signal_messages_done(None)

    async def disconnect(self) -> None:
        """断开连接并释放所有资源."""
        await self.disconnect_ws_only(notify_messages=True)
        logger.debug("Disconnected.")

    async def messages(self) -> AsyncGenerator[MqttMessage, None]:
        """获取消息监听迭代器.

        Yields:
            MqttMessage: 服务端推送的 MQTT 消息.

        Raises:
            ConnectionError: 读取或写入链路出现网络错误.
        """
        if not self._publish_receive_stream:
            return

        try:
            async for msg in self._publish_receive_stream:
                yield msg
        except anyio.ClosedResourceError:
            pass

        err = self._reader_error or self._writer_error
        if err is not None:
            raise err
