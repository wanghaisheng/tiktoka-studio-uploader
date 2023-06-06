import json
from tsup.utils.constants import *
from tsup.utils.logging import Log
from tsup.utils.exceptions import *
from tsup.youtube.youtube_helper import *
import os
from tsup.utils.login import *
from time import sleep
from datetime import datetime, date, timedelta
import logging
from playwright.async_api import async_playwright, Response, expect
import random
from tsup.utils.webdriver.setupPL import *
from tsup.utils.webdriver import (
    PlaywrightAsyncDriver,
    InterceptResponse,
    InterceptRequest,
)
from tsup.utils.webdriver import webdriver_pool_pl, WebDriverPoolPlayWright


class DouyinUpload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 3,
        watcheveryuploadstep: bool = True,
        debug: bool = True,
        username: str = "",
        password: str = "",
        CHANNEL_COOKIES: str = "",
        login_method: str = "phone",
        ytb_cookies: str = "",
        tiktok_cookies: str = "",
        recordvideo: bool = False,
    ) -> None:
        self.timeout = timeout
        self.log = Log(debug)
        self.username = username
        self.password = password
        self.CHANNEL_COOKIES = CHANNEL_COOKIES
        self.root_profile_directory = root_profile_directory
        self.proxy_option = proxy_option
        self.watcheveryuploadstep = watcheveryuploadstep
        self.ytb_cookies = ytb_cookies
        self.tiktok_cookies = tiktok_cookies
        self._playwright = ""
        self.browser = ""
        self.login_method = "qrcode"
        self.context = ""
        self.page = ""
        self.recordvideo = recordvideo
        # self.setup()

    async def upload(
        self,
        videopath: str = "",
        title: str = "",
        description: str = "",
        thumbnail: str = "",
        publishpolicy: str = 0,
        # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
        release_offset: str = "0-1",
        publish_date: datetime = datetime(
            date.today().year, date.today().month, date.today().day, 10, 15
        ),
        tags: list = [],
        location: str = "",
        miniprogram: str = "",
        hottopic: str = "",
        heji: str = "",
        up2toutiao: bool = False,
        allow2save: bool = True,
        allow2see: str = "公开",
        closewhen100percentupload: bool = True,
    ) -> Tuple[bool, Optional[str]]:
        """Uploads a video to douyin.
        Returns if the video was uploaded and the video id.
        """
        self._playwright = await self._start_playwright()
        #     browser = p.chromium.launch()

        # proxy_option = "socks5://127.0.0.1:1080"
        headless = True
        if self.watcheveryuploadstep:
            headless = False
        print("whether run in view mode", headless)
        if self.proxy_option == "":
            print("start web page without proxy")

            browserLaunchOptionDict = {
                "headless": headless,
                # "executable_path": executable_path,
                "timeout": 30000,
            }

            if not self.root_profile_directory:
                self.browser = await self._start_browser(
                    "firefox", **browserLaunchOptionDict
                )
                if self.recordvideo:
                    self.context = await self.browser.new_context(
                        record_video_dir=os.getcwd() + os.sep + "screen-recording"
                    )
                else:
                    self.context = await self.browser.new_context()
            else:
                self.context = await self._start_persistent_browser(
                    "firefox",
                    user_data_dir=self.root_profile_directory,
                    **browserLaunchOptionDict,
                )

        else:
            print("start web page with proxy")

            browserLaunchOptionDict = {
                "headless": headless,
                "proxy": {
                    "server": self.proxy_option,
                },
                # timeout <float> Maximum time in milliseconds to wait for the browser instance to start. Defaults to 30000 (30 seconds). Pass 0 to disable timeout.#
                "timeout": 30000,
            }

            if not self.root_profile_directory:
                self.browser = await self._start_browser(
                    "firefox", **browserLaunchOptionDict
                )
                if self.recordvideo:
                    self.context = await self.browser.new_context(
                        record_video_dir=os.getcwd() + os.sep + "screen-recording"
                    )
                else:
                    self.context = await self.browser.new_context()
            else:
                self.context = await self._start_persistent_browser(
                    "firefox",
                    user_data_dir=self.root_profile_directory,
                    **browserLaunchOptionDict,
                )

        self.log.debug("Firefox is now running")
        await self.context.grant_permissions(["geolocation"])
        page = await self.context.new_page()
        print("============tags", tags)
        if not videopath:
            raise FileNotFoundError(f'Could not find file with path: "{videopath}"')

        if self.CHANNEL_COOKIES and not self.CHANNEL_COOKIES == "":
            print("cookies existing", self.CHANNEL_COOKIES)

            await self.context.clear_cookies()
            cookies = await format_cookie_file(self.CHANNEL_COOKIES)
            await self.context.add_cookies(cookies)

            await page.goto(DOUYIN_URL, timeout=300000)

            await page.reload()
        else:
            self.log.debug("Please sign in and then press enter")
            # input()

            await page.goto(DOUYIN_URL, timeout=300000)
            # Interact with login form

            await self.context.clear_cookies()
            await page.locator(".login").click()
            await page.locator(".semi-button-content").click()
            if self.login_method == "phone-verify":
                await page.locator("div.semi-tabs-tab:nth-child(2)").click()
                await page.locator(".toggle").click()
                time.sleep(30)

            elif self.login_method == "password":
                print("not recommend")
                time.sleep(10)
                await page.fill(".semi-input-wrapper__with-prefix", self.username)
                await page.fill(
                    "div.semi-form-field:nth-child(2)>div>div>input", self.password
                )
                await page.locator(".agreement >img").click()
            elif self.login_method == "qrcode":
                print("pls open douyin to scan this qrcode")
                time.sleep(30)

            # page.click('text=Submit')
            sleep(USER_WAITING_TIME)
            storage = await self.context.storage_state(path=self.CHANNEL_COOKIES)
        await self.context.grant_permissions(["geolocation"])

        try:
            page.locator(".semi-modal-content")
            print("there is hint for 开始体验")
            await page.locator("button.semi-button:nth-child(3)").click()
            await page.locator(
                ".popoverFooter--2G_g0 > button:nth-child(1) > span:nth-child(1)"
            ).click()
            await page.locator(
                ".popoverFooter--2G_g0 > button:nth-child(1) > span:nth-child(1)"
            ).click()
        except:
            print("this is not the first time to login in")
        islogin = confirm_logged_in_douyin(page)

        print("checking login status", islogin)

        if not islogin:
            print("try to load cookie files")
            await self.context.clear_cookies()

            cookies = await format_cookie_file(self.CHANNEL_COOKIES)
            await self.context.add_cookies(cookies)

            print("success load cookie files")
            await page.goto(DOUYIN_URL, timeout=300000)
            print("start to check login status")

            islogin = confirm_logged_in_douyin(page)

            # https://github.com/xtekky/google-login-bypass/blob/main/login.py

        self.log.debug("Found douyin upload Dialog Modal")
        await page.goto(DOUYIN_UPLOAD_URL, timeout=300000)
        # sleep(self.timeout)

        self.log.debug(f'Trying to upload "{videopath}" to douyin...')
        if os.path.exists(get_path(videopath)):
            page.locator(DOUYIN_INPUT_FILE_VIDEO)
            await page.set_input_files(DOUYIN_INPUT_FILE_VIDEO, get_path(videopath))
        else:
            if os.path.exists(videopath.encode("utf-8")):
                print("file found", videopath)
                page.locator(DOUYIN_INPUT_FILE_VIDEO)
                await page.set_input_files(
                    DOUYIN_INPUT_FILE_VIDEO, videopath.encode("utf-8")
                )
        sleep(self.timeout)
        # accountcheck=await textbox.is_editable()
        # if not accountcheck:

        # try:

        # while True:
        #     check = page.locator('//*[@id="dialog-title"]')
        #     self.log.debug(f'found to douyin account check')
        #     x_path = '//*[@id="textbox"]'
        #     if page.locator(x_path):
        #         self.log.debug(f'fix  douyin account check')
        #         break

        # except:
        # sleep(1)

        self.log.debug(f'Trying to set "{title}" as title...')

        # get file name (default) title
        # title=title if title else page.locator(TEXTBOX).text_content()
        # print(title)
        sleep(self.timeout)

        if len(title) > DOUYIN_TITLE_COUNTER:
            print(
                f"Title was not set due to exceeding the maximum allowed characters ({len(title)}/{TITLE_COUNTER})"
            )
            title = title[: DOUYIN_TITLE_COUNTER - 1]

            # TITLE
        print("click title field to input")
        titlecontainer = page.locator(DOUYIN_TEXTBOX)
        await titlecontainer.click()
        print("clear existing title")
        await page.keyboard.press("Backspace")
        await page.keyboard.press("Control+KeyA")
        await page.keyboard.press("Delete")
        print("filling new  title")

        await page.keyboard.type(title)

        if thumbnail:
            self.log.debug(f'Trying to set "{thumbnail}" as thumbnail...')
            await page.locator(DOUYIN_INPUT_FILE_THUMBNAIL_EDIT).click()
            await page.locator(DOUYIN_INPUT_FILE_THUMBNAIL_OPTION_UPLOAD).click()

            if os.path.exists(get_path(thumbnail)):
                print("thumb file name without utf8")
                await page.locator(DOUYIN_INPUT_FILE_THUMBNAIL).set_input_files(
                    get_path(thumbnail)
                )
                time.sleep(USER_WAITING_TIME)

                # page.locator()
                # 如果缩略图尺寸不是9:16 会弹出裁剪框
                await page.locator(
                    DOUYIN_INPUT_FILE_THUMBNAIL_UPLOAD_TRIM_CONFIRM
                ).click()
                await page.locator(DOUYIN_INPUT_FILE_THUMBNAIL_UPLOAD_CONFIRM).click()
            else:
                if os.path.exists(thumbnail.encode("utf-8")):
                    print("thumbnail found", thumbnail)
                    await page.locator(DOUYIN_INPUT_FILE_THUMBNAIL).set_input_files(
                        thumbnail.encode("utf-8")
                    )
                    await page.locator(
                        DOUYIN_INPUT_FILE_THUMBNAIL_UPLOAD_TRIM_CONFIRM
                    ).click()

                    await page.locator(
                        DOUYIN_INPUT_FILE_THUMBNAIL_UPLOAD_CONFIRM
                    ).click()
                time.sleep(USER_WAITING_TIME)

            sleep(self.timeout)

        self.log.debug("Trying to set {location} to ")

        if location is None or location == "" or len(location) == 0:
            pass
        else:
            print("location you give", location)
            sleep(self.timeout)
            await page.locator(DOUYIN_LOCATION).click()
            print("clear existing location")
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(location)
            await page.keyboard.press("Enter")
            try:
                locationresultscount = await page.locator(
                    ".semi-select-option-list>div.semi-select-option"
                ).count()
                if locationresultscount > 0:
                    await page.locator("div.semi-select-option:nth-child(1)").click()
            except:
                print("no hint for location ", location)
            self.log.debug(f'Trying to set "{location}" as location...')

        self.log.debug("Trying to set {miniprogram} to ")

        if miniprogram is None or miniprogram == "" or len(miniprogram) == 0:
            pass
        else:
            print("miniprogram you give", miniprogram)
            sleep(self.timeout)
            await page.locator(DOUYIN_MINI_SELECT).click()
            await page.locator(DOUYIN_MINI_SELECT_OPTION).click()
            await page.locator(DOUYIN_MINI).click()
            print("clear existing location")
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(miniprogram)
            await page.keyboard.press("Enter")

            self.log.debug(f'Trying to set "{miniprogram}" as mini...')

        self.log.debug("Trying to set {hottopic} to ")

        if hottopic is None or hottopic == "" or len(hottopic) == 0:
            pass
        else:
            print("hottopic you give", hottopic)
            sleep(self.timeout)
            await page.locator(DOUYIN_HOT_TOPIC).click()
            print("clear existing hottopic")
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(hottopic)
            # 输入准确的热点词 可以保存
            # 输入的如果是提示词， 需从下拉列表中选择第一项
            try:
                hottopiccount = await page.locator(
                    ".semi-select-option-list > div.semi-select-option"
                ).count()
                if hottopiccount > 0:
                    await page.locator(
                        ".semi-select-option-list div.semi-select-option:nth-child(1)"
                    ).click()
            except:
                pass
            self.log.debug(f'Trying to set "{hottopic}" as hottopic...')

            self.log.debug(f'Trying to set "{hottopic}" as mini...')

        self.log.debug("Trying to set {heji} to ")

        if heji is None or heji == "" or len(heji) == 0:
            pass
        else:
            print("heji you give", heji)
            sleep(self.timeout)
            print("click to 选择合集")
            await page.locator(DOUYIN_HEJI_SELECT_OPTION).click()
            print("罗列已有合集")
            try:
                hejicount = await page.locator(
                    "div.mix-dropdown>div.semi-select-option-list"
                ).count()
                print("we found he ji count ", hejicount)
                if hejicount == 0:
                    print("pleas manual create 合集 first", heji)
                else:
                    index = 0
                    for i in hejicount:
                        text = (
                            await page.locator(
                                ".semi-select-option-list > div.semi-select-option"
                            )
                            .nth(i)
                            .text_content()
                        )
                        text = text.strip()

                        if text == heji:
                            index = i
                    if index == 0:
                        print("we cannot detect this heji,pleas  create 合集 first", heji)
                    else:
                        await page.locator(
                            ".semi-select-option-list div.semi-select-option:nth-child({index})"
                        ).click()
            except:
                print("暂无合集", heji)

            self.log.debug(f'Trying to set "{heji}" as heji...')

        self.log.debug("Trying to set {up2toutiao} to ")

        if up2toutiao is None or up2toutiao == False:
            pass
        else:
            await page.locator(".semi-switch-native-control").click()
        self.log.debug("Trying to set {allow2save} to ")

        if allow2save is None or allow2save == True:
            pass
        else:
            await page.locator(
                ".form--3R0Ka > div:nth-child(14) > div:nth-child(1) > label:nth-child(2)"
            ).click()

        self.log.debug("Trying to set {allow2see} to ")
        if heji:
            print("添加进合集或专辑的视频，无法设置好友可见或仅自己可见")
        else:
            if not allow2see in ["公开", "好友可见", "仅自己可见"]:
                allow2see = "公开"

            if allow2see is None or allow2see == "公开":
                pass
            elif allow2see == "好友可见":
                await page.locator(
                    ".publish-settings--3rCGw > div:nth-child(3) > label:nth-child(2)"
                ).click()
            elif allow2see == "仅自己可见":
                await page.locator(
                    ".publish-settings--3rCGw > div:nth-child(3) > label:nth-child(3)"
                ).click()

            else:
                print("请重新设置有效的值 只能是 公开、好友可见、仅自己可见", allow2see)

        if not publishpolicy in ["立即发布", "定时发布"]:
            publishpolicy = "立即发布"
        if publishpolicy == "立即发布":
            self.log.debug("Trying to set video visibility to 立即发布...")

        else:
            self.log.debug("Trying to set video visibility to 定时发布...")
            # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
            # mode b:release_offset not exist, publishdate exist , schedule to this specific date
            # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
            # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
            self.log.debug("Trying to set video schedule time...{publish_date}")
            if release_offset and not release_offset == "":
                if not int(release_offset.split("-")[0]) == 0:
                    offset = timedelta(
                        months=int(release_offset.split("-")[0]),
                        days=int(release_offset.split("-")[-1]),
                    )
                else:
                    offset = timedelta(days=1)
                if publish_date is None:
                    publish_date = datetime(
                        date.today().year, date.today().month, date.today().day, 10, 15
                    )
                else:
                    publish_date += offset

            else:
                if publish_date is None:
                    publish_date = datetime(
                        date.today().year, date.today().month, date.today().day, 10, 15
                    )
                    offset = timedelta(days=1)
                else:
                    publish_date = publish_date
                # dailycount=4

                # release_offset=str(int(start_index/30))+'-'+str(int(start_index)/int(setting['dailycount']))

            await setscheduletime_douyin(page, publish_date)
            # set_time_cssSelector(page,publish_date)

        retry_btn = r'//div[@class="word-card--1neCx"]/*[@class="text--GjPv4" and contains(text(),"重新上传")]'
        try:
            print("video is 100 uploading")

            page.locator(retry_btn)

            print("click publish button")
            await page.locator('//button[text()="发布"]').click()
            video_id = ""
            print(page.url)
            if "https://creator.douyin.com/creator-micro/content/manage" in page.url:
                print("提交成功:" + videopath)
            else:
                await page.screenshot(full_page=True)
                print("稿件提交失败，截图记录")
            sleep(5)
            logging.info("Upload is complete")
            await self.close()

            return True, video_id
        except:
            print("still uploading")
            return True

    async def get_video_id(self, page) -> Optional[str]:
        video_id = None
        try:
            video_url_container = page.locator(VIDEO_URL_CONTAINER)
            video_url_element = video_url_container.locator(VIDEO_URL_ELEMENT)

            video_id = await video_url_element.get_attribute(HREF)
            video_id = video_id.split("/")[-1]

            # if 'https://creator.douyin.com/creator-micro/content/manage' in self.driver.current_url :
            #     print('提交成功:' + videopath)
            #     print('Remove ' + videopath)
            #     os.remove(videopath)
            # else:
            #     self.driver.save_screenshot('err.png')
            #     print('稿件提交失败，截图记录')
        except:
            raise VideoIDError("Could not get video ID")

        return video_id

    # @staticmethod
    async def _start_playwright(self):
        #  sync_playwright().start()
        return await async_playwright().start()

    async def _start_browser(self, browsertype: str, **kwargs):
        if browsertype == "chromium":
            return await self._playwright.chromium.launch(**kwargs)

        if browsertype == "firefox":
            # return await self._playwright.firefox.launch(**kwargs)
            if self.recordvideo:
                return await self._playwright.firefox.launch(
                    record_video_dir=os.path.abspath("") + os.sep + "screen-recording",
                    **kwargs,
                )
            else:
                return await self._playwright.firefox.launch(**kwargs)

        if browsertype == "webkit":
            return await self._playwright.webkit.launch(**kwargs)

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox', or 'webkit' as browser."
        )

    async def _start_persistent_browser(
        self, browser: str, user_data_dir: Optional[Union[str, Path]], **kwargs
    ):
        if browser == "chromium":
            return await self._playwright.chromium.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "firefox":
            self.browser = await self._playwright.firefox.launch(**kwargs)

            if self.recordvideo:
                return await self._playwright.firefox.launch_persistent_context(
                    user_data_dir,
                    record_video_dir=os.path.abspath("") + os.sep + "screen-recording",
                    **kwargs,
                )
            else:
                return await self._playwright.firefox.launch_persistent_context(
                    user_data_dir, **kwargs
                )

        if browser == "webkit":
            return await self._playwright.webkit.launch_persistent_context(
                user_data_dir, **kwargs
            )

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox' or 'webkit' as browser."
        )

    async def close(self):
        await self.browser.close()
        await self._playwright.stop()
