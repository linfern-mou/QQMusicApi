"""Lyric API 返回模型定义."""

from pydantic import Field, model_validator

from ..algorithms import qrc_decrypt
from .request import Response


class GetLyricResponse(Response):
    """歌词接口返回的原始歌词载荷.

    Attributes:
        song_id: 歌曲 ID.
        lyric: 原始歌词内容.
        trans: 翻译歌词内容.
        roma: 罗马音歌词内容.
    """

    song_id: int = Field(alias="songID")
    lyric: str
    trans: str = ""
    roma: str = ""

    @model_validator(mode="before")
    @classmethod
    def _decrypt_lyrics(cls, data: dict) -> dict:
        if data.get("crypt") == 1:
            if data.get("lyric"):
                data["lyric"] = qrc_decrypt(data["lyric"])
            if data.get("trans"):
                data["trans"] = qrc_decrypt(data["trans"])
            if data.get("roma"):
                data["roma"] = qrc_decrypt(data["roma"])
        return data
