"""User API 返回模型定义."""

from typing import Any

from pydantic import AliasChoices, Field

from .base import MV, Album, Singer, SongList
from .request import Response


class UserPlaylistSummary(SongList):
    """用户歌单列表中的单个歌单摘要.

    Attributes:
        id: 歌单 ID.
        dirid: 目录 ID.
        title: 歌单标题.
        picurl: 歌单封面地址.
        songnum: 歌曲数量.
        create_time: 创建时间戳.
        update_time: 更新时间戳.
        uin: 创建者 UIN.
        nick: 创建者昵称.
        desc: 歌单简介.
        bigpic_url: 大图封面地址.
        album_pic_url: 专辑拼接封面地址.
        avatar: 创建者头像.
        ident_icon: 身份图标地址.
        layer_url: 分层装饰地址.
        invalid: 是否失效.
        dir_show: 目录展示标记.
        create_fav_cnt: 创建者收藏量.
        play_cnt: 播放量.
        comment_cnt: 评论数.
        op_type: 操作类型标记.
        sort_weight: 排序权重.
    """

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
    """用户创建歌单列表页响应.

    Attributes:
        total: 歌单总数.
        playlists: 当前页歌单摘要列表.
        deleted_ids: 上游返回的删除歌单 ID 标记.
        finished: 是否已经拉取完成.
    """

    total: int = 0
    playlists: list[UserPlaylistSummary] | None = Field(default=None, json_schema_extra={"jsonpath": "$.v_playlist[*]"})
    deleted_ids: list[int] | int | None = Field(default=None, alias="v_delTid")
    finished: bool = Field(default=False, alias="bFinish")


class UserFavSonglistItem(SongList):
    """用户收藏歌单列表中的单个条目.

    Attributes:
        id: 歌单 ID.
        dirid: 目录 ID.
        title: 歌单标题.
        picurl: 歌单封面地址.
        songnum: 歌曲数量.
        uin: 歌单所属用户 UIN.
        nickname: 歌单拥有者昵称.
        create_time: 创建时间戳.
        update_time: 更新时间戳.
        order_time: 收藏排序时间戳.
        dir_show: 目录展示标记.
        dir_type: 目录类型.
        edge_mark: 边角标识.
        layer_url: 分层装饰地址.
        album_pic_url: 专辑拼接封面地址.
        op_type: 操作类型标记.
        sort_weight: 排序权重.
        readtime: 最近读取时间戳.
    """

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
    """用户收藏歌单列表页响应.

    Attributes:
        number: 当前页数量或请求数量.
        total: 收藏歌单总数.
        hasmore: 是否还有更多结果.
        hide: 列表是否隐藏.
        playlists: 当前页收藏歌单列表.
        deleted_ids: 上游返回的删除歌单 ID 列表.
        failed_ids: 拉取失败的歌单 ID 列表.
    """

    number: int = 0
    total: int = 0
    hasmore: int = 0
    hide: bool = False
    playlists: list[UserFavSonglistItem] | None = Field(default=None, json_schema_extra={"jsonpath": "$.v_list[*]"})
    deleted_ids: list[int] | None = Field(default=None, alias="v_delTids")
    failed_ids: list[int] | None = Field(default=None, alias="v_failTids")


class UserFavAlbumItem(Album):
    """用户收藏专辑列表中的单个专辑条目.

    Attributes:
        id: 专辑 ID.
        mid: 专辑 MID.
        name: 专辑名称.
        pmid: 专辑封面标识.
        songnum: 专辑曲目数.
        pubtime: 发布时间戳.
        ordertime: 收藏排序时间戳.
        status: 状态标记.
        loc: 位置或来源标记.
        singers: 专辑歌手列表.
    """

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
    """用户收藏专辑列表页响应.

    Attributes:
        number: 当前页数量或请求数量.
        total: 收藏专辑总数.
        hasmore: 是否还有更多结果.
        hide: 列表是否隐藏.
        albums: 当前页收藏专辑列表.
        failed_album_ids: 拉取失败的专辑 ID 列表.
    """

    number: int = 0
    total: int = 0
    hasmore: int = 0
    hide: bool = False
    albums: list[UserFavAlbumItem] | None = Field(default=None, json_schema_extra={"jsonpath": "$.v_list[*]"})
    failed_album_ids: list[int] | None = Field(default=None, alias="v_failAlbumId")


class UserInfoCard(Response):
    """用户音乐基因页头部卡片信息.

    Attributes:
        head_url: 头像地址.
        nick_name: 昵称.
        signature: 个性签名.
        encryption_account: 加密账号标识.
        preferences: 偏好信息块.
    """

    head_url: str = Field(default="", alias="HeadUrl")
    nick_name: str = Field(default="", alias="NickName")
    signature: str = Field(default="", alias="Signature")
    encryption_account: str = Field(default="", alias="EncryptionAccount")
    preferences: dict[str, Any] | None = Field(default=None, alias="Preferences")


class ListeningReport(Response):
    """用户听歌报告摘要.

    Attributes:
        report: 听歌报告分块列表.
    """

    report: list[dict[str, Any]] | None = Field(default=None, alias="Report")


class UserMusicGeneResponse(Response):
    """用户音乐基因视图响应.

    Attributes:
        user_info_card: 用户卡片信息.
        listening_report: 听歌报告摘要.
        sort_array: 排序提示数组.
        is_visit_account: 是否访问本人账号.
    """

    user_info_card: UserInfoCard = Field(alias="UserInfoCard")
    listening_report: ListeningReport | None = Field(default=None, alias="ListeningReport")
    sort_array: list[int] = Field(default_factory=list, alias="SortArray")
    is_visit_account: bool = Field(default=False, alias="IsVisitAccount")


class UserHomepageBaseInfo(Response):
    """用户主页头部基础信息.

    Attributes:
        encrypted_uin: 加密 UIN.
        name: 用户名.
        avatar: 头像地址.
        background_image: 背景图地址.
        user_type: 用户类型标记.
    """

    encrypted_uin: str = Field(default="", alias="EncryptedUin")
    name: str = Field(default="", alias="Name")
    avatar: str = Field(default="", alias="Avatar")
    background_image: str = Field(default="", alias="BackgroundImage")
    user_type: int = Field(default=0, alias="UserType")


class UserHomepageResponse(Response):
    """用户主页视图响应.

    Attributes:
        base_info: 主页头部基础信息.
        singer: 主页关联歌手信息.
        is_followed: 当前账号是否已关注.
        tab_detail: 主页标签页附加信息.
    """

    base_info: UserHomepageBaseInfo = Field(json_schema_extra={"jsonpath": "$.Info.BaseInfo"})
    singer: dict[str, Any] | None = Field(default=None, json_schema_extra={"jsonpath": "$.Info.Singer"})
    is_followed: int = Field(default=0, json_schema_extra={"jsonpath": "$.Info.IsFollowed"})
    tab_detail: dict[str, Any] | None = Field(default=None, alias="TabDetail")


class VipUserInfo(Response):
    """VIP 信息响应中的用户权益摘要块.

    Attributes:
        buy_url: 开通入口地址.
        my_vip_url: 我的会员页地址.
        score: 会员积分.
        expire: 到期时间戳.
        music_level: 音乐等级.
    """

    buy_url: str = Field(default="", alias="buy_url")
    my_vip_url: str = Field(default="", alias="my_vip_url")
    score: int = 0
    expire: int = 0
    music_level: int = Field(default=0, alias="music_level")


class UserVipInfoResponse(Response):
    """VIP 信息视图响应.

    Attributes:
        auto_down: 自动下载开关状态.
        can_renew: 是否可续费.
        max_dir_num: 最大歌单数量.
        max_song_num: 最大歌曲数量.
        song_limit_msg: 歌曲上限提示文案.
        userinfo: 用户权益摘要.
    """

    auto_down: int = Field(default=0, alias="autoDown")
    can_renew: int = Field(default=0, alias="canRenew")
    max_dir_num: int = Field(default=0, alias="maxDirNum")
    max_song_num: int = Field(default=0, alias="maxSongNum")
    song_limit_msg: str = Field(default="", alias="songLimitMsg")
    userinfo: VipUserInfo | None = None


class RelationUser(Response):
    """关注或粉丝列表中的单个用户条目.

    Attributes:
        mid: 用户 MID.
        enc_uin: 加密 UIN.
        name: 用户名称.
        desc: 描述文案.
        avatar_url: 头像地址.
        fan_num: 粉丝数.
        is_follow: 当前账号是否已关注.
    """

    mid: str = Field(default="", alias="MID")
    enc_uin: str = Field(default="", alias="EncUin")
    name: str = Field(default="", alias="Name")
    desc: str = Field(default="", alias="Desc")
    avatar_url: str = Field(default="", alias="AvatarUrl")
    fan_num: int = Field(default=0, alias="FanNum")
    is_follow: bool = Field(default=False, alias="IsFollow")


class UserRelationListResponse(Response):
    """关注关系分页列表响应.

    Attributes:
        total: 总数量.
        users: 当前页用户列表.
        has_more: 是否还有更多结果.
        last_pos: 下一页游标.
        msg: 附加消息.
        lock_flag: 锁定状态标记.
        lock_msg: 锁定提示文案.
    """

    total: int = Field(default=0, alias="Total")
    users: list[RelationUser] | None = Field(default=None, json_schema_extra={"jsonpath": "$.List[*]"})
    has_more: bool = Field(default=False, alias="HasMore")
    last_pos: str | None = Field(default=None, alias="LastPos")
    msg: str = Field(default="", alias="Msg")
    lock_flag: int = Field(default=0, alias="LockFlag")
    lock_msg: str = Field(default="", alias="LockMsg")


class FriendEntry(Response):
    """好友列表中的单个好友条目.

    Attributes:
        encrypt_uin: 加密 UIN.
        user_name: 用户名.
        avatar_url: 头像地址.
        is_follow: 当前账号是否已关注.
    """

    encrypt_uin: str = Field(default="", alias="EncryptUin")
    user_name: str = Field(default="", alias="UserName")
    avatar_url: str = Field(default="", alias="AvatarUrl")
    is_follow: bool = Field(default=False, alias="IsFollow")


class UserFriendListResponse(Response):
    """好友列表视图响应.

    Attributes:
        friends: 当前页好友列表.
        has_more: 是否还有更多结果.
    """

    friends: list[FriendEntry] | None = Field(default=None, alias="Friends")
    has_more: bool = Field(default=False, alias="HasMore")


class UserFavMvItem(MV):
    """用户收藏 MV 列表中的单个条目.

    Attributes:
        id: MV ID.
        vid: MV VID.
        name: MV 名称.
        title: MV 标题.
        picurl: MV 封面地址.
        playcount: 播放量.
        publish_date: 发布时间.
        singer_id: 歌手 ID.
        singer_mid: 歌手 MID.
        singer_name: 歌手名称.
        status: 状态标记.
    """

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
    """用户收藏 MV 列表视图响应.

    Attributes:
        code: 返回码.
        sub_code: 子返回码.
        msg: 附加消息.
        mv_list: 当前页收藏 MV 列表.
    """

    code: int = 0
    sub_code: int = Field(default=0, alias="subCode")
    msg: str = ""
    mv_list: list[UserFavMvItem] | None = Field(default=None, alias="mvlist")
