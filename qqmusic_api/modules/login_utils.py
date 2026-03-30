"""二维码登录流程工具入口."""

from collections.abc import AsyncGenerator
from dataclasses import dataclass

import anyio
import httpx

from ..models.login import QR, QRCodeLoginEvents, QRLoginResult, QRLoginStream, QRLoginType


@dataclass(frozen=True)
class PollInterval:
    """二维码登录轮询间隔控制策略 (单位: 秒)."""

    default: float = 1.5
    scanned: float | None = None
    error: float | None = None

    @property
    def scanned_interval(self) -> float:
        """获取已扫码状态下的轮询间隔 (计算值)."""
        return self.scanned if self.scanned is not None else self.default / 2

    @property
    def error_interval(self) -> float:
        """获取异常退避、网络错误时的最大退避间隔."""
        return self.error if self.error is not None else self.default * 2


async def iter_qrcode_login(
    api,
    qrcode: QR,
    *,
    interval: float | PollInterval = 1.5,
    timeout_seconds: float = 180.0,
    emit_repeat: bool = False,
) -> QRLoginStream:
    """统一产出二维码登录事件流.

    根据传入的二维码类型 (QQ/WX/Mobile), 自动路由到对应的轮询或流处理生成器.
    使用物理截止时间 (deadline) 管理超时, 确保各协程任务局部性.

    Args:
        api: 用于发起登录请求的 LoginApi 实例.
        qrcode: 待监听的二维码对象.
        interval: 轮询间隔设置. 可传入 float 或内部轮询配置对象进行精细控制.
        timeout_seconds: 整个登录流程的最大超时时间.
        emit_repeat: 是否产出重复的状态变更事件.

    Yields:
        QRLoginResult: 包含当前登录状态和凭证 (仅在 DONE 时包含) 的结果对象.

    Raises:
        ValueError: timeout_seconds 小于等于 0.
    """
    terminal_events = {
        QRCodeLoginEvents.DONE,
        QRCodeLoginEvents.REFUSE,
        QRCodeLoginEvents.TIMEOUT,
        QRCodeLoginEvents.OTHER,
    }
    interval_config = PollInterval(float(interval)) if isinstance(interval, int | float) else interval

    async def sleep_before_deadline(deadline: float, delay: float) -> bool:
        timeout_left = deadline - anyio.current_time()
        if timeout_left <= 0:
            return False
        try:
            with anyio.fail_after(timeout_left):
                await anyio.sleep(delay)
        except TimeoutError:
            return False
        return True

    async def iter_distinct_qrcode_events(event_iter: AsyncGenerator[QRLoginResult, None]) -> QRLoginStream:
        last_event: QRCodeLoginEvents | None = None

        async for event_item in event_iter:
            if not emit_repeat and event_item.event == last_event:
                continue
            last_event = event_item.event
            yield event_item

    async def iter_web_qrcode_login(deadline: float) -> QRLoginStream:
        min_safe_interval = 1.0
        error_retries = 0

        while True:
            loop_start = anyio.current_time()
            timeout_left = deadline - loop_start
            if timeout_left <= 0:
                yield QRLoginResult(event=QRCodeLoginEvents.TIMEOUT)
                return

            try:
                with anyio.fail_after(timeout_left):
                    item = await api.check_qrcode(qrcode)
                error_retries = 0
            except (TimeoutError, anyio.EndOfStream):
                yield QRLoginResult(event=QRCodeLoginEvents.TIMEOUT)
                return
            except httpx.RequestError:
                backoff = min(interval_config.error_interval, (2**error_retries) * interval_config.default)
                if not await sleep_before_deadline(deadline, backoff):
                    yield QRLoginResult(event=QRCodeLoginEvents.TIMEOUT)
                    return
                error_retries += 1
                continue

            yield item
            if item.event in terminal_events:
                return

            sleep_time = interval_config.default
            if item.event == QRCodeLoginEvents.CONF:
                sleep_time = interval_config.scanned_interval
            elif qrcode.qr_type == QRLoginType.WX and item.event == QRCodeLoginEvents.SCAN:
                sleep_time = 0.5

            elapsed = anyio.current_time() - loop_start
            if not await sleep_before_deadline(deadline, max(sleep_time, min_safe_interval - elapsed)):
                yield QRLoginResult(event=QRCodeLoginEvents.TIMEOUT)
                return

    async def iter_mobile_qrcode_login(deadline: float) -> QRLoginStream:
        timeout_left = deadline - anyio.current_time()
        if timeout_left <= 0:
            yield QRLoginResult(event=QRCodeLoginEvents.TIMEOUT)
            return

        try:
            with anyio.fail_after(timeout_left):
                async for event_item in api.checking_mobile_qrcode(qrcode):
                    yield event_item
                    if event_item.event in terminal_events:
                        return
        except TimeoutError:
            yield QRLoginResult(event=QRCodeLoginEvents.TIMEOUT)

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds 必须大于 0")

    deadline = anyio.current_time() + timeout_seconds
    event_iter = (
        iter_mobile_qrcode_login(deadline) if qrcode.qr_type == QRLoginType.MOBILE else iter_web_qrcode_login(deadline)
    )

    async for event_item in iter_distinct_qrcode_events(event_iter):
        yield event_item
