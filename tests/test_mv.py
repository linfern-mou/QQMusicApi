"""MV 模块测试."""

from qqmusic_api import Client


async def test_get_detail(client: Client) -> None:
    """测试获取 MV 详细信息."""
    result = await client.mv.get_detail(["013xscuH0xlbie"])
    assert result is not None


async def test_get_detail_multiple(client: Client) -> None:
    """测试批量获取 MV 详细信息."""
    result = await client.mv.get_detail(["013xscuH0xlbie", "013xscuH0xlbie"])
    assert result is not None


async def test_get_mv_urls(client: Client) -> None:
    """测试获取 MV 播放链接."""
    result = await client.mv.get_mv_urls(["013xscuH0xlbie"])
    assert result is not None


async def test_get_mv_urls_multiple(client: Client) -> None:
    """测试批量获取 MV 播放链接."""
    result = await client.mv.get_mv_urls(["013xscuH0xlbie", "013xscuH0xlbie"])
    assert result is not None
