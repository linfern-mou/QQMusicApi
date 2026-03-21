"""专辑模块测试."""

from typing import Literal

import pytest

from qqmusic_api import Client

CoverSize = Literal[150, 300, 500, 800] | None


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (None, "https://y.gtimg.cn/music/photo_new/T002R300x300M000000YX3l54F8t8T.jpg"),
        (150, "https://y.gtimg.cn/music/photo_new/T002R150x150M000000YX3l54F8t8T.jpg"),
        (300, "https://y.gtimg.cn/music/photo_new/T002R300x300M000000YX3l54F8t8T.jpg"),
        (500, "https://y.gtimg.cn/music/photo_new/T002R500x500M000000YX3l54F8t8T.jpg"),
        (800, "https://y.gtimg.cn/music/photo_new/T002R800x800M000000YX3l54F8t8T.jpg"),
    ],
)
def test_get_cover(client: Client, size: CoverSize, expected: str) -> None:
    """测试获取专辑封面链接."""
    if size is None:
        cover_url = client.album.get_cover("000YX3l54F8t8T")
    else:
        cover_url = client.album.get_cover("000YX3l54F8t8T", size=size)
    assert cover_url == expected


def test_get_cover_invalid_size(client: Client) -> None:
    """测试无效尺寸获取专辑封面时抛出异常."""
    with pytest.raises(ValueError, match="not supported size"):
        client.album.get_cover("000YX3l54F8t8T", size=200)  # type: ignore


async def test_get_detail_by_id(client: Client) -> None:
    """测试通过专辑 ID 获取专辑详情."""
    result = await client.album.get_detail(100)
    assert result is not None


@pytest.mark.parametrize(
    ("num", "page"),
    [
        (30, 1),
        (5, 1),
        (10, 2),
    ],
)
async def test_get_song(client: Client, num: int, page: int) -> None:
    """测试获取专辑歌曲列表."""
    result = await client.album.get_song(100, num=num, page=page)
    assert result is not None
