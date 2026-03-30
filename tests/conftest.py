"""pytest 配置与共享 fixtures."""

import inspect
import os
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from functools import wraps
from typing import Any, NoReturn, ParamSpec, TypeVar, cast

import anyio
import pytest
import pytest_asyncio

from qqmusic_api import Client, Credential
from qqmusic_api.core.exceptions import GlobalAuthFailedError

TEST_CREDENTIAL_ENV_PREFIX = "QQMUSIC_"


P = ParamSpec("P")
R = TypeVar("R")

RATE_LIMIT_RETRY_DELAYS: tuple[float, ...] = (2.0, 4.0, 8.0)


def _build_test_credential_from_env() -> Credential:
    """从测试环境变量构造凭证."""
    env_map = {
        "musicid": "MUSICID",
        "musickey": "MUSICKEY",
        "encrypt_uin": "ENCRYPT_UIN",
        "str_musicid": "STR_MUSICID",
        "login_type": "LOGIN_TYPE",
    }
    data = {
        field_name: value
        for field_name, env_name in env_map.items()
        if (value := os.getenv(f"{TEST_CREDENTIAL_ENV_PREFIX}{env_name}")) is not None
    }
    return Credential.model_validate(data)


def _skip_rate_limit_after_retries() -> NoReturn:
    """在指数回退重试耗尽后跳过测试."""
    pytest.skip(f"触发 API 限流, 指数回退重试 {len(RATE_LIMIT_RETRY_DELAYS)} 次后仍失败")


async def _run_async_with_rate_limit_retry(
    invoke: Callable[[], Awaitable[R]],
    delays: tuple[float, ...],
) -> R:
    """执行异步测试并在限流时按指数回退重试."""
    try:
        return await invoke()
    except GlobalAuthFailedError:
        if not delays:
            _skip_rate_limit_after_retries()
        await anyio.sleep(delays[0])
        return await _run_async_with_rate_limit_retry(invoke, delays[1:])


def _run_sync_with_rate_limit_retry(
    invoke: Callable[[], R],
    delays: tuple[float, ...],
) -> R:
    """执行同步测试并在限流时按指数回退重试."""
    try:
        return invoke()
    except GlobalAuthFailedError:
        if not delays:
            _skip_rate_limit_after_retries()
        time.sleep(delays[0])
        return _run_sync_with_rate_limit_retry(invoke, delays[1:])


def _wrap_rate_limit_retry(
    func: Callable[P, R] | Callable[P, Awaitable[R]],
) -> Callable[P, R] | Callable[P, Awaitable[R]]:
    """为测试函数注入限流后的指数回退重试逻辑."""
    if inspect.iscoroutinefunction(func):
        async_func = cast("Callable[P, Awaitable[R]]", func)

        @wraps(async_func)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return await _run_async_with_rate_limit_retry(
                lambda: async_func(*args, **kwargs),
                RATE_LIMIT_RETRY_DELAYS,
            )

        return async_wrapper

    sync_func = cast("Callable[P, R]", func)

    @wraps(sync_func)
    def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return _run_sync_with_rate_limit_retry(
            lambda: sync_func(*args, **kwargs),
            RATE_LIMIT_RETRY_DELAYS,
        )

    return sync_wrapper


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """为异步测试补标记, 并为所有测试注入限流重试逻辑."""
    for item in items:
        obj = getattr(item, "obj", None)
        if obj is None:
            continue
        if pytest_asyncio.is_async_test(item) and item.get_closest_marker("asyncio") is None:
            item.add_marker(pytest.mark.asyncio)
        cast("Any", item).obj = _wrap_rate_limit_retry(obj)


@pytest_asyncio.fixture
async def client() -> AsyncIterator[Client]:
    """创建按测试隔离的 Client 实例."""
    test_client = Client()
    try:
        yield test_client
    finally:
        await test_client.close()


@pytest_asyncio.fixture
async def authenticated_client() -> AsyncIterator[Client]:
    """创建按测试隔离的已认证 Client 实例."""
    credential = _build_test_credential_from_env()
    if not credential.musicid or not credential.musickey:
        pytest.skip("缺少登录凭证, 跳过需要登录态的测试")
    test_client = Client(credential=credential)
    try:
        yield test_client
    finally:
        await test_client.close()
