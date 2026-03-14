# 凭证（Credential）

`Credential` 用于保存 QQ 音乐登录态相关数据，并在需要登录的接口中作为凭证使用。

## 核心字段

| 字段            | 类型  | 必需 | 说明                                                         |
|-----------------|-------|:----:|--------------------------------------------------------------|
| `musicid`       | `int` |  是  | 账号标识。QQ 登录通常是 QQ 号，微信登录通常是更长的数字 ID。 |
| `musickey`      | `str` |  是  | 登录态 Key，通常以 `Q_H_L_` 或 `W_X_` 开头。                 |
| `refresh_key`   | `str` |  否  | 用于刷新登录态。                                             |
| `refresh_token` | `str` |  否  | 用于刷新登录态。                                             |
| `encrypt_uin`   | `str` |  否  | 部分接口会返回的加密账号标识。                               |

## 常见组合

| `musickey` 前缀 | `musicid` 形态 | 说明         |
|-----------------|----------------|--------------|
| `Q_H_L_`        | 6-11 位数字    | QQ 账号登录  |
| `W_X_`          | 最长可到 19 位 | 微信账号登录 |

## 注入到 Client

最常见的做法是在初始化 `Client` 时传入全局凭证：

```python
import asyncio

from qqmusic_api import Client, Credential


async def main() -> None:
    credential = Credential(musicid=123456, musickey="Q_H_L_xxx")

    async with Client(credential=credential) as client:
        result = await client.user.get_euin(credential.musicid)
        print(result)


asyncio.run(main())
```

## 单次请求覆盖

如果你不想把凭证绑定到整个 `Client`，也可以在构造请求时单独传入 `credential`。  
这只会覆盖账号态字段和 cookies，不会改变 `Client` 自身的设备、QIMEI 与平台上下文。

## 获取凭证

如果你还没有可用凭证，可以参考：

* [快速开始](start.md)
* [Client 与连接管理](client.md)
* [登录 API 文档](../api/login.md)
