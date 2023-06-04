# -*- coding: utf-8 -*-
"""
Created on 2022/9/7 4:39 PM
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""
from tsup.utils.webdriver.playwright_driver_async import PlaywrightAsyncDriver
from tsup.utils.webdriver.playwright_driver_sync import PlaywrightSyncDriver
from tsup.utils.webdriver.selenium_driver import SeleniumDriver
from tsup.utils.webdriver.webdirver import InterceptRequest, InterceptResponse
from tsup.utils.webdriver.webdriver_pool_pl import WebDriverPoolPlayWright
from tsup.utils.webdriver.webdriver_pool_selenium import WebDriverPoolSelenium

# 为了兼容老代码
WebDriver = SeleniumDriver
