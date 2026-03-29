"""SingerAPI 返回模型定义."""

from typing import Any

from pydantic import AliasChoices, Field

from .base import MV, Album, Singer, Song
from .request import Response


class TagOption(Response):
    """歌手筛选标签项."""

    id: int
    name: str = ""


class SingerBrief(Singer):
    """歌手列表条目."""

    id: int = Field(default=-1, validation_alias=AliasChoices("singer_id", "singerId", "id"))
    mid: str = Field(default="", validation_alias=AliasChoices("singer_mid", "singerMid", "mid"))
    name: str = Field(default="", validation_alias=AliasChoices("singer_name", "singerName", "name"))
    pmid: str = Field(default="", validation_alias=AliasChoices("singer_pmid", "singerPmid", "pmid"))
    area_id: int = -1
    country_id: int = -1
    country: str = ""
    other_name: str = ""
    spell: str = ""
    trend: int = 0
    concern_num: int = Field(default=0, alias="concernNum")
    singer_pic: str = ""


class SingerTagData(Response):
    """歌手筛选标签集合."""

    area: list[TagOption] = Field(default_factory=list)
    genre: list[TagOption] = Field(default_factory=list)
    sex: list[TagOption] = Field(default_factory=list)
    index: list[TagOption] = Field(default_factory=list)


class SingerTypeListResponse(Response):
    """歌手列表响应."""

    area: int = -100
    sex: int = -100
    genre: int = -100
    singerlist: list[SingerBrief] = Field(default_factory=list)
    code: int = 0
    hotlist: list[SingerBrief] = Field(default_factory=list)
    tags: SingerTagData | None = None


class SingerIndexPageResponse(SingerTypeListResponse):
    """按索引分页的歌手列表响应."""

    index: int = -100
    total: int = 0


class HomepageBaseInfo(Response):
    """歌手主页基础信息."""

    encrypted_uin: str = Field(default="", alias="EncryptedUin")
    background_image: str = Field(default="", alias="BackgroundImage")
    avatar: str = Field(default="", alias="Avatar")
    name: str = Field(default="", alias="Name")
    is_host: int = Field(default=0, alias="IsHost")
    is_singer: int = Field(default=0, alias="IsSinger")
    user_type: int = Field(default=0, alias="UserType")


class HomepageSinger(Response):
    """歌手主页歌手信息."""

    id: int = Field(default=-1, validation_alias=AliasChoices("SingerID", "singerID", "singer_id"))
    mid: str = Field(default="", validation_alias=AliasChoices("SingerMid", "singerMid", "singer_mid"))
    name: str = Field(default="", validation_alias=AliasChoices("Name", "name", "singerName"))
    type: int = Field(default=-1, validation_alias=AliasChoices("SingerType", "type"))
    singer_pic: str = Field(default="", alias="SingerPic")
    singer_pmid: str = Field(default="", alias="SingerPMid")


class TabMeta(Response):
    """主页标签元信息."""

    tab_id: str = Field(default="", alias="TabID")
    tab_name: str = Field(default="", alias="TabName")
    title: str = Field(default="", alias="Title")


class AlbumBrief(Album):
    """歌手相关专辑条目."""

    id: int = Field(default=-1, alias="albumID")
    mid: str = Field(default="", alias="albumMid")
    name: str = Field(default="", alias="albumName")
    subtitle: str = Field(default="", alias="albumTranName")
    time_public: str = Field(default="", alias="publishDate")
    total_num: int = Field(default=0, alias="totalNum")
    album_type: str = Field(default="", alias="albumType")
    singer_name: str = Field(default="", alias="singerName")
    tags: list[str] | None = None


class VideoBrief(MV):
    """歌手视频条目."""

    id: int = Field(default=-1, alias="mvid")
    vid: str = ""
    type: int = -1
    title: str = ""
    picurl: str = ""
    picformat: int = 0
    duration: int = 0
    playcnt: int = 0
    pubdate: int = 0
    icon_type: int = 0


class HomepageTabDetailResponse(Response):
    """歌手主页标签详情响应."""

    tab_id: str = Field(default="", alias="TabID")
    has_more: int = Field(default=0, alias="HasMore")
    need_show_tab: int = Field(default=0, alias="NeedShowTab")
    order: int = Field(default=0, alias="Order")
    tab_list: list[TabMeta] | None = Field(default=None, alias="TabList")
    introduction_tab: list[dict[str, Any]] | None = Field(
        default=None,
        json_schema_extra={"jsonpath": "$.IntroductionTab.List"},
    )
    song_tab: list[Song] | None = Field(default=None, json_schema_extra={"jsonpath": "$.SongTab.List[*]"})
    album_tab: list[AlbumBrief] | None = Field(default=None, json_schema_extra={"jsonpath": "$.AlbumTab.AlbumList[*]"})
    video_tab: list[VideoBrief] | None = Field(default=None, json_schema_extra={"jsonpath": "$.VideoTab.VideoList[*]"})


class HomepageHeaderResponse(Response):
    """歌手主页头部响应."""

    status: int = Field(alias="Status")
    singer: HomepageSinger = Field(json_schema_extra={"jsonpath": "$.Info.Singer"})
    base_info: HomepageBaseInfo = Field(json_schema_extra={"jsonpath": "$.Info.BaseInfo"})
    tab_detail: HomepageTabDetailResponse = Field(alias="TabDetail")
    prompt: dict[str, Any] | None = Field(default=None, alias="Prompt")


class SingerBasicInfo(Singer):
    """歌手详情基础信息."""

    id: int = Field(default=-1, alias="singer_id")
    mid: str = Field(default="", alias="singer_mid")
    name: str = Field(default="", alias="name")
    type: int = Field(default=-1, alias="type")
    pmid: str = Field(default="", alias="singer_pmid")
    has_photo: int = Field(default=0, alias="has_photo")
    wikiurl: str = ""


class SingerExtraInfo(Response):
    """歌手详情扩展信息."""

    area: str | int = ""
    desc: str = ""
    tag: str = ""
    identity: str | int = ""
    instrument: str | int = ""
    genre: str | int = ""
    foreign_name: str = ""
    birthday: str = ""
    enter: str | int = ""
    blog_flag: int = Field(default=0, alias="blogFlag")


class SingerDetail(Response):
    """歌手详情条目."""

    basic_info: SingerBasicInfo = Field(alias="basic_info")
    ex_info: SingerExtraInfo | None = Field(default=None, alias="ex_info")
    wiki: str | list[dict[str, Any]] | None = None
    group_list: list[dict[str, Any]] = Field(default_factory=list)
    photos: list[dict[str, Any]] = Field(default_factory=list)
    group_info: list[dict[str, Any]] | None = None


class SingerDetailResponse(Response):
    """歌手详情响应."""

    singer_list: list[SingerDetail] = Field(default_factory=list, alias="singer_list")


class SimilarSinger(Singer):
    """相似歌手条目."""

    id: int = Field(default=-1, alias="singerId")
    mid: str = Field(default="", alias="singerMid")
    name: str = Field(default="", alias="singerName")
    pmid: str = Field(default="", alias="pic_mid")
    singer_pic: str = Field(default="", alias="singerPic")
    trace: str = ""
    abt: str = ""
    tf: str = ""


class SimilarSingerResponse(Response):
    """相似歌手列表响应."""

    singerlist: list[SimilarSinger] = Field(default_factory=list)
    code: int = 0
    err_msg: str = Field(default="", alias="errMsg")


class SingerSongListResponse(Response):
    """歌手歌曲列表响应."""

    singer_mid: str = Field(default="", alias="singerMid")
    total_num: int = Field(default=0, alias="totalNum")
    song_list: list[Song] = Field(default_factory=list, json_schema_extra={"jsonpath": "$.songList[*].songInfo"})


class SingerAlbumListResponse(Response):
    """歌手专辑列表响应."""

    singer_mid: str = Field(default="", alias="singerMid")
    total: int = 0
    album_list: list[AlbumBrief] = Field(default_factory=list, alias="albumList")


class SingerMvListResponse(Response):
    """歌手 MV 列表响应."""

    total: int = 0
    mv_list: list[VideoBrief] = Field(default_factory=list, alias="list")
