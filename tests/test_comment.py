"""评论模块测试."""

import pytest

from qqmusic_api import Client


async def test_get_comment_count(client: Client) -> None:
    """测试获取歌曲评论数量模型."""
    result = await client.comment.get_comment_count(102065756)
    assert result.count > 0
    assert result.biz_id == "102065756"


@pytest.mark.parametrize(
    ("method_name", "page_num", "page_size"),
    [
        ("get_hot_comments", 1, 15),
        ("get_hot_comments", 2, 10),
        ("get_new_comments", 1, 15),
        ("get_new_comments", 2, 10),
        ("get_recommend_comments", 1, 15),
        ("get_recommend_comments", 2, 10),
    ],
)
async def test_get_comments(client: Client, method_name: str, page_num: int, page_size: int) -> None:
    """测试获取评论列表接口模型."""
    method = getattr(client.comment, method_name)
    result = await method(102065756, page_num=page_num, page_size=page_size)
    assert result.comments
    assert result.comments[0].cmid


async def test_get_moment_comments(client: Client) -> None:
    """测试获取时刻评论接口模型."""
    result = await client.comment.get_moment_comments(102065756, page_size=10)
    assert result.comments
    assert result.next_pos


async def test_get_hot_comments_paginate(client: Client) -> None:
    """测试热评列表支持手动逐页拉取."""
    pager = client.comment.get_hot_comments(102065756, page_num=1, page_size=5).paginate(limit=2)

    assert pager.has_more() is True
    first_page = await pager.next()
    assert pager.has_more() is True
    second_page = await pager.next()

    assert first_page.comments
    assert second_page.comments
    assert pager.has_more() is False
    with pytest.raises(StopAsyncIteration):
        await pager.next()


async def test_get_moment_comments_paginate(client: Client) -> None:
    """测试时刻评论游标分页能力."""
    pager = client.comment.get_moment_comments(102065756, page_size=5).paginate(limit=2)
    pages = [page async for page in pager]

    assert len(pages) == 2
    assert pages[0].comments
    assert pages[1].comments
    assert pages[0].next_pos != pages[1].next_pos
