"""评论模块测试."""

import pytest

from qqmusic_api import Client


async def test_get_comment_count(client: Client) -> None:
    """测试获取歌曲评论数量."""
    result = await client.comment.get_comment_count("100")
    assert result is not None


@pytest.mark.parametrize(
    ("method_name", "page_num", "page_size"),
    [
        ("get_hot_comments", 0, 15),
        ("get_hot_comments", 1, 10),
        ("get_new_comments", 0, 15),
        ("get_new_comments", 1, 10),
        ("get_recommend_comments", 0, 15),
        ("get_recommend_comments", 1, 10),
    ],
)
async def test_get_comments(client: Client, method_name: str, page_num: int, page_size: int) -> None:
    """测试获取评论列表接口."""
    method = getattr(client.comment, method_name)
    if page_num == 0 and page_size == 15:
        result = await method("100")
    else:
        result = await method("100", page_num=page_num, page_size=page_size)
    assert result is not None
