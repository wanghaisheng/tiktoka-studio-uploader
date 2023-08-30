import abc
import time
import warnings
from datetime import datetime
from json import JSONDecodeError
from typing import AsyncIterator, ForwardRef, Iterator, List, Literal, TypeVar, Union

from playwright.async_api import BrowserContext as AsyncBrowserContext
from playwright.sync_api import BrowserContext as SyncBrowserContext
from tsup.tiktok.models  import TikTokAPIError, TikTokAPIWarning
from tsup.tiktok.models.queries import (
    get_challenge_detail_async,
    get_challenge_detail_sync,
    make_request_async,
    make_request_sync,
)

T = TypeVar("T")
Challenge = ForwardRef("Challenge")
Comment = ForwardRef("Comment")
User = ForwardRef("User")
Video = ForwardRef("Video")


class DeferredIterator(abc.ABC, Iterator[T], AsyncIterator[T]):
    def __init__(self, api):
        self._api = api
        self._collected_values = []
        self._head = 0
        self._cursor = 0
        self._has_more = True
        self._limit = -1

    @abc.abstractmethod
    def _fetch_sync(self):
        pass

    @abc.abstractmethod
    async def _fetch_async(self):
        pass

    def __iter__(self):
        if isinstance(self._api.context, AsyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use AsyncTikTokAPI in a synchronous context. Use `async for` instead."
            )
        self._head = 0
        return self

    def __next__(self):
        if isinstance(self._api.context, AsyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use AsyncTikTokAPI in a synchronous context. Use `async for` instead."
            )

        if 0 <= self._limit <= self._head:
            raise StopIteration

        if self._head >= len(self._collected_values):
            if not self._has_more:
                raise StopIteration
            self._fetch_sync()

        if 0 <= self._limit < len(self._collected_values):
            self._collected_values = self._collected_values[: self._limit]
            self._has_more = False

        out = self._collected_values[self._head]
        self._head += 1
        return out

    def __aiter__(self):
        if isinstance(self._api.context, SyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use TikTokAPI in an asynchronous context. Use `for` instead."
            )
        self._head = 0
        return self

    async def __anext__(self):
        if isinstance(self._api.context, SyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use TikTokAPI in an asynchronous context. Use `for` instead."
            )

        if 0 <= self._limit <= self._head:
            raise StopAsyncIteration

        if self._head >= len(self._collected_values):
            if not self._has_more:
                raise StopAsyncIteration
            await self._fetch_async()

        if 0 <= self._limit < len(self._collected_values):
            self._collected_values = self._collected_values[: self._limit]
            self._has_more = False

        out = self._collected_values[self._head]
        self._head += 1
        return out

    def __getitem__(self, item):
        return self._collected_values[item]

    def limit(self, limit: int) -> "DeferredIterator":
        """
        Set a limit to the number of items to iterate over. Can be useful to not iterate over an absurdly large amount
        of data.

        Example usage:

        .. code-block:: python

            for something in iterator.limit(30):
                # do something

        """
        if limit < 0:
            self._limit = -1
            return self
        self._limit = limit
        if len(self._collected_values) > self._limit:
            self._collected_values = self._collected_values[: self._limit]
            self._has_more = False
        return self


class DeferredCommentIterator(DeferredIterator[Comment]):
    def __init__(self, api, video_id: int):
        super().__init__(api)
        self._video_id = video_id

    def _fetch_sync(self):
        from tiktokapipy.models.raw_data import APIResponse

        raw = make_request_sync(
            "comment/list/", self._cursor, self._video_id, self._api.context
        )
        converted = APIResponse.model_validate(raw)
        for comment in converted.comments:
            comment._api = self._api
        self._has_more = converted.has_more
        self._collected_values += converted.comments
        self._cursor = converted.cursor

    async def _fetch_async(self):
        from tiktokapipy.models.raw_data import APIResponse

        raw = await make_request_async(
            "comment/list/", self._cursor, self._video_id, self._api.context
        )
        converted = APIResponse.model_validate(raw)
        for comment in converted.comments:
            comment._api = self._api
        self._has_more = converted.has_more
        self._collected_values += converted.comments
        self._cursor = converted.cursor


class DeferredItemListIterator(DeferredIterator[Video]):
    def __init__(
        self,
        api,
        from_type: Literal["post", "challenge"],
        target_id: Union[int, str],
        **extra_params,
    ):
        super().__init__(api)
        self.from_type = from_type
        self._target_id = target_id
        self._extra_params = extra_params

        if self.from_type == "post":
            self._cursor = int(time.time()) * 1000

    def _fetch_sync(self):
        from tiktokapipy.models.raw_data import APIResponse

        # noinspection PyTypeChecker
        try:
            raw = make_request_sync(
                f"{self.from_type}/item_list/",
                self._cursor,
                self._target_id,
                self._api.context,
                **self._extra_params,
            )
        except JSONDecodeError:
            readable_cursor = (
                f"video #{self._cursor}"
                if self.from_type == "challenge"
                else datetime.fromtimestamp(self._cursor // 1000).strftime("%c")
            )
            warnings.warn(
                f"Unable to grab videos beyond {readable_cursor} (JSONDecodeError), stopping iteration early."
                f"Try again if you think this is a mistake.",
                category=TikTokAPIWarning,
                stacklevel=2,
            )
            self._has_more = False
            raise StopIteration
        converted = APIResponse.model_validate(raw)
        if not converted.item_list:
            self._has_more = False
            raise StopIteration
        self._has_more = converted.has_more
        self._cursor = converted.cursor

        for video in converted.item_list:
            try:
                self._collected_values.append(self._api.video(video.id))
            except TikTokAPIError:
                warnings.warn(
                    f"Unable to grab video with id {video.id}",
                    category=TikTokAPIWarning,
                    stacklevel=2,
                )

    async def _fetch_async(self):
        from tiktokapipy.models.raw_data import APIResponse

        # noinspection PyTypeChecker
        try:
            raw = await make_request_async(
                f"{self.from_type}/item_list/",
                self._cursor,
                self._target_id,
                self._api.context,
                **self._extra_params,
            )
        except JSONDecodeError:
            readable_cursor = (
                f"video #{self._cursor}"
                if self.from_type == "challenge"
                else datetime.fromtimestamp(self._cursor).strftime("%c")
            )
            warnings.warn(
                f"Unable to grab videos beyond {readable_cursor}, stopping iteration early."
                f"Try again if you think this is a mistake.",
                category=TikTokAPIWarning,
                stacklevel=2,
            )
            self._has_more = False
            raise StopAsyncIteration
        converted = APIResponse.model_validate(raw)
        if not converted.item_list:
            self._has_more = False
            raise StopAsyncIteration
        self._has_more = converted.has_more
        self._cursor = converted.cursor
        for video in converted.item_list:
            try:
                self._collected_values.append(await self._api.video(video.id))
            except TikTokAPIError:
                warnings.warn(
                    f"Unable to grab video with id {video.id}",
                    category=TikTokAPIWarning,
                    stacklevel=2,
                )


class DeferredChallengeIterator(Iterator[Challenge], AsyncIterator[Challenge]):
    def __init__(self, api, challenge_names: List[str]):
        self._api = api
        self._collected_values: List[Challenge] = []
        self._challenge_names = challenge_names
        self.head = 0

    def _fetch_sync(self):
        from tiktokapipy.models.raw_data import ChallengePage

        converted = ChallengePage.model_validate(
            get_challenge_detail_sync(
                self._challenge_names[self.head], self._api.context
            )
        )
        challenge = converted.challenge_info.challenge
        challenge._api = self._api
        self._collected_values.append(challenge)

    async def _fetch_async(self):
        from tiktokapipy.models.raw_data import ChallengePage

        converted = ChallengePage.model_validate(
            await get_challenge_detail_async(
                self._challenge_names[self.head], self._api.context
            )
        )
        challenge = converted.challenge_info.challenge
        challenge._api = self._api
        self._collected_values.append(challenge)

    def __iter__(self):
        if isinstance(self._api.context, AsyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use AsyncTikTokAPI in a synchronous context. Use `async for` instead."
            )
        self.head = 0
        return self

    def __next__(self):
        if isinstance(self._api.context, AsyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use AsyncTikTokAPI in a synchronous context. Use `async for` instead."
            )
        if self.head == len(self._collected_values):
            if self.head == len(self._challenge_names):
                raise StopIteration
            self._fetch_sync()
        out = self._collected_values[self.head]
        self.head += 1
        return out

    def __aiter__(self):
        if isinstance(self._api.context, SyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use TikTokAPI in an asynchronous context. Use `for` instead."
            )
        self.head = 0
        return self

    async def __anext__(self):
        if isinstance(self._api.context, SyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use TikTokAPI in an asynchronous context. Use `for` instead."
            )
        if self.head == len(self._collected_values):
            if self.head == len(self._challenge_names):
                raise StopAsyncIteration
            await self._fetch_async()
        out = self._collected_values[self.head]
        self.head += 1
        return out


class DeferredUserGetterSync:
    def __init__(self, api, unique_id: str):
        self._api = api
        self._unique_id = unique_id
        self._user = None

    def __call__(self) -> User:
        if isinstance(self._api.context, AsyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use AsyncTikTokAPI in an synchronous context."
            )
        if self._user is None:
            self._user = self._api.user(self._unique_id)
            self._user._api = self._api
        return self._user


class DeferredUserGetterAsync:
    def __init__(self, api, unique_id: str):
        self._api = api
        self._unique_id = unique_id
        self._user = None

    async def __call__(self) -> User:
        if isinstance(self._api.context, SyncBrowserContext):
            raise TikTokAPIError(
                "Attempting to use TikTokAPI in a asynchronous context."
            )
        if self._user is None:
            self._user = await self._api.user(self._unique_id)
            self._user._api = self._api
        return self._user
