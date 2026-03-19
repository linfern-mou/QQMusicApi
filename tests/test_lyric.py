"""歌词模块测试."""

import pytest

from qqmusic_api import Client


@pytest.fixture
def client() -> Client:
    """创建 Client 实例."""
    return Client()


async def test_get_lyric_by_id(client: Client) -> None:
    """测试通过歌曲 ID 获取歌词."""
    result = await client.lyric.get_lyric(value=100)
    assert result is not None
    assert isinstance(result, dict)


async def test_get_lyric_by_mid(client: Client) -> None:
    """测试通过歌曲 MID 获取歌词."""
    result = await client.lyric.get_lyric(value="0025NhlN2yWrP4")
    assert result is not None
    assert isinstance(result, dict)


async def test_get_lyric_with_qrc(client: Client) -> None:
    """测试获取逐字歌词."""
    result = await client.lyric.get_lyric(value=100, qrc=True)
    assert result is not None
    assert isinstance(result, dict)


async def test_get_lyric_with_trans(client: Client) -> None:
    """测试获取带翻译的歌词."""
    result = await client.lyric.get_lyric(value=100, trans=True)
    assert result is not None
    assert isinstance(result, dict)


async def test_get_lyric_with_roma(client: Client) -> None:
    """测试获取带罗马音的歌词."""
    result = await client.lyric.get_lyric(value=100, roma=True)
    assert result is not None
    assert isinstance(result, dict)


async def test_get_lyric_with_all_options(client: Client) -> None:
    """测试获取包含所有选项的歌词."""
    result = await client.lyric.get_lyric(
        value=100,
        qrc=True,
        trans=True,
        roma=True,
    )
    assert result is not None
    assert isinstance(result, dict)


async def test_get_lyric_with_mid_and_options(client: Client) -> None:
    """测试通过 MID 获取包含选项的歌词."""
    result = await client.lyric.get_lyric(
        value="0025NhlN2yWrP4",
        qrc=False,
        trans=True,
        roma=True,
    )
    assert result is not None
    assert isinstance(result, dict)
