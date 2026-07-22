"""歌词 Web 路由契约."""

from qqmusic_api.models.lyric import (
    BatchGetMultiStyleTransLyricResponse,
    GetAIDictResponse,
    GetLyricResponse,
    GetSingingAnnotationsInfoResponse,
    IsAIDictExistsResponse,
)

from ..routing.route_types import PUBLIC_300, WebRoute
from ._helpers import LYRIC_OPTIONS, SONG_ID, VALUE, R

ROUTES: tuple[WebRoute, ...] = (
    R("lyric", "get_lyric", "/song/{value}/lyric", GetLyricResponse, params=(*VALUE, *LYRIC_OPTIONS), cache=PUBLIC_300),
    R(
        "lyric",
        "get_multi_style_trans_lyric",
        "/song/{songid}/lyric/multi_style_trans",
        BatchGetMultiStyleTransLyricResponse,
        params=SONG_ID,
        cache=PUBLIC_300,
    ),
    R(
        "lyric",
        "get_singing_annotations_info",
        "/song/{songid}/lyric/annotations_info",
        GetSingingAnnotationsInfoResponse,
        params=SONG_ID,
        cache=PUBLIC_300,
    ),
    R(
        "lyric",
        "is_ai_dict_exists",
        "/song/{songid}/lyric/ai_dict/exists",
        IsAIDictExistsResponse,
        params=SONG_ID,
        cache=PUBLIC_300,
    ),
    R(
        "lyric",
        "get_ai_dict_info",
        "/song/{songid}/lyric/ai_dict",
        GetAIDictResponse,
        params=SONG_ID,
        cache=PUBLIC_300,
    ),
)
