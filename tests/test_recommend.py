"""推荐模块测试."""

from qqmusic_api import Client


async def test_get_home_feed(client: Client) -> None:
    """测试获取主页推荐数据."""
    result = await client.recommend.get_home_feed()
    assert result is not None
    assert isinstance(result, dict)


async def test_get_guess_recommend(client: Client) -> None:
    """测试获取猜你喜欢推荐数据."""
    result = await client.recommend.get_guess_recommend()
    assert result is not None
    assert isinstance(result, dict)


async def test_get_radar_recommend(client: Client) -> None:
    """测试获取雷达推荐数据."""
    result = await client.recommend.get_radar_recommend()
    assert result is not None
    assert isinstance(result, dict)


async def test_get_recommend_songlist(client: Client) -> None:
    """测试获取推荐歌单数据."""
    result = await client.recommend.get_recommend_songlist()
    assert result is not None
    assert isinstance(result, dict)


async def test_get_recommend_newsong(client: Client) -> None:
    """测试获取推荐新歌数据."""
    result = await client.recommend.get_recommend_newsong()
    assert result is not None
    assert isinstance(result, dict)
