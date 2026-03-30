"""用户模块测试."""

from qqmusic_api import Client


async def test_get_homepage(client: Client) -> None:
    """测试未传凭证时主页接口自动补占位凭证."""
    result = await client.user.get_homepage(euin="7eEFNeSlNKns")
    assert result.base_info.encrypted_uin


async def test_get_music_gene(client: Client) -> None:
    """测试获取用户音乐基因模型."""
    result = await client.user.get_music_gene(euin="7eEFNeSlNKns")
    assert result.user_info_card.nick_name


async def test_relation_response_models_with_login(authenticated_client: Client) -> None:
    """测试关系接口返回可消费结果."""
    follow_singers = await authenticated_client.user.get_follow_singers(
        euin=authenticated_client.credential.encrypt_uin,
    )
    fans = await authenticated_client.user.get_fans(
        euin=authenticated_client.credential.encrypt_uin,
    )
    friends = await authenticated_client.user.get_friend()
    follow_users = await authenticated_client.user.get_follow_user(
        euin=authenticated_client.credential.encrypt_uin,
    )
    assert follow_singers.total >= 0
    assert fans.total >= 0
    assert friends.has_more in (True, False)
    assert follow_users.total >= 0
