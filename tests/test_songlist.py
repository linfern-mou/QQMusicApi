"""歌单模块测试."""

import pytest

from qqmusic_api import Client, NotLoginError


async def test_get_detail(client: Client) -> None:
    """测试获取歌单详细信息."""
    result = await client.songlist.get_detail(songlist_id=7843129912)
    assert result is not None


async def test_get_detail_with_pagination(client: Client) -> None:
    """测试分页获取歌单歌曲列表."""
    result = await client.songlist.get_detail(songlist_id=7843129912, num=5, page=1)
    assert result is not None


async def test_get_detail_page2(client: Client) -> None:
    """测试获取歌单歌曲列表第二页."""
    result = await client.songlist.get_detail(songlist_id=7843129912, num=10, page=2)
    assert result is not None


async def test_get_detail_only_song(client: Client) -> None:
    """测试仅获取歌单歌曲列表."""
    result = await client.songlist.get_detail(songlist_id=7843129912, onlysong=True)
    assert result is not None


async def test_get_detail_without_tag(client: Client) -> None:
    """测试获取歌单详情时不返回标签信息."""
    result = await client.songlist.get_detail(songlist_id=7843129912, tag=False)
    assert result is not None


async def test_get_detail_without_userinfo(client: Client) -> None:
    """测试获取歌单详情时不返回用户信息."""
    result = await client.songlist.get_detail(songlist_id=7843129912, userinfo=False)
    assert result is not None


async def test_create_without_login(client: Client) -> None:
    """测试未登录时创建歌单抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.songlist.create(dirname="测试歌单")


async def test_delete_without_login(client: Client) -> None:
    """测试未登录时删除歌单抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.songlist.delete(dirid=1)


async def test_add_songs_without_login(client: Client) -> None:
    """测试未登录时添加歌曲到歌单抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.songlist.add_songs(dirid=1, song_info=[(100, 0)])


async def test_del_songs_without_login(client: Client) -> None:
    """测试未登录时删除歌单歌曲抛出 NotLoginError."""
    with pytest.raises(NotLoginError):
        await client.songlist.del_songs(dirid=1, song_info=[(100, 0)])
