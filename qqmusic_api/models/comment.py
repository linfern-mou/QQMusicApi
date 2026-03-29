"""CommentAPI 返回模型定义."""

from typing import Any

from pydantic import Field

from .request import Response


class IconTextInfo(Response):
    """评论计数角标信息."""

    txt: str = ""
    unique_id: str = ""
    type: int = 0
    cmid: str | None = None
    is_dynamic: bool = False


class CommentCountResponse(Response):
    """评论数量响应."""

    biz_type: int = Field(default=0, json_schema_extra={"jsonpath": "$.response.biz_type"})
    biz_id: str = Field(default="", json_schema_extra={"jsonpath": "$.response.biz_id"})
    biz_sub_type: int = Field(default=0, json_schema_extra={"jsonpath": "$.response.biz_sub_type"})
    count: int = Field(default=0, json_schema_extra={"jsonpath": "$.response.count"})
    count_ver: str = Field(default="", json_schema_extra={"jsonpath": "$.response.count_ver"})
    count_view: str = Field(default="", json_schema_extra={"jsonpath": "$.response.count_view"})
    related_id: str = Field(default="", json_schema_extra={"jsonpath": "$.response.related_id"})
    tip: str = Field(default="", json_schema_extra={"jsonpath": "$.response.tip"})
    icon_list: list[IconTextInfo] | None = Field(
        default=None,
        json_schema_extra={"jsonpath": "$.response.icon_list[*]"},
    )
    cm_tab_type: int = Field(default=0, json_schema_extra={"jsonpath": "$.cmTabType"})


class CommentItem(Response):
    """评论条目."""

    cmid: str = Field(default="", alias="CmId")
    seq_no: str = Field(default="", alias="SeqNo")
    nick: str = Field(default="", alias="Nick")
    avatar: str = Field(default="", alias="Avatar")
    encrypt_uin: str = Field(default="", alias="EncryptUin")
    content: str = Field(default="", alias="Content")
    pub_time: int = Field(default=0, alias="PubTime")
    praise_num: int = Field(default=0, alias="PraiseNum")
    reply_cnt: int = Field(default=0, alias="ReplyCnt")
    is_praised: int = Field(default=0, alias="IsPraised")
    is_self: int = Field(default=0, alias="IsSelf")
    state: int = Field(default=0, alias="State")
    hot_score: str = Field(default="", alias="HotScore")
    rec_score: str = Field(default="", alias="RecScore")
    song_id: int = Field(default=0, alias="SongId")
    song_name: str = Field(default="", alias="SongName")
    singer_names: str = Field(default="", alias="SingerNames")
    song_ts_elems: list[dict[str, Any]] | None = Field(default=None, alias="SongTsElems")
    hash_tag_list: list[dict[str, Any]] | None = Field(default=None, alias="HashTagList")
    little_tails: list[dict[str, Any]] | None = Field(default=None, alias="LittleTails")
    icon_list: list[dict[str, Any]] | None = Field(default=None, alias="IconList")
    vip_ui: dict[str, Any] | None = Field(default=None, alias="VipUI")
    sub_comments: list[dict[str, Any]] | None = Field(default=None, alias="SubComments")


class CommentListResponse(Response):
    """评论列表响应."""

    comments: list[CommentItem] | None = Field(
        default=None,
        json_schema_extra={"jsonpath": "$.CommentList.Comments[*]"},
    )
    comment_ids: list[str] | None = Field(default=None, json_schema_extra={"jsonpath": "$.CommentList.CommentIds[*]"})
    has_more: int = Field(default=0, json_schema_extra={"jsonpath": "$.CommentList.HasMore"})
    next_offset: int = Field(default=0, json_schema_extra={"jsonpath": "$.CommentList.NextOffset"})
    total: int = Field(default=0, json_schema_extra={"jsonpath": "$.CommentList.Total"})
    total_cm_num: int = Field(default=0, alias="TotalCmNum")
    comment_tip: str = Field(default="", alias="CommentTip")
    comment_h5_page: str = Field(default="", alias="CommentH5Page")
    has_ts_cm: int = Field(default=0, alias="HasTsCm")
    share_cnt: int = Field(default=0, alias="ShareCnt")
    msg: str = Field(default="", alias="Msg")
    sub_code: int = Field(default=0, alias="SubCode")


class MomentCommentItem(Response):
    """时刻评论条目."""

    cmid: str = Field(default="", alias="CmId")
    seq_no: str = Field(default="", alias="SeqNo")
    content: str = Field(default="", alias="Content")
    encrypt_uin: str = Field(default="", alias="EncryptUin")
    pub_time: int = Field(default=0, alias="PubTime")
    praise_num: int = Field(default=0, alias="PraiseNum")
    reply_cnt: int = Field(default=0, alias="ReplyCnt")
    state: int = Field(default=0, alias="State")
    is_self: int = Field(default=0, alias="IsSelf")
    location: str = Field(default="", alias="Location")
    phone_type: str = Field(default="", alias="PhoneType")
    pic: str = Field(default="", alias="Pic")
    pic_size: str = Field(default="", alias="PicSize")
    song_ts_elems: list[dict[str, Any]] | None = Field(default=None, alias="SongTsElems")
    hash_tag_list: list[dict[str, Any]] | None = Field(default=None, alias="HashTagList")
    little_tails: list[dict[str, Any]] | None = Field(default=None, alias="LittleTails")


class MomentCommentResponse(Response):
    """时刻评论列表响应."""

    comments: list[MomentCommentItem] | None = Field(default=None, json_schema_extra={"jsonpath": "$.CmList[*]"})
    has_more: int = Field(default=0, alias="HasMore")
    next_pos: str | None = Field(default=None, alias="NextPos")
    hint: str = Field(default="", alias="Hint")
    prev_list_loaded: int = Field(default=0, alias="PrevListLoaded")
    map_cm_ext: dict[str, dict[str, Any]] | None = Field(default=None, alias="MapCmExt")
