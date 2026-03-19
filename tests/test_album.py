"""专辑模块测试."""

import pytest

from qqmusic_api import Client


@pytest.fixture
def client() -> Client:
    """创建 Client 实例."""
    return Client()


def test_get_cover_default_size(client: Client) -> None:
    """测试获取专辑封面链接(默认尺寸)."""
    cover_url = client.album.get_cover("000YX3l54F8t8T")
    assert cover_url == "https://y.gtimg.cn/music/photo_new/T002R300x300M000000YX3l54F8t8T.jpg"


def test_get_cover_150(client: Client) -> None:
    """测试获取专辑封面链接(150x150)."""
    cover_url = client.album.get_cover("000YX3l54F8t8T", size=150)
    assert cover_url == "https://y.gtimg.cn/music/photo_new/T002R150x150M000000YX3l54F8t8T.jpg"


def test_get_cover_300(client: Client) -> None:
    """测试获取专辑封面链接(300x300)."""
    cover_url = client.album.get_cover("000YX3l54F8t8T", size=300)
    assert cover_url == "https://y.gtimg.cn/music/photo_new/T002R300x300M000000YX3l54F8t8T.jpg"


def test_get_cover_500(client: Client) -> None:
    """测试获取专辑封面链接(500x500)."""
    cover_url = client.album.get_cover("000YX3l54F8t8T", size=500)
    assert cover_url == "https://y.gtimg.cn/music/photo_new/T002R500x500M000000YX3l54F8t8T.jpg"


def test_get_cover_800(client: Client) -> None:
    """测试获取专辑封面链接(800x800)."""
    cover_url = client.album.get_cover("000YX3l54F8t8T", size=800)
    assert cover_url == "https://y.gtimg.cn/music/photo_new/T002R800x800M000000YX3l54F8t8T.jpg"


def test_get_cover_invalid_size(client: Client) -> None:
    """测试无效尺寸获取专辑封面时抛出异常."""
    with pytest.raises(ValueError, match="not supported size"):
        client.album.get_cover("000YX3l54F8t8T", size=200)  # type: ignore


async def test_get_detail_by_id(client: Client) -> None:
    """测试通过专辑 ID 获取专辑详情."""
    result = await client.album.get_detail(100)
    assert result is not None


async def test_get_song_by_id(client: Client) -> None:
    """测试通过专辑 ID 获取专辑歌曲列表."""
    result = await client.album.get_song(100)
    assert result is not None


async def test_get_song_with_pagination(client: Client) -> None:
    """测试分页获取专辑歌曲列表."""
    result = await client.album.get_song(100, num=5, page=1)
    assert result is not None


async def test_get_song_page2(client: Client) -> None:
    """测试获取专辑歌曲列表第二页."""
    result = await client.album.get_song(100, num=10, page=2)
    assert result is not None
