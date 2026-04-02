"""重试相关工具."""

import asyncio
import logging
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from functools import wraps
from typing import ParamSpec, TypeVar

import httpx

P = ParamSpec("P")
R = TypeVar("R")

_DEFAULT_RETRY_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ReadError,
    httpx.ReadTimeout,
    httpx.RemoteProtocolError,
    httpx.WriteError,
    httpx.WriteTimeout,
)
logger = logging.getLogger(__name__)


@dataclass(slots=True)
class RetryCallState:
    """单次调用的重试状态."""

    attempt_number: int
    exception: BaseException | None = None
    sleep: float = 0.0


class AsyncRetrying:
    """异步重试执行器."""

    def __init__(
        self,
        *,
        max_attempts: int,
        retry_exceptions: tuple[type[BaseException], ...] | None = None,
        wait_multiplier: float = 0.5,
        wait_exp_base: float = 2.0,
        wait_max: float | None = None,
        wait_jitter: float = 0.0,
        log: logging.Logger | None = None,
    ) -> None:
        """初始化异步重试执行器."""
        if max_attempts <= 0:
            raise ValueError("max_attempts 必须大于 0")
        if retry_exceptions is None:
            retry_exceptions = _DEFAULT_RETRY_EXCEPTIONS
        if not retry_exceptions:
            raise ValueError("retry_exceptions 不能为空")
        for exc_type in retry_exceptions:
            if not issubclass(exc_type, BaseException):
                raise TypeError("retry_exceptions 的每个元素都必须是 BaseException 的子类")
        if wait_multiplier < 0:
            raise ValueError("wait_multiplier 不能小于 0")
        if wait_exp_base < 1:
            raise ValueError("wait_exp_base 不能小于 1")
        if wait_max is not None and wait_max < 0:
            raise ValueError("wait_max 不能小于 0")
        if not 0 <= wait_jitter <= 1:
            raise ValueError("wait_jitter 必须在 0 到 1 之间")

        self.max_attempts = max_attempts
        self.retry_exceptions = retry_exceptions
        self.wait_multiplier = wait_multiplier
        self.wait_exp_base = wait_exp_base
        self.wait_max = wait_max
        self.wait_jitter = wait_jitter
        self.log = log or logger

    def _compute_sleep(self, attempt_number: int) -> float:
        """计算当前重试前的等待时间."""
        delay = self.wait_multiplier * (self.wait_exp_base ** max(attempt_number - 1, 0))
        bounded_delay = min(delay, self.wait_max) if self.wait_max is not None else delay
        if self.wait_jitter == 0:
            return bounded_delay
        return bounded_delay * (0.5 + random.random() * self.wait_jitter)

    def _after_attempt(self, retry_state: RetryCallState) -> None:
        """在重试等待前记录日志."""
        self.log.debug(
            "网络波动, 准备进行第 %s 次重试, delay=%.3fs, error=%s",
            retry_state.attempt_number,
            retry_state.sleep,
            retry_state.exception,
        )

    async def __call__(self, fn: Callable[P, Awaitable[R]], *args: P.args, **kwargs: P.kwargs) -> R:
        """执行异步调用并按配置重试."""
        attempt_number = 1
        while True:
            try:
                return await fn(*args, **kwargs)
            except self.retry_exceptions as exc:  # noqa: PERF203
                retry_state = RetryCallState(attempt_number=attempt_number, exception=exc)
                if attempt_number >= self.max_attempts:
                    raise
                retry_state.sleep = self._compute_sleep(attempt_number)
                self._after_attempt(retry_state)
                await asyncio.sleep(retry_state.sleep)
                attempt_number += 1

    def wraps(self, fn: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """将异步函数包装为带重试能力的函数."""

        @wraps(fn)
        async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            return await self(fn, *args, **kwargs)

        return wrapped
