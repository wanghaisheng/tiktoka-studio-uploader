import json
from upgenius.constants import *
from upgenius.logging import Log
from upgenius.exceptions import *
from upgenius.youtubeHelper import *
import os
from upgenius.login import *
from time import sleep
from datetime import datetime, date, timedelta
import logging
import random
from upgenius.utils.webdriver import (
    PlaywrightAsyncDriver,
    InterceptResponse,
    InterceptRequest,
)
from playwright.async_api import Page, expect, Playwright, Browser, BrowserContext
from cf_clearance import async_cf_retry, async_stealth


class TiktokUpload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 200 * 1000,
        headless: bool = True,
        debug: bool = True,
        username: str = "",
        password: str = "",
        recoveryemail: str = "",
        browserType: Literal["chromium", "firefox", "webkit"] = "firefox",
        login_method: Literal["mailpassword", "phone", "qrcode"] = "mailpassword",
        # 'chromium', 'firefox', or 'webkit'
        CHANNEL_COOKIES: str = "",
        closewhen100percent: int = 2,
        # 0-uploading done
        # 1-Processing done
        # 2-Checking done
        recordvideo: bool = False,
    ) -> None:
        self.timeout = timeout
        self.log = Log(debug)
        self.username = username
        self.password = password
        self.CHANNEL_COOKIES = CHANNEL_COOKIES
        self.root_profile_directory = root_profile_directory
        self.proxy_option = proxy_option
        self.headless = headless
        self.browserType = browserType
        self.login_method = login_method
        self.pl: Playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.closewhen100percent = closewhen100percent
        self.recordvideo = recordvideo

    def send(self, element, text: str) -> None:
        element.clear()
        sleep(self.timeout)
        element.send_keys(text)
        sleep(self.timeout)

    async def click_next(self, page) -> None:
        await page.locator(NEXT_BUTTON).click()
        sleep(random(5 * 1000, self.timeout))

    async def not_uploaded(self, page) -> bool:
        s = await page.locator(STATUS_CONTAINER).text_content()
        return s.find(UPLOADED) != -1

    async def not_processed(self, page) -> bool:
        s = await page.locator(STATUS_CONTAINER).text_content()
        return s.find(PROCESSED) != -1

    async def not_copyrightchecked(self, page) -> bool:
        s = await page.locator(STATUS_CONTAINER).text_content()
        return s.find(CHECKED) != -1

    async def upload(
        self,
        videopath: str = "",
        title: str = "",
        description: str = "",
        thumbnail: str = "",
        publishpolicy: Optional[int] = 0,
        date_to_publish: Optional[datetime] = datetime(
            date.today().year, date.today().month, date.today().day
        ),
        hour_to_publish: Optional[str] = "10:15",
        playlist: Optional[str] = None,
        miniprogram: str = "",
        hottopic: str = "",
        heji: str = "",
        up2toutiao: bool = False,
        allow2save: bool = True,
        allow2see: str = "公开",
        VideoLanguage: Optional[str] = None,
        # input language str and get index in the availableLanguages list
        CaptionsCertification: Optional[int] = 0,
        # parse from video metadata  using ffmpeg
        location: Optional[str] = None,
        VideoRecordinglocation: Optional[str] = None,
        LicenceType: Optional[int] = 0,
        isAllowEmbedding: Optional[bool] = True,
        isPublishToSubscriptionsFeedNotify: Optional[bool] = True,
        ShortsremixingType: Optional[int] = 0,
        Category: Optional[str] = None,
        CommentsRatingsPolicy: Optional[int] = 1,
        isShowHowManyLikes: Optional[bool] = True,
        tags: list = [],
    ) -> Tuple[bool, Optional[str]]:
        """Uploads a video to YouTube.
        Returns if the video was uploaded and the video id.
        """
        print(f"default closewhen100percent:{self.closewhen100percent}")
        video_id = None
        if hour_to_publish and hour_to_publish not in availableScheduleTimes:
            self.logger.debug(
                f"you give a invalid hour_to_publish:{self.hour_to_publish}, ,try to choose one of them{availableScheduleTimes},we change it to  default 10:15"
            )
            hour_to_publish = "10:15"
        if (
            self.closewhen100percent
            and self.closewhen100percent not in closewhen100percentOptions
        ):
            self.logger.debug(
                f"you give a invalid closewhen100percent:{self.closewhen100percent}, ,try to choose one of them{closewhen100percentOptions},we change it to  default 2"
            )
            self.closewhen100percent = 2

        if publishpolicy and publishpolicy not in PublishpolicyOptions:
            self.logger.debug(
                f"you give a invalid publishpolicy:{publishpolicy} ,try to choose one of them{PublishpolicyOptions},we change it to  default 0"
            )
            publishpolicy = 0
        else:
            print(f"publishpolicy:{publishpolicy}")
        if VideoLanguage is not None:
            if VideoLanguage and VideoLanguage not in VideoLanguageOptions:
                self.logger.debug(
                    f"you give a invalid VideoLanguage:{VideoLanguage} ,try to choose one of them{VideoLanguageOptions},we change it to  default None"
                )
                VideoLanguage = None
            else:
                print(f"VideoLanguage:{VideoLanguage}")

        if (
            CaptionsCertification
            and CaptionsCertification not in CaptionsCertificationOptions
        ):
            self.logger.debug(
                f"you give a invalid publishpolicy:{CaptionsCertification} ,try to choose one of them{CaptionsCertificationOptions},we change it to  default 0"
            )
            CaptionsCertification = 0
        else:
            print(f"CaptionsCertification:{CaptionsCertification}")

        if LicenceType and LicenceType not in LicenceTypeOptions:
            self.logger.debug(
                f"you give a invalid LicenceType:{LicenceType} ,try to choose one of them{LicenceTypeOptions},we change it to  default 0"
            )
            LicenceType = 0
        else:
            print(f"LicenceType:{LicenceType}")

        if ShortsremixingType and ShortsremixingType not in ShortsremixingTypeOptions:
            self.logger.debug(
                f"you give a invalid ShortsremixingType:{ShortsremixingType} ,try to choose one of them{ShortsremixingTypeOptions},we change it to  default 0"
            )
            ShortsremixingType = 0
        else:
            print(f"ShortsremixingType:{ShortsremixingType}")

        if Category is not None:
            if Category and Category not in CategoryOptions:
                self.logger.debug(
                    f"you give a invalid Category:{Category} ,try to choose one of them{CategoryOptions},we change it to  default None"
                )
                Category = None
            else:
                print(f"Category:{Category}")
        if (
            CommentsRatingsPolicy
            and CommentsRatingsPolicy not in CommentsRatingsPolicyOptions
        ):
            self.logger.debug(
                f"you give a invalid CommentsRatingsPolicy:{CommentsRatingsPolicy} ,try to choose one of them{CommentsRatingsPolicyOptions},we change it to  default 1"
            )
            CommentsRatingsPolicy = 1
        else:
            print(f"CommentsRatingsPolicy:{CommentsRatingsPolicy}")

        # proxy_option = "socks5://127.0.0.1:1080"

        headless = True
        if self.headless:
            headless = False
        else:
            headless = True
        self.logger.debug(f"whether run in view mode:{headless}")

        if self.proxy_option == "":
            self.logger.debug(f"start web page without proxy:{self.proxy_option}")

            with PlaywrightAsyncDriver(
                proxy=None,
                driver_type=self.browserType,
                headless=headless,
                timeout=30,
                use_stealth_js=True,
            ) as pl:
                await pl._setup()
                self.pl = pl

                self._browser = pl.browser
                self.context = pl.context
                self.page = pl.page
            self.logger.debug(
                f"{self.browserType} is now running without proxy:{self.proxy_option}"
            )

        else:
            with PlaywrightAsyncDriver(
                proxy=self.proxy_option,
                driver_type=self.browserType,
                timeout=30,
                headless=headless,
                use_stealth_js=True,
            ) as pl:
                await pl._setup()
                self.pl = pl

                self._browser = pl.browser
                self.context = pl.context
                self.page = pl.page

            self.logger.debug(
                f"{self.browserType} is now running with proxy:{self.proxy_option}"
            )

            # check fakebrowser to bypass captcha and security violations
        await botcheck(pl)

        await self.page.evaluate(
            "document.body.appendChild(Object.assign(document.createElement('script'), {src: 'https://gitcdn.xyz/repo/berstend/puppeteer-extra/stealth-js/stealth.min.js'}))"
        )
        await async_stealth(self.page, pure=True)
        # store the stealth state to reload next time
        # await botcheck(pl)
        await self.page.context.storage_state(
            path="tiktok-stealth-"
            + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            + ".json"
        )

        await self.context.grant_permissions(["geolocation"])
        page = self.page
        print("============tags", tags)
        if not videopath:
            raise FileNotFoundError(f'Could not find file with path: "{videopath}"')

        if self.CHANNEL_COOKIES and not self.CHANNEL_COOKIES == "":
            print("cookies existing", self.CHANNEL_COOKIES)

            await self.context.clear_cookies()
            cookies = await format_cookie_file(self.CHANNEL_COOKIES)
            await self.context.add_cookies(cookies)

            await page.goto(TIKTOK_URL, timeout=300000)

            await page.reload()
        else:
            self.logger.debug("Please sign in and then press enter")
            # input()
            await page.goto(TIKTOK_URL, timeout=300000)
            # Interact with login form

            # await self.context.clear_cookies()
            # await page.locator(".login").click()
            # await page.locator(".semi-button-content").click()
            if self.username and self.password:
                self.logger.debug(
                    "there is no cookie file,but you give account/pass,try to login automatically"
                )
                await tiktok_login(self, self.username, self.password)
            else:
                self.logger.debug(
                    "there is no cookie file ,no  account/pass,we need you manually aiding to login in"
                )
                if self.login_method == "phone-verify":
                    await page.locator("div.semi-tabs-tab:nth-child(2)").click()
                    await page.locator(".toggle").click()
                    time.sleep(60)

                elif self.login_method == "mailpassword":
                    print("not recommend")
                    time.sleep(60)
                    # await page.fill(".semi-input-wrapper__with-prefix", self.username)
                    # await page.fill(
                    #     "div.semi-form-field:nth-child(2)>div>div>input", self.password
                    # )
                    # await page.locaotr(".agreement >img").click()
                    await tiktok_login(self, self.username, self.password)

                elif self.login_method == "qrcode":
                    print("pls open douyin to scan this qrcode")
                    time.sleep(60)

            # page.click('text=Submit')
            sleep(USER_WAITING_TIME)
            storage = await self.context.storage_state(path=self.username + ".json")
            self.logger.debug(
                f'we save cookies for next time reload:{self.username + ".json"}'
            )
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
            await page.goto(TIKTOK_URL, timeout=300000)
            print("start to check login status")

            islogin = confirm_logged_in_douyin(page)

            # https://github.com/xtekky/google-login-bypass/blob/main/login.py

        self.logger.debug("Found douyin upload Dialog Modal")
        await page.goto(DOUYIN_UPLOAD_URL, timeout=300000)
        # sleep(self.timeout)

        self.logger.debug(f'Trying to upload "{videopath}" to douyin...')
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
        #     self.logger.debug(f'found to douyin account check')
        #     x_path = '//*[@id="textbox"]'
        #     if page.locator(x_path):
        #         self.logger.debug(f'fix  douyin account check')
        #         break

        # except:
        # sleep(1)

        self.logger.debug(f'Trying to set "{title}" as title...')

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
            self.logger.debug(f'Trying to set "{thumbnail}" as thumbnail...')
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

        self.logger.debug("Trying to set {location} to ")

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
            self.logger.debug(f'Trying to set "{location}" as location...')

        self.logger.debug("Trying to set {miniprogram} to ")

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

            self.logger.debug(f'Trying to set "{miniprogram}" as mini...')

        self.logger.debug("Trying to set {hottopic} to ")

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
            self.logger.debug(f'Trying to set "{hottopic}" as hottopic...')

            self.logger.debug(f'Trying to set "{hottopic}" as mini...')

        self.logger.debug("Trying to set {heji} to ")

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

            self.logger.debug(f'Trying to set "{heji}" as heji...')

        self.logger.debug("Trying to set {up2toutiao} to ")

        if up2toutiao is None or up2toutiao == False:
            pass
        else:
            await page.locator(".semi-switch-native-control").click()
        self.logger.debug("Trying to set {allow2save} to ")

        if allow2save is None or allow2save == True:
            pass
        else:
            await page.locator(
                ".form--3R0Ka > div:nth-child(14) > div:nth-child(1) > label:nth-child(2)"
            ).click()

        self.logger.debug("Trying to set {allow2see} to ")
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
            self.logger.debug("Trying to set video visibility to 立即发布...")

        else:
            self.logger.debug("Trying to set video visibility to 定时发布...")
            # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
            # mode b:release_offset not exist, publishdate exist , schedule to this specific date
            # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
            # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
            self.logger.debug("Trying to set video schedule time...{publish_date}")
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

    # https://github.com/lonerge/tiktok_youtube_douyin_handling/blob/dd466e7d899dbcf5542d3419bc3ff225ad7b6c69/login.py
    # deal with bot detection
