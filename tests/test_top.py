"""排行榜模块测试."""

from qqmusic_api import Client


async def test_get_category(client: Client) -> None:
    """测试获取所有排行榜分类."""
    result = await client.top.get_category()
    assert result is not None


async def test_get_detail(client: Client) -> None:
    """测试获取排行榜详情."""
    result = await client.top.get_detail(top_id=26)
    assert result is not None


async def test_get_detail_with_pagination(client: Client) -> None:
    """测试分页获取排行榜歌曲列表."""
    result = await client.top.get_detail(top_id=26, num=5, page=1)
    assert result is not None


async def test_get_detail_page2(client: Client) -> None:
    """测试获取排行榜歌曲列表第二页."""
    result = await client.top.get_detail(top_id=26, num=10, page=2)
    assert result is not None


async def test_get_detail_without_tag(client: Client) -> None:
    """测试获取排行榜详情时不返回标签信息."""
    result = await client.top.get_detail(top_id=26, tag=False)
    assert result is not None
