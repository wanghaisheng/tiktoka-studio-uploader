import json
from .constants import *
from .logging import Log
from .exceptions import *
from .youtubeHelper import *
import os
from .login import *
from time import sleep
from datetime import datetime, date, timedelta
import logging
import random
from .utils.webdriver import (
    PlaywrightAsyncDriver,
    InterceptResponse,
    InterceptRequest,
)
from playwright.async_api import Page, expect
from cf_clearance import async_cf_retry, async_stealth


class YoutubeUpload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 200 * 1000,
        watcheveryuploadstep: bool = True,
        debug: bool = True,
        username: str = "",
        password: str = "",
        recoveryemail: str = "",
        browserType: str = "firefox",
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
        self.watcheveryuploadstep = watcheveryuploadstep
        self._browser = ""
        self.browserType = browserType
        self.context = ""
        self.page = ""

        self.closewhen100percent = closewhen100percent
        self.recordvideo = recordvideo
        self.pl = ""

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
        isAgeRestriction: Optional[bool] = False,
        isNotForKid: Optional[bool] = False,
        isPaidpromotion: Optional[bool] = False,
        isAutomaticChapters: Optional[bool] = True,
        isFeaturedPlace: Optional[bool] = True,
        VideoLanguage: Optional[str] = None,
        # input language str and get index in the availableLanguages list
        CaptionsCertification: Optional[int] = 0,
        # parse from video metadata  using ffmpeg
        VideoRecordingdate: Optional[str] = None,
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
            self.log.debug(
                f"you give a invalid hour_to_publish:{self.hour_to_publish}, ,try to choose one of them{availableScheduleTimes},we change it to  default 10:15"
            )
            hour_to_publish = "10:15"
        if (
            self.closewhen100percent
            and self.closewhen100percent not in closewhen100percentOptions
        ):
            self.log.debug(
                f"you give a invalid closewhen100percent:{self.closewhen100percent}, ,try to choose one of them{closewhen100percentOptions},we change it to  default 2"
            )
            self.closewhen100percent = 2

        if publishpolicy and publishpolicy not in PublishpolicyOptions:
            self.log.debug(
                f"you give a invalid publishpolicy:{publishpolicy} ,try to choose one of them{PublishpolicyOptions},we change it to  default 0"
            )
            publishpolicy = 0
        else:
            print(f"publishpolicy:{publishpolicy}")
        if VideoLanguage is not None:
            if VideoLanguage and VideoLanguage not in VideoLanguageOptions:
                self.log.debug(
                    f"you give a invalid VideoLanguage:{VideoLanguage} ,try to choose one of them{VideoLanguageOptions},we change it to  default None"
                )
                VideoLanguage = None
            else:
                print(f"VideoLanguage:{VideoLanguage}")

        if (
            CaptionsCertification
            and CaptionsCertification not in CaptionsCertificationOptions
        ):
            self.log.debug(
                f"you give a invalid publishpolicy:{CaptionsCertification} ,try to choose one of them{CaptionsCertificationOptions},we change it to  default 0"
            )
            CaptionsCertification = 0
        else:
            print(f"CaptionsCertification:{CaptionsCertification}")

        if LicenceType and LicenceType not in LicenceTypeOptions:
            self.log.debug(
                f"you give a invalid LicenceType:{LicenceType} ,try to choose one of them{LicenceTypeOptions},we change it to  default 0"
            )
            LicenceType = 0
        else:
            print(f"LicenceType:{LicenceType}")

        if ShortsremixingType and ShortsremixingType not in ShortsremixingTypeOptions:
            self.log.debug(
                f"you give a invalid ShortsremixingType:{ShortsremixingType} ,try to choose one of them{ShortsremixingTypeOptions},we change it to  default 0"
            )
            ShortsremixingType = 0
        else:
            print(f"ShortsremixingType:{ShortsremixingType}")

        if Category is not None:
            if Category and Category not in CategoryOptions:
                self.log.debug(
                    f"you give a invalid Category:{Category} ,try to choose one of them{CategoryOptions},we change it to  default None"
                )
                Category = None
            else:
                print(f"Category:{Category}")
        if (
            CommentsRatingsPolicy
            and CommentsRatingsPolicy not in CommentsRatingsPolicyOptions
        ):
            self.log.debug(
                f"you give a invalid CommentsRatingsPolicy:{CommentsRatingsPolicy} ,try to choose one of them{CommentsRatingsPolicyOptions},we change it to  default 1"
            )
            CommentsRatingsPolicy = 1
        else:
            print(f"CommentsRatingsPolicy:{CommentsRatingsPolicy}")

        # proxy_option = "socks5://127.0.0.1:1080"

        headless = True
        if self.watcheveryuploadstep:
            headless = False
        self.log.debug(f"whether run in view mode:{headless}")

        if self.proxy_option == "":
            self.log.debug(f"start web page without proxy:{self.proxy_option}")

            with PlaywrightAsyncDriver(
                proxy=None,
                driver_type=self.browserType,
                timeout=30,
                use_stealth_js=True,
            ) as pl:
                await pl._setup()
                self.pl = pl

                self._browser = pl.browser
                self.context = pl.context
                self.page = pl.page
            self.log.debug(
                f"{self.browserType} is now running without proxy:{self.proxy_option}"
            )

        else:
            with PlaywrightAsyncDriver(
                proxy=self.proxy_option,
                driver_type=self.browserType,
                timeout=30,
                use_stealth_js=True,
            ) as pl:
                await pl._setup()
                self.pl = pl

                self._browser = pl.browser
                self.context = pl.context
                self.page = pl.page

            self.log.debug(
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
            path="stealth-" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".json"
        )
        if not videopath:
            raise FileNotFoundError(f'Could not find file with path: "{videopath}"')

        try:
            if (
                self.CHANNEL_COOKIES
                and not self.CHANNEL_COOKIES == ""
                and os.path.exists(self.CHANNEL_COOKIES)
                and os.path.getsize(self.CHANNEL_COOKIES) > 0
            ):
                self.log.debug(f"cookies existing:{self.CHANNEL_COOKIES}")

                await self.context.clear_cookies()

                await self.context.add_cookies(
                    json.load(open(self.CHANNEL_COOKIES, "r"))["cookies"]
                )

                # self.page = await self.context.new_page()

        except:
            print("your should provide a valid cookie file")

            # login_using_cookie_file(self,self.CHANNEL_COOKIES,page)
        await self.page.goto(YoutubeHomePageURL, timeout=self.timeout)

        page = self.page
        islogin = confirm_logged_in(self)
        self.log.debug(f"checking login status:{islogin}")

        if not islogin:
            self.log.debug(
                "you can mannually sign in to save credentials for later auto login"
            )
            passwordlogin(self, page)
            await page.goto(YoutubeHomePageURL, timeout=self.timeout)
            self.log.debug("start to check login status")

            islogin = confirm_logged_in(self)

            # https://github.com/xtekky/google-login-bypass/blob/main/login.py

        self.log.debug("check whether  home page is English")
        await set_channel_language_english(self, page)
        self.log.debug("go to youtube studio home page")
        try:
            await page.goto(YOUTUBE_STUDIO_URL, timeout=self.timeout)
        except:
            self.log.debug(
                "failed to youtube studio home page due to network issue,pls check your speed"
            )

        self.log.debug("double check youtube studio home page display language")

        if not await page.get_by_role("heading", name="Channel dashboard").is_visible():
            # page.locator('.page-title').text_content()=='Channel content':
            self.log.debug(
                "It seems studio home page is not English,start change locale to english again"
            )
            await set_channel_language_english(self, page)
            self.log.debug("finish change locale to English")
        else:
            self.log.debug("your dashborad is in English")

        try:
            await page.goto(YOUTUBE_UPLOAD_URL, timeout=self.timeout)
        except:
            self.log.debug(
                f"failed to load youtube studio upload page:{YOUTUBE_UPLOAD_URL} due to network issue,pls check your speed"
            )

        await expect(
            page.get_by_role("button", name="Details", exact=True)
        ).to_be_visible()

        self.log.debug("Found YouTube upload Dialog Modal")

        self.log.debug(f'Trying to upload "{videopath}" to YouTube...')
        if os.path.exists(get_path(videopath)):
            page.locator(INPUT_FILE_VIDEO)
            await page.set_input_files(INPUT_FILE_VIDEO, get_path(videopath))
            self.log.debug(f'Trying to upload "{get_path(videopath)}" to YouTube...')

        else:
            if os.path.exists(videopath.encode("utf-8")):
                self.log.debug(f"file found: {videopath}")
                page.locator(INPUT_FILE_VIDEO)
                await page.set_input_files(INPUT_FILE_VIDEO, videopath.encode("utf-8"))
            self.log.debug(
                f'Trying to upload "{videopath.encode("utf-8")}" to YouTube...'
            )

        #     <h1 slot="primary-header" id="dialog-title" class="style-scope ytcp-confirmation-dialog">
        #   Verify it's you
        # </h1>

        await VerifyDialog(self, page)

        try:
            self.log.debug(f"Trying to detect daily upload limit...")
            hint = (
                await page.locator("#error-short style-scope ytcp-uploads-dialog")
                .waitfor()
                .text_content()
            )
            if "Daily upload limit reached" in hint:
                self.log.debug(f"you have reached daily upload limit pls try tomorrow")

                self.close()

            else:
                pass
        except:
            self.log.debug(f"Finishing detect daily upload limit...")

        # random case of you are currently sign out ,please sigin
        # to be fixed

        # detect video id during uploading done in the title description page
        # .row

        self.log.debug(f'Trying to set "{title}" as title...')

        await VerifyDialog(self, page)

        if len(title) > TITLE_COUNTER:
            self.log.debug(
                f"Title was not set due to exceeding the maximum allowed characters ({len(title)}/{TITLE_COUNTER})"
            )
            title = title[: TITLE_COUNTER - 1]

            # TITLE
        self.log.debug(f'Trying to set "{title}" as title...')
        try:
            await page.locator(TITLE_CONTAINER).is_visible()
            # await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").click().fill(description)

            await page.locator(TITLE_CONTAINER).click()

            self.log.debug("clear existing title")
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(title)
            # 很可能就是这个没有确认输入，导致悬浮窗口，无法获取提交按钮
            await page.keyboard.press("Enter")
            self.log.debug("filling new  title")
        except:
            self.log.debug("failed to set title")

        self.log.debug(f'Trying to set "{description}" as description...')

        if description:
            if len(description) > DESCRIPTION_COUNTER:
                self.log.debug(
                    f"Description was not set due to exceeding the maximum allowed characters ({len(description)}/{DESCRIPTION_COUNTER})"
                )
                description = description[:4888]
        try:
            self.log.debug("click description container to input")
            # print('1',await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").is_visible())
            # print('2',await page.locator("html body#html-body ytcp-uploads-dialog tp-yt-paper-dialog#dialog.style-scope.ytcp-uploads-dialog div.dialog-content.style-scope.ytcp-uploads-dialog ytcp-animatable#scrollable-content.metadata-fade-in-section.style-scope.ytcp-uploads-dialog ytcp-ve.style-scope.ytcp-uploads-dialog ytcp-video-metadata-editor#details.style-scope.ytcp-uploads-dialog div.left-col.style-scope.ytcp-video-metadata-editor ytcp-video-metadata-editor-basics#basics.style-scope.ytcp-video-metadata-editor div#description-container.input-container.description.style-scope.ytcp-video-metadata-editor-basics ytcp-video-description#description-wrapper.style-scope.ytcp-video-metadata-editor-basics div#description-container.input-container.description.style-scope.ytcp-video-description ytcp-social-suggestions-textbox#description-textarea.style-scope.ytcp-video-description ytcp-form-input-container#container.fill-height.style-scope.ytcp-social-suggestions-textbox div#outer.style-scope.ytcp-form-input-container div#child-input.style-scope.ytcp-form-input-container div#container-content.style-scope.ytcp-social-suggestions-textbox ytcp-social-suggestion-input#input.fill-height.style-scope.ytcp-social-suggestions-textbox div#textbox.style-scope.ytcp-social-suggestions-textbox").is_visible())

            await page.locator(DESCRIPTION_CONTAINER).is_visible()
            # await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").click().fill(description)

            await page.locator(DESCRIPTION_CONTAINER).click()

            self.log.debug("clear existing description")
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(description)
            await page.keyboard.press("Enter")

            self.log.debug("filling new  description")
        except:
            self.log.debug("failed to set description")
        await VerifyDialog(self, page)

        if self.closewhen100percent in [0, 1, 2]:
            if self.closewhen100percent == 0:
                self.log.debug("we choose to skip processing and check steps")
                self.log.debug("start to check whether upload is finished")
                while await self.not_uploaded(page):
                    self.log.debug("Still uploading...")
                    sleep(1)
                self.log.debug("upload is finished")

            elif self.closewhen100percent == 1:
                self.log.debug("start to check whether upload is finished")
                while await self.not_uploaded(page):
                    self.log.debug("Still uploading...")
                    sleep(1)
                self.log.debug("uploading is finished")

                self.log.debug("start to check whether process is finished")
                while await self.not_processed(page):
                    self.log.debug("Still processing...")
                    sleep(1)
                self.log.debug("processing is finished")

            else:
                self.log.debug("we choose to wait after copyright check steps")
                self.log.debug("start to check whether upload is finished")
                while await self.not_uploaded(page):
                    self.log.debug("Still uploading...")
                    sleep(1)
                self.log.debug("start to check whether process is finished")
                while await self.not_processed(page):
                    self.log.debug("Still processing...")
                    sleep(1)
                self.log.debug("finished to check whether process is finished")

                self.log.debug("start to check whether check is finished")
                while await self.not_copyrightchecked(page):
                    self.log.debug("Still checking...")
                    sleep(1)
                self.log.debug("copyright checking is finished")
                self.log.debug("start to check whether copyright issue exist")
                s = await page.locator(STATUS_CONTAINER).text_content()
                if not "Checks complete. No issues found" in s:
                    self.log.debug("copyright issue exist")

                    # force publishpolicy to private if there is any copyright issues
                    publishpolicy = 0
                else:
                    self.log.debug("There is no copyright issue exist")
        # get video id
        try:
            self.log.debug(f"Trying to get videoid...")

            if await page.locator("a.ytcp-video-info").is_visible():
                video_id = await page.locator("a.ytcp-video-info").get_attribute("href")
                video_id = video_id.split("/")[-1]
                self.log.debug(f" get videoid in uploading page:{video_id}")

        except:
            self.log.debug(
                f"can not identify video id in the upload detail page,try to grab in schedule page"
            )
        if thumbnail:
            self.log.debug(f'Trying to set "{thumbnail}" as thumbnail...')
            try:
                # await page.get_by_role("button", name="Upload thumbnail").set_input_files(get_path(thumbnail))

                await page.locator(INPUT_FILE_THUMBNAIL).set_input_files(
                    get_path(thumbnail)
                )
            except:
                if os.path.exists(get_path(thumbnail)):
                    if await page.get_by_role(
                        "button", name="Upload thumbnail"
                    ).is_visible():
                        await page.get_by_role(
                            "button", name="Upload thumbnail"
                        ).click()

                        await page.get_by_role(
                            "button", name="Upload thumbnail"
                        ).set_input_files(get_path(thumbnail))

                else:
                    if os.path.exists(thumbnail.encode("utf-8")):
                        self.log.debug("thumbnail found", thumbnail)
                        if await page.get_by_role(
                            "button", name="Upload thumbnail"
                        ).is_visible():
                            await page.get_by_role(
                                "button", name="Upload thumbnail"
                            ).click()
                            await page.get_by_role(
                                "button", name="Upload thumbnail"
                            ).set_input_files(thumbnail.encode("utf-8"))

                    else:
                        self.log.debug(
                            f'you should provide a valid file path: "{thumbnail}"'
                        )
            self.log.debug(f'finishing to set "{thumbnail}" as thumbnail...')

        await VerifyDialog(self, page)
        self.log.debug('Trying to set video to "Not made for kids"...')

        try:
            if isNotForKid:
                await page.get_by_role(
                    "radio",
                    name="Yes, it's made for kids . Features like personalized ads and notifications won’t be available on videos made for kids. Videos that are set as made for kids by you are more likely to be recommended alongside other kids’ videos. Learn more",
                ).click()

            else:
                self.log.debug("keep the default setting:No, its not made for kids")
                await page.get_by_role(
                    "radio", name="No, it's not made for kids"
                ).click()

                # if await page.locator(NOT_MADE_FOR_KIDS_LABEL).is_visible():
                #     await page.locator(NOT_MADE_FOR_KIDS_RADIO_LABEL).click()
                self.log.debug("not made for kids task done")
        except:
            self.log.debug("failed to set not made for kids")

        self.log.debug("Trying to set video AgeRestriction...")

        try:
            if isAgeRestriction:
                await page.get_by_role(
                    "radio", name="Yes, restrict my video to viewers over 18"
                ).click()
            else:
                # keep the default

                self.log.debug(
                    "keep the default setting:No, dont restrict my video to viewers over 18 only"
                )
        except:
            self.log.debug("failed to set not made for kids")

        # show more to set Paid promotion,Automatic chapters,Featured places,Language and captions certification,
        #  Recording date and location,License, Shorts remixing ,Comments and ratings,Category

        self.log.debug("click show more button")
        try:
            self.log.debug(f" find show more button get_by_role")

            if await page.get_by_role("button", name="Show more").is_visible():
                print("click more get_by_role")
                await page.get_by_role("button", name="Show more").click()
                print("click more locator")

        except:
            if await page.locator(MORE_OPTIONS_CONTAINER).is_visible():
                self.log.debug(f" find show more button: {MORE_OPTIONS_CONTAINER}")

                await page.locator(MORE_OPTIONS_CONTAINER).click()

            else:
                self.log.debug("could not find show more button")

        self.log.debug("finish clicking show more button")

        # Paid promotion
        if isPaidpromotion:
            self.log.debug("Trying to set video Paid promotion...")

            await page.get_by_text("Paid promotion", exact=True).is_visible()
            await page.get_by_text("Paid promotion", exact=True).click()
            await page.get_by_role(
                "checkbox",
                name="My video contains paid promotion like a product placement, sponsorship, or endorsement",
            ).click()
            self.log.debug("Trying to set video Paid promotion done")

        if isAutomaticChapters == False:
            self.log.debug("Trying to set video Automatic chapters...")

            await page.get_by_role(
                "checkbox", name="Allow automatic chapters and key moments"
            ).click()

            self.log.debug("Trying to set video Automatic chapters done")
        # Featured places
        if isFeaturedPlace == False:
            self.log.debug("Trying to set video Featured places...")

            await page.get_by_text("Featured places").click()
            await page.get_by_role("checkbox", name="Allow automatic places").click()
            self.log.debug("Trying to set video Featured places done")
        if tags is None or tags == "" or len(tags) == 0:
            pass
        else:
            self.log.debug(f"tags you give:{tags}")
            if type(tags) == list:
                tags = ",".join(str(tag) for tag in tags)
                tags = tags[:500]
            else:
                tags = tags
            self.log.debug("overwrite prefined channel tags")
            if len(tags) > TAGS_COUNTER:
                self.log.debug(
                    f"Tags were not set due to exceeding the maximum allowed characters ({len(tags)}/{TAGS_COUNTER})"
                )
                tags = tags[:TAGS_COUNTER]
            self.log.debug(f'Trying to set "{tags}" as tags...')

            try:
                # await page.locator(TAGS_CONTAINER).locator(TEXT_INPUT).click()
                await page.get_by_text("Tags", exact=True).click()
                await page.get_by_placeholder("Add tag").click()
                # await page.get_by_placeholder("Add tag").fill("babala,")
                await page.get_by_label("Tags").click()

                self.log.debug("clear existing tags")
                await page.keyboard.press("Backspace")
                await page.keyboard.press("Control+KeyA")
                await page.keyboard.press("Delete")
                await page.get_by_label("Tags").fill(tags)
                self.log.debug("finishing set   tags")
            except:
                self.log.debug("failed to set tags")

        # input language str and get index in the availableLanguages list
        if VideoLanguage is not None:
            await page.get_by_text("Language and captions certification").click()
            await page.locator("#language-input tp-yt-iron-icon").click()

        if CaptionsCertification is not None and not CaptionsCertification == 0:
            if await page.locator(
                "#uncaptioned-reason > ytcp-select:nth-child(1) > ytcp-text-dropdown-trigger:nth-child(1) > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
            ).is_visible():
                await page.locator(
                    "#uncaptioned-reason > ytcp-select:nth-child(1) > ytcp-text-dropdown-trigger:nth-child(1) > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
                ).click()
                await page.get_by_role(
                    "option", name=CaptionsCertificationOptions[CaptionsCertification]
                ).locator("div").nth(1 + int(CaptionsCertification)).click()

        if VideoRecordingdate is not None:
            # parse from video metadata  using ffmpeg
            # if none, set to uploading day
            VideoRecordingdate = (
                datetime(date.today().year, date.today().month, date.today().day),
            )
            VideoRecordingdate = VideoRecordingdate.strftime("%b %d, %Y")

            await page.locator("#recorded-date tp-yt-iron-icon").click()
            await page.locator("#input-1").get_by_role("textbox").is_visible()
            await page.locator("#input-1").get_by_role("textbox").fill(
                VideoRecordingdate
            )
        if VideoRecordinglocation is not None:
            await page.get_by_text("Video location").click()
            await page.get_by_placeholder("Search", exact=True).click()
            await page.get_by_placeholder("Search", exact=True).dblclick()
            await page.get_by_placeholder("Search", exact=True).fill(
                VideoRecordinglocation
            )

        if LicenceType == 1:
            await page.locator("#license tp-yt-iron-icon").click()
            await page.get_by_text("Creative Commons - Attribution").click()
        if isAllowEmbedding == False:
            await page.get_by_role("checkbox", name="Allow embedding").click()
        if isPublishToSubscriptionsFeedNotify == False:
            await page.get_by_role(
                "checkbox", name="Publish to subscriptions feed and notify subscribers"
            ).click()

        if ShortsremixingType is None:
            ShortsremixingType = 0
        if ShortsremixingType == 0:
            pass
        elif ShortsremixingType == 1:
            await page.get_by_role("radio", name="Allow only audio remixing").click()
        elif ShortsremixingType == 2:
            await page.get_by_role("radio", name="Don’t allow remixing").click()

        if Category:
            await page.get_by_text("Category", exact=True).click()
            await page.locator("#category tp-yt-iron-icon").click()
            await page.get_by_role("option", name=Category).locator("div").nth(
                1
            ).click()
        if CommentsRatingsPolicy == 0:
            await page.get_by_role("radio", name="Allow all comments").click()

        elif CommentsRatingsPolicy == 1:
            pass
        elif CommentsRatingsPolicy == 2:
            await page.get_by_role("checkbox", name="Increase strictness").click()

        elif CommentsRatingsPolicy == 3:
            await page.get_by_role("radio", name="Hold all comments for review").click()
        elif CommentsRatingsPolicy == 4:
            await page.get_by_role("radio", name="Disable comments").click()
        if isShowHowManyLikes == False:
            await page.get_by_role(
                "radio", name="Show how many viewers like this video"
            ).click()

        # sometimes you have 4 tabs instead of 3
        # this handles both cases
        for _ in range(3):
            try:
                await self.click_next(page)
                self.log.debug("next next!")
            except:
                pass
        #
        # if VideoLanguage is None:
        #     print('you should manually set your video language first to upload default subtitle for default video language')
        # if await page.locator('#subtitles-button > div:nth-child(2)').is_enabled():

        # if there is issue in Copyright check, mandate publishpolicy to 0

        if not int(publishpolicy) in PublishpolicyOptions:
            publishpolicy = 0
        if int(publishpolicy) == 0:
            self.log.debug("Trying to set video visibility to private...")

            await page.locator(PRIVATE_RADIO_LABEL).click()
        elif int(publishpolicy) == 1:
            self.log.debug("Trying to set video visibility to public...")
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).is_visible()
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).click()

            publish = "public"
            try:
                if publish == "unlisted":
                    print(
                        f"detect getbyrole unlisted button visible:",
                        await page.get_by_role("radio", name="Public").is_visible(),
                    )

                    # print(f'detect public button visible{PUBLIC_BUTTON}:',await page.locator(PUBLIC_BUTTON).is_visible())
                    # print(f'detect public button visible:{PUBLIC_RADIO_LABEL}',await page.locator(PUBLIC_RADIO_LABEL).is_visible())
                    await page.get_by_role("radio", name="Unlisted").click()
                    print("Unlisted radio button clicked")
                    # await page.locator(PUBLIC_BUTTON).click()
                elif publish == "public":
                    print("switch case to public")
                    try:
                        print(
                            f"detect getbyrole public button visible:",
                            await page.get_by_role("radio", name="Public").is_visible(),
                        )

                        # print(f'detect public button visible{PUBLIC_BUTTON}:',await page.locator(PUBLIC_BUTTON).is_visible())
                        # print(f'detect public button visible:{PUBLIC_RADIO_LABEL}',await page.locator(PUBLIC_RADIO_LABEL).is_visible())
                        await page.get_by_role("radio", name="Public").click()
                        print("public radio button clicked")
                        # await page.locator(PUBLIC_BUTTON).click()
                    except:
                        self.log.debug("we could not find the public buttton...")

                elif publish == "public&premiere":
                    try:
                        print(
                            f"detect getbyrole public button visible:",
                            await page.get_by_role("radio", name="Public").is_visible(),
                        )
                        await page.get_by_role("radio", name="Public").click()
                        print("public radio button clicked")
                    except:
                        self.log.debug("we could not find the public buttton...")
                    try:
                        await page.get_by_role(
                            "checkbox", name="Set as instant Premiere"
                        ).is_visible()
                        await page.get_by_role(
                            "checkbox", name="Set as instant Premiere"
                        ).click()

                    except:
                        self.log.debug(
                            "we could not find the Set as instant Premiere checkbox..."
                        )

            except:
                pass

        else:
            if date_to_publish is None:
                date_to_publish = datetime(
                    date.today().year, date.today().month, date.today().day
                )
            else:
                date_to_publish = date_to_publish

            if hour_to_publish and hour_to_publish in availableScheduleTimes:
                hour_to_publish = datetime.strptime(hour_to_publish, "%H:%M")
                hour_to_publish = hour_to_publish.strftime("%I:%M %p")
            else:
                self.log.debug(
                    f"your specified schedule time is not supported by youtube yet{hour_to_publish}"
                )
                hour_to_publish = "10:15"
                hour_to_publish = hour_to_publish.strftime("%I:%M %p")

            self.log.debug(
                f"Trying to set video schedule time...{date_to_publish}...{hour_to_publish}"
            )

            await setscheduletime(page, date_to_publish, hour_to_publish)
        self.log.debug("publish setting task done")

        if video_id is None:
            self.log.debug("start to grab video id  in schedule page")

            video_id = await self.get_video_id(page)
            self.log.debug(f"finish to grab video id in schedule page:{video_id}")
        # await page.click('#save-button')
        # done-button > div:nth-child(2)
        self.log.debug("trying to click done button")

        # await expect(page.get_by_role("button", name="Schedule")).to_be_visible()
        # done_button = page.get_by_role("button", name="Schedule")
        # await page.get_by_role("button", name="Schedule").click()

        # await expect(page.locator(DONE_BUTTON_CSS_SELECTOR)).to_be_visible()
        # done_button = page.locator(DONE_BUTTON_CSS_SELECTOR)
        # print(done_button)

        # if await done_button.get_attribute("aria-disabled") == "true":
        #     error_message = await page.locator(ERROR_CONTAINER).text_content()
        #     return False, error_message

        # await done_button.click()
        # if await done_button.get_attribute("aria-disabled") == "false":
        #     await done_button.click()

        try:
            # done-button

            if await page.locator('//*[@id="done-button"]').is_visible():
                await page.locator('//*[@id="done-button"]').click()

        except:
            self.log.debug("Failed to locate done button")

            if publishpolicy == 2:
                print(await page.get_by_role("button", name="Schedule").is_visible())

                await page.get_by_role("button", name="Schedule").click()
            else:
                print(await page.get_by_role("button", name="Save").is_visible())

                await page.get_by_role("radio", name="Save").click()
            print("click done button")
        self.log.debug(f"{videopath} is upload process is done")

        sleep(5)
        logging.info("Upload is complete")

        # upload multi-language subtitles and title description
        # https://studio.youtube.com/video/_aaNTRwoJco/translations
        YoutubeSubtitleURL = (
            "https://studio.youtube.com/video/" + video_id + "/translations"
        )

        await self.pl.quit()
        # page.locator("#close-icon-button > tp-yt-iron-icon:nth-child(1)").click()
        # self.log.debug(page.expect_popup().locator("#html-body > ytcp-uploads-still-processing-dialog:nth-child(39)"))
        # page.wait_for_selector("ytcp-dialog.ytcp-uploads-still-processing-dialog > tp-yt-paper-dialog:nth-child(1)")
        # page.locator("ytcp-button.ytcp-uploads-still-processing-dialog > div:nth-child(2)").click()
        return True, video_id

    async def get_video_id(self, page) -> Optional[str]:
        video_id = None
        try:
            video_url_container = page.locator(VIDEO_URL_CONTAINER)
            video_url_element = video_url_container.locator(VIDEO_URL_ELEMENT)

            video_id = await video_url_element.get_attribute(HREF)
            video_id = video_id.split("/")[-1]
        except:
            raise VideoIDError("Could not get video ID")

        return video_id
