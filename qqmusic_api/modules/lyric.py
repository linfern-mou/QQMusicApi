"""歌词相关 API."""

from typing import Any

from ..models.lyric import GetLyricResponse, GetSingingAnnotationsInfoResponse
from ._base import ApiModule


class LyricApi(ApiModule):
    """歌词相关 API."""

    def get_lyric(
        self,
        value: int | str,
        song_type: int = 1,
        *,
        qrc: bool = False,
        trans: bool = False,
        roma: bool = False,
        singing_annotations: bool = False,
    ):
        """获取歌词原始数据.

        Args:
            value: 歌曲 ID 或 MID.
            qrc: 是否获取逐字歌词 (逐字歌词可能需要特定权限).
            trans: 是否获取翻译.
            roma: 是否获取罗马音.
            singing_annotations: 是否获取助唱标注歌词.
            song_type: 歌曲类型.
        """
        params: dict[str, Any] = {
            "crypt": 1,
            "lrc_t": 0,
            "qrc": int(qrc),
            "qrc_t": 0,
            "roma": int(roma),
            "roma_t": 0,
            "trans": int(trans),
            "trans_t": 0,
            "needSingingAnnotations": singing_annotations,
            "type": song_type,
        }
        params.update(self._build_query_common_params())

        if isinstance(value, int) or (isinstance(value, str) and value.isdecimal()):
            params["songId"] = int(value)
        else:
            params["songMid"] = value

        return self._build_request(
            module="music.musichallSong.PlayLyricInfo",
            method="GetPlayLyricInfo",
            param=params,
            preserve_bool=True,
            response_model=GetLyricResponse,
        )

    def get_singing_annotations_info(
        self,
        song_id: int,
    ):
        """获取助唱标注歌词信息.

        Args:
            song_id: 歌曲 ID.
        """
        return self._build_request(
            module="music.musichallSong.PlayLyricInfo",
            method="GetSingingAnnotationsInfo",
            param={
                "songID": song_id,
                "needNum": False,
            },
            preserve_bool=True,
            response_model=GetSingingAnnotationsInfoResponse,
        )
