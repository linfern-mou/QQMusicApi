"""LyricAPI 返回模型定义."""

from pydantic import Field

from ..algorithms import qrc_decrypt
from .request import Response


class GetLyricResponse(Response):
    """获取歌词结果.

    Attributes:
        song_id: 歌曲 ID.
        crypt: 是否加密.
        lyric: 原始歌词内容.
        trans: 翻译歌词内容.
        roma: 罗马音歌词内容.
    """

    song_id: int = Field(alias="songID")
    crypt: int
    lyric: str
    trans: str = ""
    roma: str = ""

    def decrypt(self) -> "GetLyricResponse":
        """解密歌词响应内容.

        Returns:
            GetLyricResponse: 解密后的歌词响应副本.
        """
        if self.crypt != 1:
            return self

        return self.model_copy(
            update={
                "lyric": qrc_decrypt(self.lyric) if self.lyric else "",
                "trans": qrc_decrypt(self.trans) if self.trans else "",
                "roma": qrc_decrypt(self.roma) if self.roma else "",
            },
        )
