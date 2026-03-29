"""用户模块测试."""

import pytest

from qqmusic_api import Client
from qqmusic_api.core.exceptions import NotLoginError
from qqmusic_api.models.user import (
    UserFriendListResponse,
    UserHomepageResponse,
    UserMusicGeneResponse,
    UserRelationListResponse,
    UserVipInfoResponse,
)


async def test_get_homepage(client: Client) -> None:
    """测试未传凭证时主页接口自动补占位凭证."""
    result = await client.user.get_homepage(euin="7eEFNeSlNKns")
    assert isinstance(result, UserHomepageResponse)
    assert result.base_info.encrypted_uin


async def test_get_vip_info_without_login(client: Client) -> None:
    """测试未传凭证时 VIP 接口自动补占位凭证."""
    result = await client.user.get_vip_info()
    assert isinstance(result, UserVipInfoResponse)
    assert result.userinfo is not None


async def test_get_follow_singers_without_login(client: Client) -> None:
    """测试未登录时获取关注歌手列表抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.user.get_follow_singers(euin="00000000000000000000000000000000")


async def test_get_fans_without_login(client: Client) -> None:
    """测试未登录时获取粉丝列表抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.user.get_fans(euin="00000000000000000000000000000000")


async def test_get_friend_without_login(client: Client) -> None:
    """测试未登录时获取好友列表抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.user.get_friend()


async def test_get_follow_user_without_login(client: Client) -> None:
    """测试未登录时获取关注用户列表抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.user.get_follow_user(euin="00000000000000000000000000000000")


async def test_get_music_gene(client: Client) -> None:
    """测试获取用户音乐基因模型."""
    result = await client.user.get_music_gene(euin="7eEFNeSlNKns")
    assert isinstance(result, UserMusicGeneResponse)
    assert result.user_info_card.nick_name


async def test_relation_response_models_with_login(client: Client) -> None:
    """测试关系接口返回模型类型."""
    if not client.credential.musicid or not client.credential.musickey:
        pytest.skip("缺少登录凭证, 跳过真实登录关系接口验证")

    follow_singers = await client.user.get_follow_singers(euin=client.credential.encrypt_uin)
    fans = await client.user.get_fans(euin=client.credential.encrypt_uin)
    friends = await client.user.get_friend()
    follow_users = await client.user.get_follow_user(euin=client.credential.encrypt_uin)

    assert isinstance(follow_singers, UserRelationListResponse)
    assert isinstance(fans, UserRelationListResponse)
    assert isinstance(friends, UserFriendListResponse)
    assert isinstance(follow_users, UserRelationListResponse)
