# -*- coding: utf-8 -*-
"""
Created on 2022/9/7 4:39 PM
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""
from .playwright_driver_async import PlaywrightAsyncDriver
from .playwright_driver_sync import PlaywrightSyncDriver
from .selenium_driver import SeleniumDriver
from .webdirver import InterceptRequest, InterceptResponse
from .webdriver_pool_pl import WebDriverPoolPlayWright
from .webdriver_pool_selenium import WebDriverPoolSelenium

# 为了兼容老代码
WebDriver = SeleniumDriver
