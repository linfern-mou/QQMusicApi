"""MQTT 工具测试."""

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, cast

import anyio
import paho.mqtt.client as mqtt
import pytest

from qqmusic_api.utils.mqtt import Client, MqttMessage, PropertyId, _MqttSubackError


@dataclass
class _FakeReasonCode:
    value: int


class _FakePahoClient:
    """用于测试的 Paho 客户端桩."""

    def __init__(self, outcomes=None, subscribe_reason_codes=None) -> None:
        self.outcomes = list(outcomes or [])
        self.subscribe_reason_codes = list(subscribe_reason_codes or [0])
        self.ws_options = None
        self.connect_calls: list[dict] = []
        self.disconnect_called = False
        self.loop_started = False
        self.loop_stopped = False
        self.subscribe_calls: list[dict] = []
        self.on_connect = None
        self.on_message = None
        self.on_subscribe = None
        self.on_disconnect = None

    def enable_logger(self, _logger) -> None:
        """模拟 enable_logger."""

    def ws_set_options(self, *, path=None, headers=None) -> None:
        """记录 WebSocket 配置."""
        self.ws_options = {"path": path, "headers": headers}

    def connect(self, host, port, keepalive, *, clean_start=True, properties=None) -> None:
        """模拟建立连接并立即触发回调."""
        self.connect_calls.append(
            {
                "host": host,
                "port": port,
                "keepalive": keepalive,
                "clean_start": clean_start,
                "properties": properties,
            },
        )
        outcome = self.outcomes.pop(0)
        assert self.on_connect is not None
        self.on_connect(
            self,
            None,
            SimpleNamespace(session_present=False),
            _FakeReasonCode(outcome["reason_code"]),
            outcome["properties"],
        )

    def loop_start(self) -> None:
        """记录 loop_start 调用."""
        self.loop_started = True

    def loop_stop(self) -> None:
        """记录 loop_stop 调用."""
        self.loop_stopped = True

    def disconnect(self) -> None:
        """记录 disconnect 调用."""
        self.disconnect_called = True

    def subscribe(self, topic, qos=0, options=None, properties=None):
        """模拟订阅并立即返回 SUBACK."""
        packet_id = len(self.subscribe_calls) + 1
        self.subscribe_calls.append({"topic": topic, "qos": qos, "options": options, "properties": properties})
        return mqtt.MQTT_ERR_SUCCESS, packet_id


def test_build_redirect_path_appends_server_reference():
    """测试重定向路径会在握手路径后追加地址."""
    assert Client._build_redirect_path("/ws/handshake", "1.2.3.4:29001") == "/ws/handshake/1.2.3.4:29001"


def test_build_redirect_path_replaces_tail_server_reference():
    """测试重定向路径会替换已有的末尾地址."""
    assert Client._build_redirect_path("/ws/handshake/1.1.1.1:29001", "2.2.2.2:29001") == "/ws/handshake/2.2.2.2:29001"


@pytest.mark.anyio
async def test_messages_raises_reader_error_on_sentinel():
    """测试消息迭代器在收到结束信号时会抛出 reader 错误."""
    client = Client(client_id="cid", host="example.com", port=443)
    client._publish_send_stream, client._publish_receive_stream = anyio.create_memory_object_stream(10)
    client._reader_error = ConnectionError("boom")
    client._signal_messages_done(client._reader_error)

    with pytest.raises(ConnectionError, match="boom"):
        async for _msg in client.messages():
            pass


@pytest.mark.anyio
async def test_disconnect_increments_epoch_and_signals_messages():
    """测试断开连接会推进 epoch 并通知消息消费者退出."""
    client = Client(client_id="cid", host="example.com", port=443)
    client._publish_send_stream, client._publish_receive_stream = anyio.create_memory_object_stream(10)
    before = client._epoch
    await client.disconnect_ws_only()
    assert client._epoch == before + 1

    events: list = [m async for m in client.messages()]
    assert len(events) == 0


@pytest.mark.anyio
async def test_connect_configures_websocket_headers_and_updates_keepalive(monkeypatch):
    """测试 connect 会配置 WebSocket 并读取 Server Keep Alive."""
    fake_client = _FakePahoClient(
        outcomes=[{"reason_code": 0, "properties": SimpleNamespace(ServerKeepAlive=30, ServerReference=None)}],
    )
    client = Client(client_id="cid", host="mu.y.qq.com", port=443, path="/ws/handshake", keep_alive=45)
    fake_client.on_connect = client._on_connect
    fake_client.on_subscribe = client._on_subscribe
    fake_client.on_disconnect = client._on_disconnect
    fake_client.on_message = client._on_message

    monkeypatch.setattr(client, "_create_paho_client", lambda: fake_client)

    async with client:
        await client.connect(
            properties={
                PropertyId.AUTH_METHOD: "pass",
                PropertyId.USER_PROPERTY: [("business", "management")],
            },
            headers={"Origin": "https://y.qq.com"},
        )

    assert fake_client.ws_options == {"path": "/ws/handshake", "headers": {"Origin": "https://y.qq.com"}}
    assert client.keep_alive == 30
    connect_props = fake_client.connect_calls[0]["properties"]
    assert connect_props is not None
    assert connect_props.AuthenticationMethod == "pass"
    assert connect_props.UserProperty == [("business", "management")]


@pytest.mark.anyio
async def test_connect_follows_server_reference_redirect(monkeypatch):
    """测试 connect 遇到 Server Reference 时会按规则重连."""
    redirect_client = _FakePahoClient(
        outcomes=[{"reason_code": 0x9C, "properties": SimpleNamespace(ServerReference="1.2.3.4:29001")}],
    )
    success_client = _FakePahoClient(
        outcomes=[{"reason_code": 0, "properties": SimpleNamespace(ServerKeepAlive=None, ServerReference=None)}],
    )
    created = [redirect_client, success_client]
    client = Client(client_id="cid", host="mu.y.qq.com", port=443, path="/ws/handshake", keep_alive=45)
    for fake_client in created:
        fake_client.on_connect = client._on_connect
        fake_client.on_subscribe = client._on_subscribe
        fake_client.on_disconnect = client._on_disconnect
        fake_client.on_message = client._on_message

    monkeypatch.setattr(client, "_create_paho_client", lambda: created.pop(0))

    async with client:
        await client.connect(headers={"Origin": "https://y.qq.com"})

    assert redirect_client.disconnect_called is True
    assert success_client.ws_options == {
        "path": "/ws/handshake/1.2.3.4:29001",
        "headers": {"Origin": "https://y.qq.com"},
    }
    assert client.path == "/ws/handshake/1.2.3.4:29001"


@pytest.mark.anyio
async def test_subscribe_raises_on_failed_reason_code():
    """测试 subscribe 在 SUBACK 返回失败码时抛错."""
    fake_client = _FakePahoClient(subscribe_reason_codes=[0x87])
    client = Client(client_id="cid", host="example.com", port=443)
    fake_client.on_subscribe = client._on_subscribe
    client._mqtt_client = cast("Any", fake_client)
    client._connected = True
    original_wait = client._wait_threading_event

    async def _trigger_suback(event, wait_seconds):
        assert fake_client.on_subscribe is not None
        fake_client.on_subscribe(
            fake_client,
            None,
            1,
            [_FakeReasonCode(code) for code in fake_client.subscribe_reason_codes],
            None,
        )
        return await original_wait(event, wait_seconds)

    client._wait_threading_event = _trigger_suback  # type: ignore[method-assign]

    with pytest.raises(_MqttSubackError, match="SUBACK rejected"):
        await client.subscribe(
            "management.qrcode_login/id",
            properties={PropertyId.USER_PROPERTY: [("authorization", "tmelogin")]},
        )

    subscribe_props = fake_client.subscribe_calls[0]["properties"]
    assert subscribe_props is not None
    assert subscribe_props.UserProperty == [("authorization", "tmelogin")]


@pytest.mark.anyio
async def test_on_message_maps_user_properties_to_mqtt_message():
    """测试 on_message 会把 UserProperty 映射到 MqttMessage.properties."""
    client = Client(client_id="cid", host="example.com", port=443)
    client._publish_send_stream, client._publish_receive_stream = anyio.create_memory_object_stream(10)
    client._dispatch_to_async = lambda callback, *args: callback(*args)  # type: ignore[method-assign]

    raw_message = SimpleNamespace(
        topic="management.qrcode_login/id",
        payload=b'{"ok":true}',
        qos=0,
        properties=SimpleNamespace(UserProperty=[("type", "cookies"), ("pubsub", "unicast")]),
    )
    client._on_message(cast("Any", client._mqtt_client), None, cast("Any", raw_message))

    assert client._publish_receive_stream is not None
    async with client._publish_receive_stream:
        msg = await client._publish_receive_stream.receive()

    assert isinstance(msg, MqttMessage)
    assert msg.properties == {"type": "cookies", "pubsub": "unicast"}
    assert msg.json == {"ok": True}
