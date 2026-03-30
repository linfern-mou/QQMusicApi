"""UserAPI 返回模型定义."""

from typing import Any

from pydantic import AliasChoices, Field

from .base import MV, Album, Singer, SongList
from .request import Response


class UserPlaylistSummary(SongList):
    """用户歌单摘要."""

    id: int = Field(default=-1, alias="tid")
    dirid: int = Field(default=0, alias="dirId")
    title: str = Field(default="", validation_alias=AliasChoices("dirName", "name", "title"))
    picurl: str = Field(default="", validation_alias=AliasChoices("picUrl", "logo", "picurl"))
    songnum: int = Field(default=0, validation_alias=AliasChoices("songNum", "songnum"))
    create_time: int = Field(default=0, alias="createTime")
    update_time: int = Field(default=0, alias="updateTime")
    uin: str = ""
    nick: str = ""
    desc: str = ""
    bigpic_url: str = Field(default="", alias="bigpicUrl")
    album_pic_url: str = Field(default="", alias="albumPicUrl")
    avatar: str = ""
    ident_icon: str = Field(default="", alias="identIcon")
    layer_url: str = Field(default="", alias="layerUrl")
    invalid: bool = False
    dir_show: int = Field(default=0, alias="dirShow")
    create_fav_cnt: int = Field(default=0, alias="fav_cnt")
    play_cnt: int = 0
    comment_cnt: int = 0
    op_type: int = Field(default=0, alias="opType")
    sort_weight: int = Field(default=0, alias="sortWeight")


class UserCreatedSonglistResponse(Response):
    """用户创建歌单列表响应."""

    total: int = 0
    playlists: list[UserPlaylistSummary] | None = Field(default=None, json_schema_extra={"jsonpath": "$.v_playlist[*]"})
    deleted_ids: list[int] | int | None = Field(default=None, alias="v_delTid")
    finished: bool = Field(default=False, alias="bFinish")


class UserFavSonglistItem(SongList):
    """用户收藏歌单条目."""

    id: int = Field(default=-1, alias="tid")
    dirid: int = Field(default=0, alias="dirId")
    title: str = Field(default="", alias="name")
    picurl: str = Field(default="", alias="logo")
    songnum: int = 0
    uin: str = ""
    nickname: str = ""
    create_time: int = Field(default=0, alias="createtime")
    update_time: int = Field(default=0, alias="updateTime")
    order_time: int = Field(default=0, alias="orderTime")
    dir_show: int = Field(default=0, alias="dirShow")
    dir_type: int = Field(default=0, alias="dirType")
    edge_mark: str = Field(default="", alias="edgeMark")
    layer_url: str = Field(default="", alias="layerUrl")
    album_pic_url: str = Field(default="", alias="albumPicUrl")
    op_type: int = Field(default=0, alias="opType")
    sort_weight: int = Field(default=0, alias="sortWeight")
    readtime: int = 0


class UserFavSonglistResponse(Response):
    """用户收藏歌单列表响应."""

    number: int = 0
    total: int = 0
    hasmore: int = 0
    hide: bool = False
    playlists: list[UserFavSonglistItem] | None = Field(default=None, json_schema_extra={"jsonpath": "$.v_list[*]"})
    deleted_ids: list[int] | None = Field(default=None, alias="v_delTids")
    failed_ids: list[int] | None = Field(default=None, alias="v_failTids")


class UserFavAlbumItem(Album):
    """用户收藏专辑条目."""

    id: int = -1
    mid: str = ""
    name: str = ""
    pmid: str = Field(default="", alias="logo")
    songnum: int = 0
    pubtime: int = 0
    ordertime: int = 0
    status: int = 0
    loc: int = 0
    singers: list[Singer] | None = Field(default=None, alias="v_singer")


class UserFavAlbumResponse(Response):
    """用户收藏专辑列表响应."""

    number: int = 0
    total: int = 0
    hasmore: int = 0
    hide: bool = False
    albums: list[UserFavAlbumItem] | None = Field(default=None, json_schema_extra={"jsonpath": "$.v_list[*]"})
    failed_album_ids: list[int] | None = Field(default=None, alias="v_failAlbumId")


class UserInfoCard(Response):
    """用户音乐基因卡片基础信息."""

    head_url: str = Field(default="", alias="HeadUrl")
    nick_name: str = Field(default="", alias="NickName")
    signature: str = Field(default="", alias="Signature")
    encryption_account: str = Field(default="", alias="EncryptionAccount")
    preferences: dict[str, Any] | None = Field(default=None, alias="Preferences")


class ListeningReport(Response):
    """用户听歌报告摘要."""

    report: list[dict[str, Any]] | None = Field(default=None, alias="Report")


class UserMusicGeneResponse(Response):
    """用户音乐基因响应."""

    user_info_card: UserInfoCard = Field(alias="UserInfoCard")
    listening_report: ListeningReport | None = Field(default=None, alias="ListeningReport")
    sort_array: list[int] = Field(default_factory=list, alias="SortArray")
    is_visit_account: bool = Field(default=False, alias="IsVisitAccount")


class UserHomepageBaseInfo(Response):
    """用户主页基础信息."""

    encrypted_uin: str = Field(default="", alias="EncryptedUin")
    name: str = Field(default="", alias="Name")
    avatar: str = Field(default="", alias="Avatar")
    background_image: str = Field(default="", alias="BackgroundImage")
    user_type: int = Field(default=0, alias="UserType")


class UserHomepageResponse(Response):
    """用户主页响应."""

    base_info: UserHomepageBaseInfo = Field(json_schema_extra={"jsonpath": "$.Info.BaseInfo"})
    singer: dict[str, Any] | None = Field(default=None, json_schema_extra={"jsonpath": "$.Info.Singer"})
    is_followed: int = Field(default=0, json_schema_extra={"jsonpath": "$.Info.IsFollowed"})
    tab_detail: dict[str, Any] | None = Field(default=None, alias="TabDetail")


class VipUserInfo(Response):
    """VIP 用户信息块."""

    buy_url: str = Field(default="", alias="buy_url")
    my_vip_url: str = Field(default="", alias="my_vip_url")
    score: int = 0
    expire: int = 0
    music_level: int = Field(default=0, alias="music_level")


class UserVipInfoResponse(Response):
    """VIP 信息响应."""

    auto_down: int = Field(default=0, alias="autoDown")
    can_renew: int = Field(default=0, alias="canRenew")
    max_dir_num: int = Field(default=0, alias="maxDirNum")
    max_song_num: int = Field(default=0, alias="maxSongNum")
    song_limit_msg: str = Field(default="", alias="songLimitMsg")
    userinfo: VipUserInfo | None = None


class RelationUser(Response):
    """关注关系用户条目."""

    mid: str = Field(default="", alias="MID")
    enc_uin: str = Field(default="", alias="EncUin")
    name: str = Field(default="", alias="Name")
    desc: str = Field(default="", alias="Desc")
    avatar_url: str = Field(default="", alias="AvatarUrl")
    fan_num: int = Field(default=0, alias="FanNum")
    is_follow: bool = Field(default=False, alias="IsFollow")


class UserRelationListResponse(Response):
    """关注关系列表响应."""

    total: int = Field(default=0, alias="Total")
    users: list[RelationUser] | None = Field(default=None, json_schema_extra={"jsonpath": "$.List[*]"})
    has_more: bool = Field(default=False, alias="HasMore")
    last_pos: str | None = Field(default=None, alias="LastPos")
    msg: str = Field(default="", alias="Msg")
    lock_flag: int = Field(default=0, alias="LockFlag")
    lock_msg: str = Field(default="", alias="LockMsg")


class FriendEntry(Response):
    """好友条目."""

    encrypt_uin: str = Field(default="", alias="EncryptUin")
    user_name: str = Field(default="", alias="UserName")
    avatar_url: str = Field(default="", alias="AvatarUrl")
    is_follow: bool = Field(default=False, alias="IsFollow")


class UserFriendListResponse(Response):
    """好友列表响应."""

    friends: list[FriendEntry] | None = Field(default=None, alias="Friends")
    has_more: bool = Field(default=False, alias="HasMore")


class UserFavMvItem(MV):
    """用户收藏 MV 条目."""

    id: int = Field(default=-1, validation_alias=AliasChoices("id", "mvid"))
    vid: str = ""
    name: str = Field(default="", validation_alias=AliasChoices("name", "title"))
    title: str = ""
    picurl: str = Field(default="", alias="picUrl")
    playcount: int = 0
    publish_date: int = 0
    singer_id: int = Field(default=0, alias="singerId")
    singer_mid: str = Field(default="", alias="singerMid")
    singer_name: str = Field(default="", alias="singerName")
    status: int = 0


class UserFavMvResponse(Response):
    """用户收藏 MV 列表响应."""

    code: int = 0
    sub_code: int = Field(default=0, alias="subCode")
    msg: str = ""
    mv_list: list[UserFavMvItem] | None = Field(default=None, alias="mvlist")
