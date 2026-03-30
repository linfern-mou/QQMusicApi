"""推荐模块测试."""

import pytest

from qqmusic_api import Client, LoginExpiredError
from qqmusic_api.models.recommend import (
    GuessRecommendResponse,
    RadarRecommendResponse,
    RecommendFeedCardResponse,
    RecommendNewSongResponse,
    RecommendSonglistItem,
    RecommendSonglistResponse,
)


async def test_get_home_feed(client: Client) -> None:
    """测试获取主页推荐响应模型."""
    result = await client.recommend.get_home_feed()
    assert isinstance(result, RecommendFeedCardResponse)
    assert result.shelves
    assert result.shelves[0].id > 0


async def test_get_guess_recommend(client: Client) -> None:
    """测试猜你喜欢接口登录态要求与响应模型."""
    if not client.credential.musicid or not client.credential.musickey:
        with pytest.raises(LoginExpiredError):
            await client.recommend.get_guess_recommend()
        return

    result = await client.recommend.get_guess_recommend()
    assert isinstance(result, GuessRecommendResponse)
    assert result.songs
    assert result.songs[0].mid


async def test_get_radar_recommend(client: Client) -> None:
    """测试获取雷达推荐响应模型."""
    result = await client.recommend.get_radar_recommend()
    assert isinstance(result, RadarRecommendResponse)
    assert result.songs
    assert result.songs[0].mid


async def test_get_recommend_songlist(client: Client) -> None:
    """测试获取推荐歌单响应模型."""
    result = await client.recommend.get_recommend_songlist()
    assert isinstance(result, RecommendSonglistResponse)
    assert result.songlists
    assert isinstance(result.songlists[0], RecommendSonglistItem)
    assert result.songlists[0].title


async def test_get_recommend_newsong(client: Client) -> None:
    """测试获取推荐新歌响应模型."""
    result = await client.recommend.get_recommend_newsong()
    assert isinstance(result, RecommendNewSongResponse)
    assert result.songs
    assert result.songs[0].mid
