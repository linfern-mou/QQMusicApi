# Pagination

`paginate()` 用于按页消费已经声明连续翻页能力的请求结果。

与一次性请求单页数据不同，分页器会在每次迭代时自动请求下一页，并返回接口原本的响应模型。

`refresh()` 则用于“换一批”接口。它不会暴露异步迭代，而是返回 `ResponseRefresher`，由调用方按需手动请求下一批。

## Pager 基本用法

下面的示例会连续获取搜索结果的前 3 页：

```python
import asyncio

from qqmusic_api import Client


async def main() -> None:
    async with Client() as client:
        pager = client.search.search_by_type("周杰伦", num=5).paginate(limit=3)
        page_number = 1

        async for page in pager:
            print(f"第 {page_number} 页")
            print(len(page.song))
            page_number += 1

asyncio.run(main())
```

## Pager 手动逐页拉取

如果你希望自行控制何时请求下一页, 可以配合 `has_more()` 与 `next()` 使用。`has_more()` 只读取分页器当前状态, 不会主动发起网络请求。

> `next()` 与 `async for` 的终止行为一致: 没有更多结果时会抛出 `StopAsyncIteration`。

```python
import asyncio

from qqmusic_api import Client


async def main() -> None:
    async with Client() as client:
        pager = client.comment.get_hot_comments(102065756, page_size=5).paginate(limit=2)

        while pager.has_more():
            page = await pager.next()
            print(len(page.comments))


asyncio.run(main())
```

在第一页尚未请求前, 只要分页器未耗尽且未达到 `limit`, `has_more()` 就会返回 `True`。当上游响应已经明确没有下一页, 或者你已经达到 `limit`, `has_more()` 会变为 `False`。

## Pager 返回值

分页器每次迭代返回的，仍然是该接口原本的响应模型。

例如：

* `client.search.search_by_type(...).paginate()` 每一页返回 `SearchByTypeResponse`
* `client.songlist.get_detail(...).paginate()` 每一页返回 `GetSonglistDetailResponse`

这意味着你不需要学习新的分页包装类型，可以直接按原接口字段读取当前页数据。

## Pager 限制页数

`limit` 只控制最多迭代多少页，不会改写单页请求参数。

```python
import asyncio

from qqmusic_api import Client


async def main() -> None:
    async with Client() as client:
        pager = client.songlist.get_detail(songlist_id=7843129912, num=10).paginate(limit=2)
        pages = [page async for page in pager]
        print(len(pages))  # 2


asyncio.run(main())
```

如果不传 `limit`，分页器会一直请求，直到接口明确表示没有下一页。

## Refresher 基本用法

“换一批”接口先通过 `refresh()` 取得控制器，再由控制器的 `first()` 获取当前批次，随后通过 `refresh()` 手动拉取下一批。

```python
import asyncio

from qqmusic_api import Client


async def main() -> None:
    async with Client() as client:
        refresher = client.song.get_related_mv(1114857).refresh()
        current_batch = await refresher.first()
        next_batch = await refresher.refresh()

        print(current_batch.mv[0].id)
        print(next_batch.mv[0].id)


asyncio.run(main())
```
