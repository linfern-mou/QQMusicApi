"""评论模块测试."""

import pytest

from qqmusic_api import Client


@pytest.fixture
def client() -> Client:
    """创建 Client 实例."""
    return Client()


async def test_get_comment_count(client: Client) -> None:
    """测试获取歌曲评论数量."""
    result = await client.comment.get_comment_count("100")
    assert result is not None


async def test_get_hot_comments(client: Client) -> None:
    """测试获取业务热评."""
    result = await client.comment.get_hot_comments("100")
    assert result is not None


async def test_get_hot_comments_with_pagination(client: Client) -> None:
    """测试分页获取业务热评."""
    result = await client.comment.get_hot_comments("100", page_num=1, page_size=10)
    assert result is not None


async def test_get_new_comments(client: Client) -> None:
    """测试获取业务最新评论."""
    result = await client.comment.get_new_comments("100")
    assert result is not None


async def test_get_new_comments_with_pagination(client: Client) -> None:
    """测试分页获取业务最新评论."""
    result = await client.comment.get_new_comments("100", page_num=1, page_size=10)
    assert result is not None


async def test_get_recommend_comments(client: Client) -> None:
    """测试获取业务推荐评论."""
    result = await client.comment.get_recommend_comments("100")
    assert result is not None


async def test_get_recommend_comments_with_pagination(client: Client) -> None:
    """测试分页获取业务推荐评论."""
    result = await client.comment.get_recommend_comments("100", page_num=1, page_size=10)
    assert result is not None
