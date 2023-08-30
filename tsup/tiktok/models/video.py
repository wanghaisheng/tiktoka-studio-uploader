#https://raw.githubusercontent.com/Russell-Newton/TikTokPy/main/src/tiktokapipy/models/video.py
"""Video data models"""

from __future__ import annotations

from datetime import datetime
from functools import cached_property
from typing import Any, ForwardRef, List, Optional, Union

from playwright.async_api import BrowserContext as AsyncBrowserContext
from pydantic import AliasChoices, Field, computed_field
from tsup.tiktok.models import CamelCaseModel, TitleCaseModel,TikTokAPIError
from tsup.tiktok.models.deferred_collectors import (
    DeferredChallengeIterator,
    DeferredCommentIterator,
    DeferredUserGetterAsync,
    DeferredUserGetterSync,
)

LightChallenge = ForwardRef("LightChallenge")
Challenge = ForwardRef("Challenge")
Comment = ForwardRef("Comment")
LightUser = ForwardRef("LightUser")
User = ForwardRef("User")
UserStats = ForwardRef("UserStats")


class VideoStats(CamelCaseModel):
    digg_count: int
    share_count: int
    comment_count: int
    play_count: int
    collect_count: int


class SubtitleData(TitleCaseModel):
    language_id: int
    language_code_name: str
    url: str
    url_expire: int
    format: str
    version: int
    source: str
    # video_subtitle_ID: int
    size: int


class VideoData(CamelCaseModel):
    """Contains data about a downloadable video"""

    # id: int
    height: int
    width: int
    duration: int
    ratio: str
    format: Optional[str] = None
    bitrate: Optional[int] = None
    # encoded_type: str
    # video_quality: str
    # encode_user_tag: str
    # codec_type: str
    # definition: str
    # subtitle_infos: Optional[List[SubtitleData]]

    ################
    # Video stills #
    ################
    cover: str
    origin_cover: str
    dynamic_cover: Optional[str] = None
    share_cover: Optional[List[str]] = None
    reflow_cover: Optional[str] = None

    ###############
    # Video links #
    ###############
    play_addr: Optional[str] = None
    download_addr: Optional[str] = None


class MusicData(CamelCaseModel):
    """Contains data about the music within a video"""

    id: int
    title: str
    play_url: Optional[str] = None
    author_name: Optional[str] = None
    duration: int
    original: bool
    album: Optional[str] = None

    cover_large: str
    cover_medium: str
    cover_thumb: str

    # schedule_search_time: int


class ImageUrlList(CamelCaseModel):
    """
    Contains a list of 3 urls that can be used to access an image. Each URL is different, sometimes only the last will
    be populated.
    """

    url_list: List[str]


class ImageData(CamelCaseModel):
    image_url: ImageUrlList = Field(
        ..., alias="imageURL", description="3 urls that can be used to access the image"
    )
    image_width: int
    image_height: int


class ImagePost(CamelCaseModel):
    images: List[ImageData]
    """All images in the slideshow"""
    cover: ImageData
    """Still image on the video before playing"""
    share_cover: ImageData
    """Still image embedded with a sharing link"""
    title: Optional[str] = None


class LightVideo(CamelCaseModel):
    """Bare minimum information for scraping"""

    id: int = Field(validation_alias=AliasChoices("cid", "uid", "id"))
    """The unique video ID"""
    # Have this here to sort the iteration.
    stats: VideoStats
    """Stats about the video"""
    create_time: datetime


class Video(LightVideo):
    #####################
    # Content and stats #
    #####################
    desc: str
    """Video description"""
    diversification_labels: Optional[List[str]] = None
    """Tags/Categories applied to the video"""
    challenges: Optional[List[LightChallenge]] = None
    """
    We don't want to grab anything more than the title so we can generate the lazy challenge getter.
    :autodoc-skip:
    """
    video: VideoData
    music: MusicData
    # digged: bool
    # item_comment_status: int
    # location_created: Optional[str]
    image_post: Optional[ImagePost] = None
    """The images in the video if the video is a slideshow"""

    ######################
    # Author information #
    ######################
    author: Union[LightUser, str]
    """
    We don't want to grab anything more than the unique_id so we can generate the lazy user getter.
    :autodoc-skip:
    """
    # nickname: Optional[str]
    # author_id: Optional[int]  # redundant with the lazy author getter
    # author_sec_id: Optional[str]
    # avatar_thumb: Optional[Union[str, dict]]
    # author_stats: "UserStats"

    ##########################
    # Duet/stitching/sharing #
    ##########################
    # stitch_enabled: bool
    # duet_enabled: bool
    # share_enabled: bool
    # private_item: bool
    # duet_info: dict
    # duet_display: int         # display format of duet I think
    # stitch_display: int       # display format of stitch
    # mix_info: Optional[dict]

    ##########################################################
    # Ad and Security info (not sure what most of these are) #
    ##########################################################
    # is_ad: bool
    # ad_authorization: bool
    # ad_label_version: int
    # original_item: bool
    # offical_item: bool                # this is a typo
    # is_activity_item: Optional[bool]
    # secret: bool
    # index_enabled: Optional[bool]
    # show_not_pass: bool

    #################################################
    # Misc fields (not sure what most of these are) #
    #################################################
    # schedule_time: Optional[int]
    # take_down: Optional[int]
    # item_mute: bool
    # text_extra: Optional[list]
    # effect_stickers: Optional[list]
    # stickers_on_item: Optional[list]
    # for_friend: bool
    # vl1: bool

    @computed_field(repr=False)
    @property
    def _api(self) -> Any:
        if not hasattr(self, "_api_internal"):
            self._api_internal = None
        return self._api_internal

    @_api.setter
    def _api(self, api):
        self._api_internal = api

    @computed_field(repr=False)
    @cached_property
    def comments(self) -> DeferredCommentIterator:
        if self._api is None:
            raise TikTokAPIError(
                "A TikTokAPI must be attached to video._api before collecting comments"
            )
        return DeferredCommentIterator(self._api, self.id)

    @computed_field(repr=False)
    @cached_property
    def tags(self) -> DeferredChallengeIterator:
        if self._api is None:
            raise TikTokAPIError(
                "A TikTokAPI must be attached to video._api before collecting comments"
            )
        return DeferredChallengeIterator(
            self._api,
            [challenge.title for challenge in self.challenges]
            if self.challenges
            else [],
        )

    @computed_field(repr=False)
    @cached_property
    def creator(self) -> Union[DeferredUserGetterAsync, DeferredUserGetterSync]:
        if self._api is None:
            raise TikTokAPIError(
                "A TikTokAPI must be attached to video._api before retrieving creator data"
            )
        unique_id = (
            self.author if isinstance(self.author, str) else self.author.unique_id
        )
        if isinstance(self._api.context, AsyncBrowserContext):
            return DeferredUserGetterAsync(self._api, unique_id)
        else:
            return DeferredUserGetterSync(self._api, unique_id)

    @computed_field(repr=False)
    @cached_property
    def url(self) -> str:
        """The url to the video on TikTok."""
        return video_link(self.id)


del Challenge, LightChallenge, Comment, LightUser, User, UserStats


from tiktokapipy.models.challenge import Challenge, LightChallenge  # noqa E402
from tiktokapipy.models.comment import Comment  # noqa E402
from tiktokapipy.models.user import LightUser, User, UserStats  # noqa E402

Video.model_rebuild()


def video_link(video_id: int) -> str:
    """Get a working link to a TikTok video from the video's unique id."""
    return f"https://m.tiktok.com/v/{video_id}"


def is_mobile_share_link(link: str) -> bool:
    import re

    return re.match(r"https://vm\.tiktok\.com/[0-9A-Za-z]*", link) is not None
