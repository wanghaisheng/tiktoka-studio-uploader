# -*- coding: utf-8 -*-
"""
Created on 2022/9/7 4:39 PM
---------
@summary:
---------
@author: Boris
@email: boris_liu@foxmail.com
"""
from upgenius.utils.webdriver.playwright_driver_async import PlaywrightAsyncDriver
from upgenius.utils.webdriver.playwright_driver_sync import PlaywrightSyncDriver
from upgenius.utils.webdriver.selenium_driver import SeleniumDriver
from upgenius.utils.webdriver.webdirver import InterceptRequest, InterceptResponse
from upgenius.utils.webdriver.webdriver_pool_pl import WebDriverPoolPlayWright
from upgenius.utils.webdriver.webdriver_pool_selenium import WebDriverPoolSelenium

# 为了兼容老代码
WebDriver = SeleniumDriver
