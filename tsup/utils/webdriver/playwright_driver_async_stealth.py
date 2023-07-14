# -*- coding: utf-8 -*-
"""
Created on 2023/06/01 4:11 PM
---------
@summary:
---------
@author: wanghaisheng
@email: admin@tiktokastudio.com
"""

import json
import os
import re
from collections import defaultdict
from typing import Union, List
import playwright_stealth

try:
    from typing import Literal  # python >= 3.8
except ImportError:  # python <3.8
    from typing_extensions import Literal
import asyncio

from playwright.async_api import Page, BrowserContext, ViewportSize, ProxySettings
from playwright.async_api import Playwright, Browser
from playwright.async_api import Response
from playwright.async_api import async_playwright

from tsup.utils import tools
from tsup.utils.log import log
from tsup.utils.webdriver.webdirver import *
from tsup.utils.fakebrowser import *

import filecmp
import requests


class PlaywrightAsyncDriverStealth(WebDriver):
    def __init__(
        self,
        *,
        page_on_event_callback: dict = None,
        storage_state_path: str = None,
        isRecodingVideo: bool = True,
        driver_type: Literal["chromium", "firefox", "webkit"] = "chromium",
        url_regexes: list = None,
        save_all: bool = False,
        **kwargs,
    ):
        """

        Args:
            page_on_event_callback: page.on() 事件的回调 如 page_on_event_callback={"dialog": lambda dialog: dialog.accept()}
            storage_state_path: 保存浏览器状态的路径
            driver_type: 浏览器类型 chromium, firefox, webkit
            url_regexes: 拦截接口，支持正则，数组类型
            save_all: 是否保存所有拦截的接口, 默认只保存最后一个
            **kwargs:
        """
        super(PlaywrightAsyncDriverStealth, self).__init__(**kwargs)
        self.driver: Playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.url = None
        self.storage_state_path = storage_state_path
        self.isRecodingVideo = isRecodingVideo
        self._driver_type = driver_type
        self._page_on_event_callback = page_on_event_callback
        self._url_regexes = url_regexes
        self._save_all = save_all
        self._timeout = 300
        self.country = None
        self.country_code = None
        self.region = None
        self.city = None
        self.zip = None
        self.latitude = None
        self.longitude = None
        self.timezone = None

        if self._save_all and self._url_regexes:
            log.warning(
                "获取完拦截的数据后, 请主动调用PlaywrightDriver的clear_cache()方法清空拦截的数据，否则数据会一直累加，导致内存溢出"
            )
            self._cache_data = defaultdict(list)
        else:
            self._cache_data = {}

    async def _setup(self):
        # 处理参数
        proxy = None               
        if self._proxy:
            proxy = self._proxy() if callable(self._proxy) else self._proxy
            proxy = self.format_context_proxy(proxy)
            if  not tools.url_ok(proxies=proxy,url='www.google.com'):

                await self.quit()
            self.proxy = Proxy(self._proxy)
            if not self.proxy.check:
                self.logger.error(f"Proxy Check Failed: {self.proxy.reason}")
                return False
            else:
                proxy = None            
        else:
            proxy = None
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.DEBUG)

        # 初始化浏览器对象
        self.driver = await async_playwright().start()
        self.browser = await getattr(self.driver, self._driver_type).launch(
            headless=self._headless,
            args=["--no-sandbox"],
            proxy=proxy,
            executable_path=self._executable_path,
            downloads_path=self._download_path,
            firefox_user_prefs={
                "media.peerconnection.enabled": False,
                "media.navigator.enabled": False,
                "privacy.resistFingerprinting": False,
            } if self._driver_type=='firefox' 
            else None,
        )
        # Initializing Faker, ComputerInfo, PersonInfo and ProxyInfo

        self.faker = Faker(self.proxy.httpx_proxy,self._driver_type)

        await self.faker.computer()
        # await self.faker.person()

        await self.faker.locale(self.proxy.country_code)
        print(f"self locale is:{self.faker.locale}")
        # Context for more options
        print(f"self.proxy.longitude:{self.proxy.longitude}")
        print(f"self.proxy.latitude:{self.proxy.latitude}")
        print(f"self.proxy.timezone:{self.proxy.timezone}")
        print(f"self.proxy.useragent:{self.faker.useragent}")
        print(f"self.proxy.storage_state_path:{self.storage_state_path}")
        print(f"self.proxy.username:{self.proxy.username}")
        print(f"self.proxy.password:{self.proxy.password}")

        self.context = await self.browser.new_context(
            locale=self.faker.locale,  # self.faker.locale
            geolocation={
                "longitude": self.proxy.longitude,
                "latitude": self.proxy.latitude,
                "accuracy": 0.7,
            },
            timezone_id=self.proxy.timezone,
            permissions=["geolocation"],
            # screen={"width": self.faker.avail_width, "height": self.faker.avail_height},
            user_agent=self.faker.useragent,
            no_viewport=True,
            # viewport={"width": self.faker.width, "height": self.faker.height},
            proxy=proxy,
            # here proxy format is important
            storage_state=self.storage_state_path if self._isRecodingVideo else None,
            record_video_dir=os.getcwd() + os.sep + "screen-recording"
            if self._isRecodingVideo
            else None,
            http_credentials={
                "username": self.proxy.username,
                "password": self.proxy.password,
            }
            if self.proxy.username
            else None,
        )
        # Grant Permissions to Discord to use Geolocation
        await self.context.grant_permissions(["geolocation"], origin=self.url)
        # Create new Page and do something idk why i did that lol
        # await page.emulate_media(
        #     color_scheme="dark", media="screen", reduced_motion="reduce"
        # )
        self.page = await self.context.new_page()

        # Stealthen the page with custom Stealth Config
        
        config = playwright_stealth.StealthConfig()
        (
            config.navigator_languages,
            config.permissions,
            config.navigator_platform,
            config.navigator_vendor,
            config.outerdimensions,
        ) = (False, False, False, False, False)
        config.vendor, config.renderer, config.nav_user_agent, config.nav_platform = (
            self.faker.vendor,
            self.faker.renderer,
            self.faker.useragent,
            "Win32",
        )
        config.languages = ("en-US", "en", self.faker.locale, self.faker.language_code)

        await playwright_stealth.stealth_async(self.page, config)
        self.page.set_default_timeout(self._timeout * 1000)


        return self

    async def __aenter__(self):
        print("async Enter!", self)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            log.error(exc_val)
        await self.quit()
        return True

    @classmethod
    async def create(self, **kwargs):
        self = PlaywrightAsyncDriverStealth(**kwargs)
        await self._setup()

        return self

    def format_context_proxy(self, proxy) -> ProxySettings:
        """
        Args:
            proxy: username:password@ip:port / ip:port
        Returns:
            {
                "server": "ip:port"
                "username": username,
                "password": password,
            }
            server: http://ip:port or socks5://ip:port. Short form ip:port is considered an HTTP proxy.
        """

        if "@" in proxy:
            certification, _proxy = proxy.split("@")
            username, password = certification.split(":")

            context_proxy = ProxySettings(
                server=_proxy,
                username=username,
                password=password,
            )
        else:
            context_proxy = ProxySettings(server=proxy)

        return context_proxy

    async def save_storage_stage(self):
        if self.storage_state_path:
            os.makedirs(os.path.dirname(self.storage_state_path), exist_ok=True)
            await self.context.storage_state(path=self.storage_state_path)

    async def quit(self):
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.driver:
            await self.driver.stop()

    @property
    def domain(self):
        return tools.get_domain(self.url or self.page.url)

    @property
    def cookies(self):
        cookies_json = {}
        for cookie in self.page.context.cookies():
            cookies_json[cookie["name"]] = cookie["value"]

        return cookies_json

    @cookies.setter
    async def cookies(self, val: Union[dict, List[dict]]):
        """
        设置cookie
        Args:
            val: List[{name: str, value: str, url: Union[str, NoneType], domain: Union[str, NoneType], path: Union[str, NoneType], expires: Union[float, NoneType], httpOnly: Union[bool, NoneType], secure: Union[bool, NoneType], sameSite: Union["Lax", "None", "Strict", NoneType]}]

        Returns:

        """
        if isinstance(val, list):
            await self.page.context.add_cookies(val)
        else:
            cookies = []
            for key, value in val.items():
                cookies.append(
                    {"name": key, "value": value, "url": self.url or self.page.url}
                )
            await self.page.context.add_cookies(cookies)

    @property
    async def user_agent(self):
        return await self.page.evaluate("() => navigator.userAgent")
