# Client 与连接管理

`qqmusic_api` 使用 `Client` 统一管理连接、凭证、设备信息与请求配置。

## 推荐用法

推荐使用 `async with Client()`，这样可以自动关闭底层 `httpx.AsyncClient`：

```python
import asyncio

from qqmusic_api import Client


async def main() -> None:
    async with Client() as client:
        result = await client.search.quick_search("周杰伦")
        print(result)


asyncio.run(main())
```

## 常用初始化参数

`Client` 当前常用参数包括：

* `credential`: 全局凭证。
* `device_path`: 设备信息持久化路径。
* `enable_sign`: 是否启用签名参数。
* `platform`: 请求默认平台。
* `max_concurrency`: 单个 `Client` 的最大并发请求数。
* `max_connections`: 底层连接池大小。
* `qimei_timeout`: 获取 QIMEI 的超时时间。

另外也支持透传部分 `httpx.AsyncClient` 配置，例如 `proxy`、`verify`、`transport` 等。

## 全局凭证

如果你的场景需要登录，可以在初始化 `Client` 时直接注入 `Credential`：

```python
from qqmusic_api import Client, Credential

credential = Credential(musicid=123456, musickey="Q_H_L_xxx")
client = Client(credential=credential)
```

## 设备与上下文

`Client` 会维护自己的设备信息、QIMEI 缓存和平台上下文。  
即使某次请求临时覆盖了 `credential`，这些上下文仍然属于当前 `Client` 实例本身。
