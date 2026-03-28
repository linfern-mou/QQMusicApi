"""SongAPI 返回定义."""

from pydantic import Field

from .base import MV, Singer, Song, SongList
from .request import Response


class QuerySongResponse(Response):
    """查询歌曲结果.

    Attributes:
        tracks: 歌曲列表.
    """

    tracks: list[Song]


class UrlinfoItem(Response):
    """表示 GetEVkey/GetVkey 返回的单个文件授权结果.

    Attributes:
        mid: 歌曲 mid.
        filename: 请求的目标文件名.
        purl: 相对下载路径,需要与 CDN 域名拼接后才能访问.
        vkey: 资源访问令牌,歌曲文件通常依赖该字段完成鉴权。
        ekey: 加密资源解密密钥.
        result: 单个文件的业务结果码。常见值为 `0`(成功)、`104003`(无权限)、
                `104004`(VKey 获取失败)、`104013`(播放设备受限)。
    """

    mid: str = Field(alias="songmid")
    filename: str
    purl: str
    vkey: str
    ekey: str
    result: int


class GetSongUrlsResponse(Response):
    """获取歌曲链接结果.

    Attributes:
        expiration: 链接过期时间 (秒).
        data: 链接信息列表.
    """

    expiration: int
    data: list[UrlinfoItem] = Field(alias="midurlinfo")


class ContentItem(Response):
    """表示 GetSongDetail 返回的内容项.

    Attributes:
        id: 内容项 ID.
        value: 内容项值.
        show_type: 内容项展示类型.
        jumpurl: 内容项跳转链接.
    """

    id: int
    value: str
    show_type: int
    jumpurl: str


class GetSongDetailResponse(Response):
    """获取歌曲详情结果.

    Attributes:
        company: 发行公司信息.
        genre: 歌曲类型信息.
        intro: 歌曲简介信息.
        lan: 语言信息.
        pub_time: 发布时间信息.
        extra: 额外信息.
        track: 歌曲基本信息.
    """

    company: list[ContentItem] = Field(json_schema_extra={"jsonpath": "$.info.company.content"})
    genre: list[ContentItem] = Field(json_schema_extra={"jsonpath": "$.info.genre.content"})
    intro: list[ContentItem] = Field(json_schema_extra={"jsonpath": "$.info.intro.content"})
    lan: list[ContentItem] = Field(json_schema_extra={"jsonpath": "$.info.lan.content"})
    pub_time: list[ContentItem] = Field(json_schema_extra={"jsonpath": "$.info.pub_time.content"})
    extras: dict[str, str]
    track: Song = Field(alias="track_info")


class SimilarSongGroup(Response):
    """一组相似歌曲推荐卡片.

    Attributes:
        title_template: 推荐分组的标题模板.
        title_content: 标题模板中的实际内容.
        song: 当前推荐分组下的歌曲列表.
    """

    title_template: str
    title_content: str
    song: list[Song] = Field(json_schema_extra={"jsonpath": "$.songs[*].track"})


class GetSimilarSongResponse(Response):
    """表示获取相似歌曲接口的响应结果.

    Attributes:
        tag: 相似歌曲结果附带的歌曲标签列表.
        song: 相似歌曲推荐分组列表.
    """

    tag: list[dict] = Field(alias="songTagInfoList")
    song: list[SimilarSongGroup] = Field(json_schema_extra={"jsonpath": "$.vecSongNew"})


class SongLabel(Response):
    """歌曲标签项.

    Attributes:
        id: 标签 ID.
        tag_txt: 标签文本.
        tag_icon: 标签图标地址.
        tag_url: 标签跳转链接.
        tag_type: 标签类型.
        species: 标签所属分类.
    """

    id: int
    tag_txt: str = Field(alias="tagTxt")
    tag_icon: str = Field(alias="tagIcon")
    tag_url: str = Field(alias="tagUrl")
    tag_type: int = Field(alias="tagType")
    species: int


class GetSongLabelsResponse(Response):
    """获取歌曲标签结果.

    Attributes:
        labels: 歌曲标签列表.
    """

    labels: list[SongLabel]


class RelatedPlaylist(SongList):
    """相关歌单项.

    Attributes:
        creator: 歌单创建者.
    """

    creator: str = ""


class GetRelatedSonglistResponse(Response):
    """获取歌曲相关歌单结果.

    Attributes:
        has_more: 是否还有更多结果.
        songlist: 相关歌单列表.
    """

    has_more: int = Field(alias="hasMore")
    songlist: list[RelatedPlaylist] = Field(json_schema_extra={"jsonpath": "$.vecPlaylistNew[*].playlists[*]"})


class RelatedMv(MV):
    """相关 MV 项.

    Attributes:
        picurl: MV 封面.
        playcnt: MV 播放量.
        singers: MV 歌手名称列表.
    """

    class MVSinger(Singer):
        """歌手信息.

        Attributes:
            picurl: 歌手头像地址.
        """

        picurl: str

    picurl: str
    playcnt: int
    singers: list[MVSinger] = Field(json_schema_extra={"jsonpath": "$.singers"})


class GetRelatedMvResponse(Response):
    """获取歌曲相关 MV 结果.

    Attributes:
        has_more: 是否还有更多结果.
        mv: 相关 MV 列表.
    """

    has_more: int = Field(alias="hasmore")
    mv: list[RelatedMv] = Field(alias="list")


class GetOtherVersionResponse(Response):
    """获取歌曲其他版本结果.

    Attributes:
        data: 其他版本歌曲列表.
    """

    data: list[Song] = Field(alias="versionList")


class SongProducer(Response):
    """歌曲制作人项.

    Attributes:
        type: 制作人类型.
        name: 制作人名称.
        icon: 制作人头像.
        scheme: 制作人跳转链接.
        singer_mid: 制作人 singer mid.
        follow: 关注状态.
    """

    type: int = Field(alias="Type")
    name: str = Field(alias="Name")
    icon: str = Field(alias="Icon")
    scheme: str = Field(alias="Scheme")
    singer_mid: str = Field(alias="SingerMid")
    follow: int = Field(alias="Follow")


class SongProducerGroup(Response):
    """歌曲制作人分组.

    Attributes:
        title: 分组标题.
        producers: 制作人列表.
        type: 分组类型.
    """

    title: str = Field(alias="Title")
    producers: list[SongProducer] = Field(alias="Producers")
    type: int = Field(alias="Type")


class GetProducerResponse(Response):
    """获取歌曲制作人信息结果.

    Attributes:
        data: 制作人分组列表.
        reinforce_msg: 摘要文案.
    """

    data: list[SongProducerGroup] = Field(alias="Lst")
    reinforce_msg: str = Field(alias="ReinforceMsg")


class SheetMusic(Response):
    """曲谱项.

    Attributes:
        score_mid: 曲谱 MID.
        score_name: 曲谱名称.
        pic_urls: 曲谱图片列表.
        version: 曲谱版本说明.
        tonality: 调号.
        score_type: 曲谱类型.
        score_type_text: 曲谱类型文本.
        uploader: 上传者.
        view_frequency: 浏览量.
        tonality2: 第二调号值.
        author: 作者.
        composer: 作曲.
        lyricist: 作词.
        singer: 演唱者.
        performer: 演奏者.
        song_mid: 关联歌曲 MID.
        sub_name: 曲谱副标题.
        url: 曲谱详情链接.
        album_url: 专辑链接.
        ins_type: 乐器类型.
        ins_type_text: 乐器类型文本.
        cover_url: 乐器封面.
        difficulty: 难度.
        sheet_file: 曲谱文件地址.
    """

    score_mid: str = Field(alias="scoreMID")
    score_name: str = Field(alias="scoreName")
    pic_urls: list[str] = Field(alias="picURLs")
    version: str
    tonality: int
    score_type: int = Field(alias="scoreType")
    score_type_text: str = Field(alias="strScoreType")
    uploader: str
    view_frequency: int = Field(alias="viewFrequency")
    tonality2: int
    author: str
    composer: str
    lyricist: str
    singer: str
    performer: str
    song_mid: str = Field(alias="songMID")
    sub_name: str = Field(alias="subName")
    url: str
    album_url: str = Field(alias="albumURL")
    ins_type: int = Field(alias="insType")
    ins_type_text: str = Field(alias="strInsType")
    cover_url: str = Field(alias="coverURL")
    difficulty: str
    sheet_file: str = Field(alias="sheetFile")


class GetSheetResponse(Response):
    """获取歌曲相关曲谱结果.

    Attributes:
        result: 曲谱列表.
        total_map: 按类型聚合的曲谱数量.
    """

    result: list[SheetMusic]
    total_map: dict[str, int] = Field(alias="totalMap")


class GetFavNumResponse(Response):
    """获取歌曲收藏人数结果.

    Attributes:
        numbers: 歌曲收藏人数原始值映射.
        show: 歌曲收藏人数展示值映射.
    """

    numbers: dict[str, int] = Field(alias="m_numbers")
    show: dict[str, str] = Field(alias="m_show")
