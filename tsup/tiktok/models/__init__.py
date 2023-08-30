"""
Pydantic models used to load and store TikTok data
"""

from __future__ import annotations

from re import sub

from pydantic import BaseModel

# noinspection PyProtectedMember
from pydantic._internal._model_construction import ModelMetaclass
from collections import defaultdict


class TikTokAPIError(Exception):
    """Raised when the API encounters an error"""

    pass


class TikTokAPIWarning(RuntimeWarning):
    pass


ERROR_CODES = defaultdict(
    lambda: "Unknown Error",
    {
        0: "OK",
        450: "CLIENT_PAGE_ERROR",
        10000: "VERIFY_CODE",
        10101: "SERVER_ERROR_NOT_500",
        10102: "USER_NOT_LOGIN",
        10111: "NET_ERROR",
        10113: "SHARK_SLIDE",
        10114: "SHARK_BLOCK",
        10119: "LIVE_NEED_LOGIN",
        10202: "USER_NOT_EXIST",
        10203: "MUSIC_NOT_EXIST",
        10204: "VIDEO_NOT_EXIST",
        10205: "HASHTAG_NOT_EXIST",
        10208: "EFFECT_NOT_EXIST",
        10209: "HASHTAG_BLACK_LIST",
        10210: "LIVE_NOT_EXIST",
        10211: "HASHTAG_SENSITIVITY_WORD",
        10212: "HASHTAG_UNSHELVE",
        10213: "VIDEO_LOW_AGE_M",
        10214: "VIDEO_LOW_AGE_T",
        10215: "VIDEO_ABNORMAL",
        10216: "VIDEO_PRIVATE_BY_USER",
        10217: "VIDEO_FIRST_REVIEW_UNSHELVE",
        10218: "MUSIC_UNSHELVE",
        10219: "MUSIC_NO_COPYRIGHT",
        10220: "VIDEO_UNSHELVE_BY_MUSIC",
        10221: "USER_BAN",
        10222: "USER_PRIVATE",
        10223: "USER_FTC",
        10224: "GAME_NOT_EXIST",
        10225: "USER_UNIQUE_SENSITIVITY",
        10227: "VIDEO_NEED_RECHECK",
        10228: "VIDEO_RISK",
        10229: "VIDEO_R_MASK",
        10230: "VIDEO_RISK_MASK",
        10231: "VIDEO_GEOFENCE_BLOCK",
        10404: "FYP_VIDEO_LIST_LIMIT",
        "undefined": "MEDIA_ERROR",
    },
)


def _to_camel(field: str) -> str:
    # replace _ and - with space, title case, and remove spaces
    field = sub(r"[_\-]+", " ", field).title().replace(" ", "")
    # make first character lowercase
    return field[0].lower() + field[1:]


def _to_title(field: str) -> str:
    # replace _ and - with space, title case, and remove spaces
    field = sub(r"[_\-]+", " ", field).title().replace(" ", "")
    return field


class DataModelDefaultDocumentor(ModelMetaclass):
    """:autodoc-skip:"""

    def __init__(cls, *args):
        if not cls.__doc__:
            cls.__doc__ = f"{cls.__name__} data"
        super().__init__(*args)


class TikTokDataModel(BaseModel, metaclass=DataModelDefaultDocumentor):
    """:autodoc-skip:"""

    def __init_subclass__(cls, **kwargs):
        if not cls.__doc__:
            cls.__doc__ = f"{cls.__name__} model"
            super.__init_subclass__()


class CamelCaseModel(TikTokDataModel):
    """:autodoc-skip:"""

    model_config = dict(
        alias_generator=_to_camel,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class TitleCaseModel(TikTokDataModel):
    """:autodoc-skip:"""

    model_config = dict(
        alias_generator=_to_title,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


__all__ = [
    "CamelCaseModel",
    "TikTokDataModel",
    "TitleCaseModel",
]
