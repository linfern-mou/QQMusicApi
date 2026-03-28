"""SonglistAPI 返回模型定义."""

from pydantic import Field

from .base import Song, SongList
from .request import Response


class SonglistCreator(Response):
    """歌单创建者信息.

    Attributes:
        musicid: 用户 musicid.
        nick: 昵称.
        headurl: 头像地址.
        encrypt_uin: 加密 UIN.
    """

    musicid: int
    nick: str = ""
    headurl: str = ""
    encrypt_uin: str = Field(default="")


class SonglistInfo(SongList):
    """歌单基础信息.

    Attributes:
        creator: 创建者信息.
    """

    creator: SonglistCreator


class GetSonglistDetailResponse(Response):
    """获取歌单详情结果.

    Attributes:
        code: 返回码.
        subcode: 子返回码.
        msg: 附加消息.
        info: 歌单基础信息.
        size: 当前返回的歌曲数量.
        songs: 歌曲列表.
        total: 歌曲总数.
        hasmore: 是否还有更多结果.
    """

    code: int = 0
    subcode: int = 0
    msg: str = ""
    info: SonglistInfo = Field(alias="dirinfo")
    size: int = Field(alias="songlist_size")
    songs: list[Song] = Field(alias="songlist")
    total: int = Field(alias="total_song_num")
    hasmore: int = 0
