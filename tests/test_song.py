"""歌曲模块测试."""

import pytest

from qqmusic_api import Client


@pytest.fixture
def client() -> Client:
    """创建 Client 实例."""
    return Client()


async def test_query_song_by_id(client: Client) -> None:
    """测试通过歌曲 ID 查询歌曲信息."""
    result = await client.song.query_song([100])
    assert result is not None


async def test_query_song_by_mid(client: Client) -> None:
    """测试通过歌曲 MID 查询歌曲信息."""
    result = await client.song.query_song(["003w2xz20QlUZt"])
    assert result is not None


async def test_query_song_empty_value(client: Client) -> None:
    """测试空列表查询歌曲时抛出异常."""
    with pytest.raises(ValueError, match="value 不能为空"):
        await client.song.query_song([])


async def test_get_try_url(client: Client) -> None:
    """测试获取试听文件链接."""
    result = await client.song.get_try_url(mid="003w2xz20QlUZt", vs="003w2xz20QlUZt")
    assert result is not None


async def test_get_song_urls_mp3(client: Client) -> None:
    """测试获取歌曲 MP3 文件链接."""
    from qqmusic_api.modules.song import SongFileType

    result = await client.song.get_song_urls(
        mid=["003w2xz20QlUZt"],
        file_type=SongFileType.MP3_128,
    )
    assert isinstance(result, dict)


async def test_get_song_urls_flac(client: Client) -> None:
    """测试获取歌曲 FLAC 文件链接."""
    from qqmusic_api.modules.song import SongFileType

    result = await client.song.get_song_urls(
        mid=["003w2xz20QlUZt"],
        file_type=SongFileType.FLAC,
    )
    assert isinstance(result, dict)


async def test_get_song_urls_encrypted(client: Client) -> None:
    """测试获取加密歌曲文件链接."""
    from qqmusic_api.modules.song import EncryptedSongFileType

    result = await client.song.get_song_urls(
        mid=["003w2xz20QlUZt"],
        file_type=EncryptedSongFileType.FLAC,
    )
    assert isinstance(result, dict)


async def test_get_song_urls_empty(client: Client) -> None:
    """测试空列表获取歌曲链接返回空字典."""
    result = await client.song.get_song_urls(mid=[])
    assert result == {}


async def test_get_detail_by_id(client: Client) -> None:
    """测试通过歌曲 ID 获取歌曲详情."""
    result = await client.song.get_detail(100)
    assert result is not None


async def test_get_detail_by_mid(client: Client) -> None:
    """测试通过歌曲 MID 获取歌曲详情."""
    result = await client.song.get_detail("003w2xz20QlUZt")
    assert result is not None


async def test_get_similar_song(client: Client) -> None:
    """测试获取相似歌曲."""
    result = await client.song.get_similar_song(100)
    assert result is not None


async def test_get_lables(client: Client) -> None:
    """测试获取歌曲标签."""
    result = await client.song.get_lables(100)
    assert result is not None


async def test_get_related_songlist(client: Client) -> None:
    """测试获取歌曲相关歌单."""
    result = await client.song.get_related_songlist(100)
    assert result is not None


async def test_get_related_mv(client: Client) -> None:
    """测试获取歌曲相关 MV."""
    result = await client.song.get_related_mv(100)
    assert result is not None


async def test_get_other_version_by_id(client: Client) -> None:
    """测试通过歌曲 ID 获取其他版本."""
    result = await client.song.get_other_version(100)
    assert result is not None


async def test_get_other_version_by_mid(client: Client) -> None:
    """测试通过歌曲 MID 获取其他版本."""
    result = await client.song.get_other_version("003w2xz20QlUZt")
    assert result is not None


async def test_get_producer_by_id(client: Client) -> None:
    """测试通过歌曲 ID 获取制作人信息."""
    result = await client.song.get_producer(100)
    assert result is not None


async def test_get_producer_by_mid(client: Client) -> None:
    """测试通过歌曲 MID 获取制作人信息."""
    result = await client.song.get_producer("003w2xz20QlUZt")
    assert result is not None


async def test_get_sheet(client: Client) -> None:
    """测试获取歌曲相关曲谱."""
    result = await client.song.get_sheet("003w2xz20QlUZt")
    assert result is not None


async def test_get_fav_num(client: Client) -> None:
    """测试获取歌曲收藏数量."""
    result = await client.song.get_fav_num([100])
    assert result is not None
