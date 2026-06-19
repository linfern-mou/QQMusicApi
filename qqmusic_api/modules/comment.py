"""评论模块."""

from typing import Any, cast

from ..core.pagination import (
    CursorStrategy,
    MultiFieldContinuationStrategy,
    PagerMeta,
    PaginationParams,
    ResponseAdapter,
)
from ..core.versioning import Platform
from ..models.comment import AddCommentResponse, CommentCountResponse, CommentListResponse, MomentCommentResponse
from ..models.request import Credential
from ._base import ApiModule


def _build_comment_pager_meta() -> PagerMeta:
    """构建评论列表接口使用的 continuation 策略."""

    def build_next_params(
        params: PaginationParams,
        response: CommentListResponse,
        adapter: ResponseAdapter,
    ) -> PaginationParams | None:
        next_seq_no = adapter.get_cursor(response)
        if next_seq_no is None:
            return None
        next_params = cast("dict[str, Any]", params.copy())
        next_params["PageNum"] = next_params["PageNum"] + 1
        next_params["LastCommentSeqNo"] = next_seq_no
        return next_params

    return PagerMeta(
        strategy=MultiFieldContinuationStrategy(build_next_params, context_name="comment_list"),
        adapter=ResponseAdapter(
            has_more_flag="has_more",
            total="total",
            cursor=lambda response: response.comments[-1].seq_no if response.comments else None,
        ),
    )


class CommentApi(ApiModule):
    """评论 API."""

    def get_comment_count(self, biz_id: int):
        """获取歌曲评论数量.

        Args:
            biz_id: 歌曲 ID.
        """
        # 支持 request_list
        data = {
            "request": {
                "biz_id": str(biz_id),
                "biz_type": 1,
                "biz_sub_type": 2,
            },
        }
        return self._build_request(
            "music.globalComment.CommentCountSrv",
            "GetCmCount",
            data,
            response_model=CommentCountResponse,
        )

    def get_hot_comments(
        self,
        biz_id: int,
        page_num: int = 1,
        page_size: int = 15,
        last_comment_seq_no: str = "",
    ):
        """获取歌曲热评.

        Args:
            biz_id: 歌曲 ID.
            page_num: 页码.
            page_size: 每页数量.
            last_comment_seq_no: 上一页最后一条评论 ID (可选).
        """
        params = {
            "BizType": 1,
            "BizId": str(biz_id),
            "LastCommentSeqNo": last_comment_seq_no,
            "PageSize": page_size,
            "PageNum": page_num - 1,
            "HotType": 1,
            "WithAirborne": 0,
            "PicEnable": 1,
        }
        return self._build_request(
            "music.globalComment.CommentRead",
            "GetHotCommentList",
            params,
            response_model=CommentListResponse,
            pager_meta=_build_comment_pager_meta(),
        )

    def get_new_comments(
        self,
        biz_id: int,
        page_num: int = 1,
        page_size: int = 15,
        last_comment_seq_no: str = "",
    ):
        """获取歌曲最新评论.

        Args:
            biz_id: 歌曲 ID.
            page_num: 页码.
            page_size: 每页数量.
            last_comment_seq_no: 上一页最后一条评论 ID (可选).
        """
        params = {
            "PageSize": page_size,
            "PageNum": page_num - 1,
            "HashTagID": "",
            "BizType": 1,
            "PicEnable": 1,
            "LastCommentSeqNo": last_comment_seq_no,
            "SelfSeeEnable": 1,
            "BizId": str(biz_id),
            "AudioEnable": 1,
        }
        return self._build_request(
            "music.globalComment.CommentRead",
            "GetNewCommentList",
            params,
            response_model=CommentListResponse,
            pager_meta=_build_comment_pager_meta(),
        )

    def get_recommend_comments(
        self,
        biz_id: int,
        page_num: int = 1,
        page_size: int = 15,
        last_comment_seq_no: str = "",
    ):
        """获取歌曲推荐评论.

        Args:
            biz_id: 歌曲 ID.
            page_num: 页码.
            page_size: 每页数量.
            last_comment_seq_no: 上一页最后一条评论 ID (可选).
        """
        params = {
            "PageSize": page_size,
            "PageNum": page_num - 1,
            "BizType": 1,
            "PicEnable": 1,
            "Flag": 1,
            "LastCommentSeqNo": last_comment_seq_no,
            "CmListUIVer": 1,
            "BizId": str(biz_id),
            "AudioEnable": 1,
        }
        return self._build_request(
            "music.globalComment.CommentRead",
            "GetRecCommentList",
            params,
            response_model=CommentListResponse,
            pager_meta=_build_comment_pager_meta(),
        )

    def get_moment_comments(
        self,
        biz_id: int,
        page_size: int = 15,
        last_comment_seq_no: str = "",
    ):
        """获取歌曲时刻评论.

        Args:
            biz_id: 歌曲 ID.
            page_size: 每页数量.
            last_comment_seq_no: 上一页最后一条评论 ID (可选).
        """
        params = {
            "LastPos": last_comment_seq_no,
            "HashTagID": "",
            "SeekTs": -1,
            "Size": page_size,
            "BizType": 1,
            "BizId": str(biz_id),
        }
        return self._build_request(
            "music.globalComment.SongTsComment",
            "GetSongTsCmList",
            params,
            response_model=MomentCommentResponse,
            pager_meta=PagerMeta(
                strategy=CursorStrategy(cursor_key="LastPos"),
                adapter=ResponseAdapter(has_more_flag="has_more", cursor="next_pos"),
            ),
        )

    def add_comment(
        self,
        biz_id: int,
        content: str,
        reply_cmt_id: str | None = None,
        credential: Credential | None = None,
    ):
        """添加评论.

        固定使用 Android 平台.

        Args:
            biz_id: 歌曲 ID.
            content: 评论内容.
            reply_cmt_id: 回复的评论 ID.
            credential: 登录凭据.
        """
        return self._build_request(
            "music.globalComment.CommentWriteServer",
            "AddComment",
            {
                "Content": content,
                "BizType": 1,
                "BizId": str(biz_id),
                "RepliedCmId": reply_cmt_id,
            },
            credential=credential,
            platform=Platform.ANDROID,
            response_model=AddCommentResponse,
            require_login=True,
        )

    async def delete_comment(
        self,
        cm_id: str,
        credential: Credential | None = None,
    ) -> bool:
        """删除评论.

        固定使用 Android 平台.

        Args:
            cm_id: 评论 ID.
            credential: 登录凭据.

        Returns:
            是否删除成功,评论不存在也为 True.
        """
        data = await self._build_request(
            "music.globalComment.CommentWriteServer",
            "DelComment",
            {
                "CommentId": cm_id,
            },
            platform=Platform.ANDROID,
            credential=credential,
            require_login=True,
        )
        return data.get("SubCode", 0) == 0
