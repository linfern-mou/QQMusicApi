"""用户模块测试."""

import pytest

from qqmusic_api import Client
from qqmusic_api.core.exceptions import NotLoginError


async def test_get_euin(client: Client) -> None:
    """测试通过 musicid 获取 encrypt_uin."""
    result = await client.user.get_euin(musicid=123456789)
    assert result is not None
    assert isinstance(result, str)


async def test_get_musicid(client: Client) -> None:
    """测试通过 encrypt_uin 反查 musicid."""
    result = await client.user.get_musicid(euin="00000000000000000000000000000000")
    assert result is not None


async def test_get_homepage(client: Client) -> None:
    """测试获取用户主页头部及统计信息."""
    result = await client.user.get_homepage(euin="00000000000000000000000000000000")
    assert result is not None


async def test_get_vip_info_without_login(client: Client) -> None:
    """测试未登录时获取 VIP 信息抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.user.get_vip_info()


async def test_get_follow_singers_without_login(client: Client) -> None:
    """测试未登录时获取关注歌手列表抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.user.get_follow_singers(euin="00000000000000000000000000000000")


async def test_get_fans_without_login(client: Client) -> None:
    """测试未登录时获取粉丝列表抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.user.get_fans(euin="00000000000000000000000000000000")
