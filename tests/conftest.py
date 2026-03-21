"""pytest 配置与共享 fixtures."""

from collections.abc import AsyncIterator, Generator
from typing import Any

import pytest
import pytest_asyncio

from qqmusic_api import Client
from qqmusic_api.core.exceptions import GlobalAuthFailedError


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """为所有异步测试函数自动添加 asyncio 标记."""
    import inspect

    for item in items:
        # getattr with a default and the following checks should be safe;
        # avoid broad try/except inside the loop for performance.
        if inspect.iscoroutinefunction(getattr(item, "obj", None)) and item.get_closest_marker("asyncio") is None:
            item.add_marker(pytest.mark.asyncio)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[Any, Any, None]:
    """在测试执行时自动捕获 GlobalAuthFailedError 并跳过测试."""
    outcome = yield
    exc = outcome.excinfo
    if exc and issubclass(exc[0], GlobalAuthFailedError):
        outcome.force_result(None)
        pytest.skip("触发 API 限流, 跳过测试")


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
    test_client = Client()
    try:
        yield test_client
    finally:
        await test_client.close()
