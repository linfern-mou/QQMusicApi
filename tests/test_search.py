"""搜索模块测试."""

from qqmusic_api import Client
from qqmusic_api.modules.search import SearchType


async def test_get_hotkey(client: Client) -> None:
    """测试获取热搜词列表."""
    result = await client.search.get_hotkey()
    assert result is not None
    assert isinstance(result, dict)


async def test_complete(client: Client) -> None:
    """测试搜索词补全建议."""
    result = await client.search.complete("周杰伦")
    assert result is not None
    assert isinstance(result, dict)


async def test_quick_search(client: Client) -> None:
    """测试快速搜索."""
    result = await client.search.quick_search("周杰伦")
    assert result is not None
    assert isinstance(result, dict)


async def test_general_search(client: Client) -> None:
    """测试综合搜索."""
    result = await client.search.general_search("周杰伦")
    assert result is not None
    assert isinstance(result, dict)


async def test_general_search_with_page(client: Client) -> None:
    """测试综合搜索翻页."""
    result = await client.search.general_search("周杰伦", page=2)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_song(client: Client) -> None:
    """测试按类型搜索歌曲."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.SONG)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_singer(client: Client) -> None:
    """测试按类型搜索歌手."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.SINGER)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_album(client: Client) -> None:
    """测试按类型搜索专辑."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.ALBUM)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_songlist(client: Client) -> None:
    """测试按类型搜索歌单."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.SONGLIST)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_mv(client: Client) -> None:
    """测试按类型搜索MV."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.MV)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_lyric(client: Client) -> None:
    """测试按类型搜索歌词."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.LYRIC)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_user(client: Client) -> None:
    """测试按类型搜索用户."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.USER)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_audio_album(client: Client) -> None:
    """测试按类型搜索节目专辑."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.AUDIO_ALBUM)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_audio(client: Client) -> None:
    """测试按类型搜索节目."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.AUDIO)
    assert result is not None
    assert isinstance(result, dict)


async def test_search_by_type_with_pagination(client: Client) -> None:
    """测试按类型搜索分页."""
    result = await client.search.search_by_type("周杰伦", search_type=SearchType.SONG, page=2, num=5)
    assert result is not None
    assert isinstance(result, dict)
