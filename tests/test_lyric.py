"""歌词模块测试."""

from qqmusic_api import Client


async def test_get_lyric_by_id(client: Client) -> None:
    """测试通过歌曲 ID 获取歌词."""
    result = await client.lyric.get_lyric(value=100)
    assert result.song_id == 100
    assert result.lyric


async def test_get_lyric_with_qrc(client: Client) -> None:
    """测试获取逐字歌词."""
    result = await client.lyric.get_lyric(value=100, qrc=True)
    assert result.lyric


async def test_get_lyric_with_trans(client: Client) -> None:
    """测试获取带翻译的歌词."""
    result = await client.lyric.get_lyric(value=100, trans=True)
    assert result.trans is not None


async def test_get_lyric_with_roma(client: Client) -> None:
    """测试获取带罗马音的歌词."""
    result = await client.lyric.get_lyric(value=100, roma=True)
    assert result.roma is not None


async def test_get_lyric_with_singing_annotations(client: Client) -> None:
    """测试获取助唱标注歌词."""
    result = await client.lyric.get_lyric(value=4835784, singing_annotations=True)
    assert result.song_id == 4835784


async def test_get_lyric_with_all_options(client: Client) -> None:
    """测试获取包含所有选项的歌词."""
    result = await client.lyric.get_lyric(
        value=4835784,
        qrc=True,
        trans=True,
        roma=True,
        singing_annotations=True,
    )
    assert result.lyric


async def test_get_singing_annotations_info(client: Client) -> None:
    """测试获取助唱标注歌词信息."""
    result = await client.lyric.get_singing_annotations_info(song_id=4835784)
    assert result.has_singing_annotations_lyric is True
