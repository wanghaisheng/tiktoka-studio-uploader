"""
API Queries
:autodoc-skip:
"""

from typing import Literal, Union
from urllib.parse import quote, urlencode

from playwright.async_api import BrowserContext as AsyncContext
from playwright.sync_api import BrowserContext as SyncContext
from tiktokapipy import TikTokAPIError
from upgenius.tiktok.models.signing import (
    sign_and_get_request_async,
    sign_and_get_request_sync,
)

SUPPORTED_ENDPOINT = Literal[
    "comment/list/",
    "post/item_list/",
    "challenge/item_list/",
    "related/item_list/",
    "item/detail/",
    "challenge/detail/",
    # "user/detail/", # TODO - User detail requires msToken, X-Bogus, and _signature
    # "recommend/item_list/", # TODO - recommended list likely also requires msToken, X-Bogus, and _signature
]


TEMPLATE_QUERY_PARAMS_DICT = {
    "aid": 1988,
    "app_name": "tiktok_web",
    "browser_language": "en-US",  # TODO - Set dynamically?
    "browser_platform": "Win32",  # TODO - Set dynamically?
    "count": 20,
    "device_id": "",
    "device_platform": "web_pc",  # TODO - Set dynamically?
    "os": "windows",  # TODO - Set dynamically?
    "priority_region": "",
    "referrer": "",
    "region": "US",  # TODO - Set dynamically?
    "screen_height": 0,
    "screen_width": 0,
}


ENDPOINT_ID_MAP = {
    "comment/list/": "aweme_id",
    "post/item_list/": "secUid",
    "challenge/item_list/": "challengeID",
    "related/item_list/": "itemID",
    "item/detail/": "itemId",
    "challenge/detail/": "challengeName",
    # "user/detail/": "secUid",
}


# As of June 14, 2023, the following parameters are necessary to make comment API requests and don't seem to affect
# other API requests:
#
# * ``aid`` = 1988
# * ``app_name`` = tiktok_web
# * ``browser_language`` = en-US
# * ``browser_name`` = Mozilla
# * ``browser_platform`` = Win32
# * ``browser_version`` = Rest of UserAgent
# * ``count`` = 20
# * ``device_id`` (empty, but needed)
# * ``device_platform`` = web_pc
# * ``os`` = windows
# * ``priority_region`` (empty, but needed)
# * ``referer`` (empty, but needed)
# * ``region`` = US
# * ``screen_height`` (can be 0)
# * ``screen_width`` (can be 0)
#
# Unique to Video Detail (item/detail/):
# * ``itemId``
# * ``cursor`` and ``count`` don't seem to affect
#
# Unique to Challenge Detail (item/detail/):
# * ``challengeID``
# * ``challengeName``
# * ``cursor`` and ``count`` don't seem to affect
#
# Unique to Comments (comment/list/):
# * ``aweme_id``
# * ``cursor``
#
# Unique to Related Videos (related/item_list/):
# * ``itemID``
# * ``cursor``
#
# Unique to User Posts (post/item_list/):
# * ``secUid``
# * ``cursor`` is a Unix Timestamp. The retrieved videos are the newest ``count`` since before said timestamp
# * Next ``cursor`` is provided in response
# * Requires msToken cookie(s)
#
# Unique to Challenges (challenge/item_list/):
# * ``challengeID``
# * ``cursor``
#


async def get_necessary_query_params_async(
    context: AsyncContext, **extra_params
) -> str:
    """

    :param context: Playwright Context retrieved from :class:`.AsyncTikTokAPI` with ``api.context``
    :return: a paramstring containing query parameters necessary for all API calls
    """

    page = await context.new_page()
    agent: str = await page.evaluate("navigator.userAgent")
    await page.close()
    browser_name, browser_version = agent.split("/", 1)
    query = dict(
        **TEMPLATE_QUERY_PARAMS_DICT,
        browser_name=browser_name,
        browser_version=browser_version,
    )
    query.update(**extra_params)
    return urlencode(query)


def get_necessary_query_params_sync(context: SyncContext, **extra_params) -> str:
    """
    :param context: Playwright Context retrieved from :class:`.AsyncTikTokAPI` with ``api.context``
    :return: a paramstring containing query parameters necessary for all API calls
    """

    page = context.new_page()
    agent: str = page.evaluate("navigator.userAgent")
    page.close()
    browser_name, browser_version = agent.split("/", 1)
    query = dict(
        **TEMPLATE_QUERY_PARAMS_DICT,
        browser_name=browser_name,
        browser_version=browser_version,
    )
    query.update(**extra_params)
    return urlencode(query, quote_via=quote)


def get_id_type(endpoint: str) -> str:
    for k, v in ENDPOINT_ID_MAP.items():
        if k == endpoint:
            return v
    raise TikTokAPIError(f"Unsupported endpoint: {endpoint}")


async def make_request_async(
    endpoint: SUPPORTED_ENDPOINT,
    cursor: int,
    target_id: Union[int, str],
    context: AsyncContext,
    **extra_params,
) -> dict:
    params = await get_necessary_query_params_async(context, **extra_params)
    id_type = get_id_type(endpoint)
    params += f"&cursor={cursor}&{id_type}={target_id}"
    return await sign_and_get_request_async(
        f"https://www.tiktok.com/api/{endpoint}?{params}", context
    )


def make_request_sync(
    endpoint: SUPPORTED_ENDPOINT,
    cursor: int,
    target_id: Union[int, str],
    context: SyncContext,
    **extra_params,
) -> dict:
    params = get_necessary_query_params_sync(context, **extra_params)
    id_type = get_id_type(endpoint)
    params += f"&cursor={cursor}&{id_type}={target_id}"
    return sign_and_get_request_sync(
        f"https://www.tiktok.com/api/{endpoint}?{params}", context
    )


async def get_challenge_detail_async(challenge_name: str, context: AsyncContext):
    return await make_request_async("challenge/detail/", 0, challenge_name, context)


def get_challenge_detail_sync(challenge_name: str, context: SyncContext):
    return make_request_sync("challenge/detail/", 0, challenge_name, context)


def get_video_detail_sync(video_id: int, context: SyncContext):
    return make_request_sync("item/detail/", 0, video_id, context)


async def get_video_detail_async(video_id: int, context: AsyncContext):
    return await make_request_async("item/detail/", 0, video_id, context)


__all__ = [
    "get_necessary_query_params_async",
    "get_necessary_query_params_sync",
    "make_request_async",
    "make_request_sync",
    "get_challenge_detail_async",
    "get_challenge_detail_sync",
    "get_video_detail_async",
    "get_video_detail_sync",
]
