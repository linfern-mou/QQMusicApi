"""pytest 配置与共享 fixtures."""

from collections.abc import Generator
from typing import Any

import pytest

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


@pytest.fixture(scope="session")
def client() -> Client:
    """创建共享的 Client 实例."""
    return Client()


@pytest.fixture(scope="session")
def authenticated_client() -> Client:
    """创建已认证的 Client 实例 (需要环境变量或配置)."""
    return Client()
