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
import random
from tsup.utils.webdriver import (
    PlaywrightAsyncDriver,
    InterceptResponse,
    InterceptRequest,
)
import asyncio
from playwright.async_api import Page, expect
from playwright.async_api import Playwright, Browser, BrowserContext


class YoutubeUpload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 200 * 1000,
        is_open_browser: bool = True,
        debug: bool = True,
        username: str = "",
        password: str = "",
        recovery_email: str = "",
        use_stealth_js:bool = False,
        browser_type: Literal["chromium", "firefox", "webkit"] = "firefox",
        # 'chromium', 'firefox', or 'webkit'
        channel_cookie_path: str = "",
        wait_policy: Literal[
            "go next after uploading success",
            "go next after processing success",
            "go next after copyright check success",
        ] = "go next after copyright check success",
        is_record_video: bool = False,
    ) -> None:
        self.timeout = timeout
        self.log = Log(debug)
        self.debug = debug
        self.username = username
        self.password = password
        self.use_stealth_js=use_stealth_js
        self.channel_cookie_path = channel_cookie_path
        self.root_profile_directory = root_profile_directory
        self.proxy_option = proxy_option
        self.is_open_browser = is_open_browser
        self.browser_type = browser_type

        self.pl: Playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.wait_policy = wait_policy
        self.is_record_video = is_record_video

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
        video_local_path: str = "",
        video_title: str = "",
        video_description: str = "",
        thumbnail_local_path: str = "",
        publish_policy: Optional[int] = 0,
        release_date: Optional[datetime] = datetime(
            date.today().year, date.today().month, date.today().day
        ),
        release_date_hour: Optional[str] = "10:15",
        playlist: Optional[str] = None,
        is_age_restriction: Optional[bool] = False,
        is_not_for_kid: Optional[bool] = False,
        is_paid_promotion: Optional[bool] = False,
        is_automatic_chapters: Optional[bool] = True,
        is_featured_place: Optional[bool] = True,
        video_language: Optional[str] = None,
        # input language str and get index in the availableLanguages list
        captions_certification: Optional[int] = 0,
        # parse from video metadata  using ffmpeg
        video_film_date: Optional[str] = None,
        video_film_location: Optional[str] = None,
        license_type: Optional[int] = 0,
        is_allow_embedding: Optional[bool] = True,
        is_publish_to_subscriptions_feed_notify: Optional[bool] = True,
        shorts_remixing_type: Optional[int] = 0,
        categories: Optional[str] = None,
        comments_ratings_policy: Optional[int] = 1,
        is_show_howmany_likes: Optional[bool] = True,
        is_monetization_allowed: Optional[bool] = True,
        tags: list = [],
        first_comment:Optional[str]=None,
        subtitles:Optional[str]=None
    ) -> Tuple[bool, Optional[str]]:
        """Uploads a video to YouTube.
        Returns if the video was uploaded and the video id.
        """
        self.log.debug(f"default wait_policy:{self.wait_policy}")
        video_id = None
        if release_date_hour is None:
            release_date_hour="10:15"
        elif release_date_hour and release_date_hour not in availableScheduleTimes:
            self.log.debug(
                f"you give a invalid release_date_hour:{self.release_date_hour}, ,try to choose one of them{availableScheduleTimes},we change it to  default 10:15"
            )
            release_date_hour = "10:15"
        if (
            self.wait_policy
            and self.wait_policy not in WaitPolicyOptions
        ):
            self.log.debug(
                f"you give a invalid wait_policy:{self.wait_policy}, ,try to choose one of them{WaitPolicyOptions},we change it to  default 2"
            )
            self.wait_policy = "go next after copyright check success"

        if publish_policy and publish_policy not in PublishpolicyOptions:
            self.log.debug(
                f"you give a invalid publish_policy:{publish_policy} ,try to choose one of them{PublishpolicyOptions},0 -private 1-publish 2-schedule 3-Unlisted 4-public&premiere we change it to  default 0"
            )
            publish_policy = 0
        else:
            self.log.debug(f"publish_policy:{publish_policy}")
        if video_language is not None:
            if video_language and video_language not in VideoLanguageOptions:
                self.log.debug(
                    f"you give a invalid video_language:{video_language} ,try to choose one of them{VideoLanguageOptions},we change it to  default None"
                )
                video_language = None
            else:
                self.log.debug(f"video_language:{video_language}")

        if (
            captions_certification
            and captions_certification not in CaptionsCertificationOptions
        ):
            self.log.debug(
                f"you give a invalid publish_policy:{captions_certification} ,try to choose one of them{CaptionsCertificationOptions},we change it to  default 0"
            )
            captions_certification = 0
        else:
            self.log.debug(f"captions_certification:{captions_certification}")

        if license_type and license_type not in LicenceTypeOptions:
            self.log.debug(
                f"you give a invalid license_type:{license_type} ,try to choose one of them{LicenceTypeOptions},we change it to  default 0"
            )
            license_type = 0
        else:
            self.log.debug(f"license_type:{license_type}")

        if shorts_remixing_type and shorts_remixing_type not in ShortsremixingTypeOptions:
            self.log.debug(
                f"you give a invalid shorts_remixing_type:{shorts_remixing_type} ,try to choose one of them{ShortsremixingTypeOptions},we change it to  default 0"
            )
            shorts_remixing_type = 0
        else:
            self.log.debug(f"shorts_remixing_type:{shorts_remixing_type}")

        if categories is not None:
            if categories and categories not in CategoryOptions:
                self.log.debug(
                    f"you give a invalid categories:{categories} ,try to choose one of them{CategoryOptions},we change it to  default None"
                )
                categories = None
            else:
                self.log.debug(f"categories:{categories}")
        if (
            comments_ratings_policy
            and comments_ratings_policy not in CommentsRatingsPolicyOptions
        ):
            self.log.debug(
                f"you give a invalid comments_ratings_policy:{comments_ratings_policy} ,try to choose one of them{CommentsRatingsPolicyOptions},we change it to  default 1"
            )
            comments_ratings_policy = 1
        else:
            self.log.debug(f"comments_ratings_policy:{comments_ratings_policy}")

        # proxy_option = "socks5://127.0.0.1:1080"

        if self.is_open_browser is None:
            self.is_open_browser = True

        self.log.debug(f"whether run in view mode:{self.is_open_browser}")
        if self.proxy_option == "":
            self.log.debug(f"start web page without proxy:{self.proxy_option}")

            pl = await PlaywrightAsyncDriver.create(
                proxy=None,
                driver_type=self.browser_type,
                timeout=3000,
                use_stealth_js=False,
            )
            self.pl = pl
            self.page = pl.page
            self._browser = pl.browser
            self.context = pl.context
            self.log.debug(
                f"{self.browser_type} is now running without proxy:{self.proxy_option}"
            )

        else:
            self.log.debug(f"start web page with proxy:{self.proxy_option}")
            
            pl = await PlaywrightAsyncDriver.create(
                proxy=self.proxy_option,
                driver_type=self.browser_type,
                timeout=3000,
                use_stealth_js=self.use_stealth_js,
                url=YOUTUBE_URL,
            )
            self.pl = pl
            self.page = pl.page

            self._browser = pl.browser
            self.context = pl.context

            self.log.debug(
                f"{self.browser_type} is now running with proxy:{self.proxy_option}"
            )

            # self.page = await self.context.new_page()
            # check fakebrowser to bypass captcha and security violations
            # if self.debug:
            #     await botcheck(self.pl)


        if not video_local_path:
            raise FileNotFoundError(f'Could not find file with path: "{video_local_path}"')

        if not self.channel_cookie_path is None:
            self.log.debug(f"Try to load specified cookie file:{self.channel_cookie_path}")

            if (os.path.exists(self.channel_cookie_path)
                and os.path.getsize(self.channel_cookie_path) > 0
            ):
                self.log.debug(f"cookies existing:{self.channel_cookie_path}")

                await self.context.clear_cookies()

                await self.context.add_cookies(
                    json.load(open(self.channel_cookie_path, "r"))["cookies"]
                )
                self.log.debug(f"cookies file load success:{self.channel_cookie_path}")
               
            else:         
                
                self.log.debug(f"your should provide a valid cookie file:{self.channel_cookie_path} is not found or broken")

                if self.proxy_option:
                    self.log.debug(f'you use proxy:{self.proxy_option}, first run a botcheck')
                    await botcheck(self.pl)
                else:
                    self.log.debug(f'you dont use any proxy {self.proxy_option}')
                # await passwordlogin(self, page)

                login=await youtube_login(self,self.username, self.password)
                if login:
                    self.log.debug('we need save cookie to future usage')
                # save cookie
                else:
                    self.log.debug(
                    "first try for autologin failed,you can mannually sign in to save credentials for later auto login"
                )
                # self.page = await self.context.new_page()

        else:
            self.log.debug('cookie files is not provided')
            await self.page.close()
            return 

            # save cookie to later import
            # login_using_cookie_file(self,self.channel_cookie_path,page)
        await self.page.goto(YoutubeHomePageURL, timeout=self.timeout)

        page = self.page
        islogin = False
        try:
            self.log.debug(f"start checking login status:{islogin}")

            islogin = await confirm_logged_in(self)
            self.log.debug(f"finish checking login status:{islogin}")
        except:
            self.log.debug(f"checking login status failed")

        if not islogin:
            self.log.debug(
                "you can mannually sign in to save credentials for later auto login"
            )
            await passwordlogin(self, page)
            # save cookie to later import
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
        # try:
        #     await expect(
        #         page.get_by_role("button", name="Details", exact=True)
        #     ).to_be_visible()
        # except:
        #     self.log.debug("Details failed to load")
        self.log.debug("Found YouTube upload Dialog Modal")

        self.log.debug(f'Trying to upload "{video_local_path}" to YouTube...')
        if os.path.exists(get_path(video_local_path)):
            page.locator(INPUT_FILE_VIDEO)
            await page.set_input_files(INPUT_FILE_VIDEO, get_path(video_local_path))
            self.log.debug(f'Trying to upload "{get_path(video_local_path)}" to YouTube...')

        else:
            if os.path.exists(video_local_path.encode("utf-8")):
                self.log.debug(f"file found: {video_local_path}")
                page.locator(INPUT_FILE_VIDEO)
                await page.set_input_files(INPUT_FILE_VIDEO, video_local_path.encode("utf-8"))
            self.log.debug(
                f'Trying to upload "{video_local_path.encode("utf-8")}" to YouTube...'
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


        await VerifyDialog(self, page)

        if len(video_title) > TITLE_COUNTER:
            self.log.debug(
                f"Title was not set due to exceeding the maximum allowed characters ({len(video_title)}/{TITLE_COUNTER})"
            )
            video_title = video_title[: TITLE_COUNTER - 1]

            # TITLE
        self.log.debug(f'Trying to set "{video_title}" as title...')
        try:
            await page.locator(TITLE_CONTAINER).is_visible()
            # await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").click().fill(description)

            await page.locator(TITLE_CONTAINER).click()

            self.log.debug("clear existing title")
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(video_title)
            # 很可能就是这个没有确认输入，导致悬浮窗口，无法获取提交按钮
            await page.keyboard.press("Enter")
            self.log.debug("filling new  title")
        except:
            self.log.debug("failed to set title")

        self.log.debug(f'Trying to set "{video_description}" as description...')

        if video_description:
            if len(video_description) > DESCRIPTION_COUNTER:
                self.log.debug(
                    f"Description was not set due to exceeding the maximum allowed characters ({len(video_description)}/{DESCRIPTION_COUNTER})"
                )
                video_description = video_description[:4888]
        try:
            self.log.debug("click description container to input")
            # self.log.debug('1',await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").is_visible())
            # self.log.debug('2',await page.locator("html body#html-body ytcp-uploads-dialog tp-yt-paper-dialog#dialog.style-scope.ytcp-uploads-dialog div.dialog-content.style-scope.ytcp-uploads-dialog ytcp-animatable#scrollable-content.metadata-fade-in-section.style-scope.ytcp-uploads-dialog ytcp-ve.style-scope.ytcp-uploads-dialog ytcp-video-metadata-editor#details.style-scope.ytcp-uploads-dialog div.left-col.style-scope.ytcp-video-metadata-editor ytcp-video-metadata-editor-basics#basics.style-scope.ytcp-video-metadata-editor div#description-container.input-container.description.style-scope.ytcp-video-metadata-editor-basics ytcp-video-description#description-wrapper.style-scope.ytcp-video-metadata-editor-basics div#description-container.input-container.description.style-scope.ytcp-video-description ytcp-social-suggestions-textbox#description-textarea.style-scope.ytcp-video-description ytcp-form-input-container#container.fill-height.style-scope.ytcp-social-suggestions-textbox div#outer.style-scope.ytcp-form-input-container div#child-input.style-scope.ytcp-form-input-container div#container-content.style-scope.ytcp-social-suggestions-textbox ytcp-social-suggestion-input#input.fill-height.style-scope.ytcp-social-suggestions-textbox div#textbox.style-scope.ytcp-social-suggestions-textbox").is_visible())

            await page.locator(DESCRIPTION_CONTAINER).is_visible()
            # await page.get_by_label("Tell viewers about your video (type @ to mention a channel)").click().fill(description)

            await page.locator(DESCRIPTION_CONTAINER).click()

            self.log.debug("clear existing description")
            await page.keyboard.press("Backspace")
            await page.keyboard.press("Control+KeyA")
            await page.keyboard.press("Delete")
            await page.keyboard.type(video_description)
            await page.keyboard.press("Enter")

            self.log.debug("filling new  description")
        except:
            self.log.debug("failed to set description")
        await VerifyDialog(self, page)

        if self.wait_policy in WaitPolicyOptions:
            if self.wait_policy == "go next after uploading success":
                self.log.debug("we choose to skip processing and check steps")
                self.log.debug("start to check whether upload is finished")
                while await self.not_uploaded(page):
                    self.log.debug("Still uploading...")
                    sleep(1)
                self.log.debug("upload is finished")

            elif self.wait_policy == "go next after processing success":
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

                    # force publish_policy to private if there is any copyright issues
                    publish_policy = 0
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
        if thumbnail_local_path:
            self.log.debug(f'Trying to set "{thumbnail_local_path}" as thumbnail...')
            try:
                # await page.get_by_role("button", name="Upload thumbnail").set_input_files(get_path(thumbnail))

                await page.locator(INPUT_FILE_THUMBNAIL).set_input_files(
                    get_path(thumbnail_local_path)
                )
            except:
                if os.path.exists(get_path(thumbnail_local_path)):
                    if await page.get_by_role(
                        "button", name="Upload thumbnail"
                    ).is_visible():
                        await page.get_by_role(
                            "button", name="Upload thumbnail"
                        ).click()

                        await page.get_by_role(
                            "button", name="Upload thumbnail"
                        ).set_input_files(get_path(thumbnail_local_path))

                else:
                    if os.path.exists(thumbnail_local_path.encode("utf-8")):
                        self.log.debug("thumbnail found", thumbnail_local_path)
                        if await page.get_by_role(
                            "button", name="Upload thumbnail"
                        ).is_visible():
                            await page.get_by_role(
                                "button", name="Upload thumbnail"
                            ).click()
                            await page.get_by_role(
                                "button", name="Upload thumbnail"
                            ).set_input_files(thumbnail_local_path.encode("utf-8"))

                    else:
                        self.log.debug(
                            f'you should provide a valid file path: "{thumbnail_local_path}"'
                        )
            self.log.debug(f'finishing to set "{thumbnail_local_path}" as thumbnail...')

        await VerifyDialog(self, page)

        try:
            if playlist:
                self.log.debug(f'Trying to add video to "{playlist}" playlist...')
                await page.locator("#basics").get_by_text("Playlists", exact=True).is_visible()
                await page.locator("#basics").get_by_text("Playlists", exact=True).click()

                await page.locator(".ytcp-video-metadata-playlists tp-yt-iron-icon").click()

                playlists_element = page.locator("tp-yt-iron-list")
                await playlists_element.is_visible()
                if playlist in await playlists_element.inner_html():
                    await page.get_by_text(playlist, exact=True).click()
                    await page.get_by_text("Done", exact=True).click()
                else:
                    await page.keyboard.press("Escape")
                    self.log.debug(f'"{playlist}" playlist not found')
            else:
                self.log.debug("No playlist provided")
        except:
            await page.keyboard.press("Escape")
            self.log.debug("failed to add video to playlist")
            


        self.log.debug('Trying to set video to "Not made for kids"...')

        try:
            if is_not_for_kid:
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
            if is_age_restriction:
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
                self.log.debug("click more get_by_role")
                await page.get_by_role("button", name="Show more").click()
                self.log.debug("click more locator")

        except:
            if await page.locator(MORE_OPTIONS_CONTAINER).is_visible():
                self.log.debug(f" find show more button: {MORE_OPTIONS_CONTAINER}")

                await page.locator(MORE_OPTIONS_CONTAINER).click()

            else:
                self.log.debug("could not find show more button")

        self.log.debug("finish clicking show more button")

        # Paid promotion
        if is_paid_promotion:
            self.log.debug("Trying to set video Paid promotion...")

            await page.get_by_text("Paid promotion", exact=True).is_visible()
            await page.get_by_text("Paid promotion", exact=True).click()
            await page.get_by_role(
                "checkbox",
                name="My video contains paid promotion like a product placement, sponsorship, or endorsement",
            ).click()
            self.log.debug("Trying to set video Paid promotion done")

        if is_automatic_chapters == False:
            self.log.debug("Trying to set video Automatic chapters...")

            await page.get_by_role(
                "checkbox", name="Allow automatic chapters and key moments"
            ).click()

            self.log.debug("Trying to set video Automatic chapters done")
        # Featured places
        if is_featured_place == False:
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
        if video_language is not None:
            await page.get_by_text("Language and captions certification").click()
            await page.locator("#language-input tp-yt-iron-icon").click()

        if captions_certification is not None and not captions_certification == 0:
            if await page.locator(
                "#uncaptioned-reason > ytcp-select:nth-child(1) > ytcp-text-dropdown-trigger:nth-child(1) > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
            ).is_visible():
                await page.locator(
                    "#uncaptioned-reason > ytcp-select:nth-child(1) > ytcp-text-dropdown-trigger:nth-child(1) > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
                ).click()
                await page.get_by_role(
                    "option", name=CaptionsCertificationOptions[captions_certification]
                ).locator("div").nth(1 + int(captions_certification)).click()

        if video_film_date is not None:
            # parse from video metadata  using ffmpeg
            # if none, set to uploading day
            video_film_date = (
                datetime(date.today().year, date.today().month, date.today().day),
            )
            video_film_date = video_film_date.strftime("%b %d, %Y")

            await page.locator("#recorded-date tp-yt-iron-icon").click()
            await page.locator("#input-1").get_by_role("textbox").is_visible()
            await page.locator("#input-1").get_by_role("textbox").fill(
                video_film_date
            )
        if video_film_location is not None:
            await page.get_by_text("Video location").click()
            await page.get_by_placeholder("Search", exact=True).click()
            await page.get_by_placeholder("Search", exact=True).dblclick()
            await page.get_by_placeholder("Search", exact=True).fill(
                video_film_location
            )

        if license_type == 1:
            await page.locator("#license tp-yt-iron-icon").click()
            await page.get_by_text("Creative Commons - Attribution").click()
        if is_allow_embedding == False:
            await page.get_by_role("checkbox", name="Allow embedding").click()
        if is_publish_to_subscriptions_feed_notify == False:
            await page.get_by_role(
                "checkbox", name="Publish to subscriptions feed and notify subscribers"
            ).click()

        if shorts_remixing_type is None:
            shorts_remixing_type = 0
        if shorts_remixing_type == 0:
            pass
        elif shorts_remixing_type == 1:
            await page.get_by_role("radio", name="Allow only audio remixing").click()
        elif shorts_remixing_type == 2:
            await page.get_by_role("radio", name="Don’t allow remixing").click()

        if categories:
            await page.get_by_text("Category", exact=True).click()
            await page.locator("#category tp-yt-iron-icon").click()
            await page.get_by_role("option", name=categories).locator("div").nth(
                1
            ).click()
        if comments_ratings_policy == 0:
            await page.get_by_role("radio", name="Allow all comments").click()

        elif comments_ratings_policy == 1:
            pass
        elif comments_ratings_policy == 2:
            await page.get_by_role("checkbox", name="Increase strictness").click()

        elif comments_ratings_policy == 3:
            await page.get_by_role("radio", name="Hold all comments for review").click()
        elif comments_ratings_policy == 4:
            await page.get_by_role("radio", name="Disable comments").click()
        if is_show_howmany_likes == False:
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
        # if video_language is None:
        #     self.log.debug('you should manually set your video language first to upload default subtitle for default video language')
        # if await page.locator('#subtitles-button > div:nth-child(2)').is_enabled():

        # if there is issue in Copyright check, mandate publish_policy to 0

        if not int(publish_policy) in PublishpolicyOptions:
            publish_policy = 0
        if int(publish_policy) == 0:
            self.log.debug("Trying to set video visibility to private...")

            await page.locator(PRIVATE_RADIO_LABEL).click()
            
        elif int(publish_policy) == 1:
            self.log.debug("Trying to set video visibility to unlisted...")
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).is_visible()
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).click()

            try:
                self.log.debug("Trying to set video visibility to public...")
                try:
                    self.log.debug(
                        f"detect getbyrole public button visible:",
                        await page.get_by_role("radio", name="Public").is_visible(),
                    )

                    # self.log.debug(f'detect public button visible{PUBLIC_BUTTON}:',await page.locator(PUBLIC_BUTTON).is_visible())
                    # self.log.debug(f'detect public button visible:{PUBLIC_RADIO_LABEL}',await page.locator(PUBLIC_RADIO_LABEL).is_visible())
                    await page.get_by_role("radio", name="Public").click()
                    self.log.debug("public radio button clicked")
                    # await page.locator(PUBLIC_BUTTON).click()
                except:
                    self.log.debug("we could not find the public buttton...")

            except:
                pass            
        elif int(publish_policy) == 3:
            self.log.debug("Trying to set video visibility to Unlisted...")
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).is_visible()
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).click()

            try:
                await page.get_by_role("radio", name="Unlisted").click()
                self.log.debug("Unlisted radio button clicked")
                # await page.locator(PUBLIC_BUTTON).click()
                # await page.locator(PUBLIC_BUTTON).click()
            except:
                self.log.debug("we could not find the public buttton...")


            
        elif int(publish_policy) == 4:
            self.log.debug("Trying to set video visibility to public&premiere...")
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).is_visible()
            await page.locator(
                "#first-container > tp-yt-paper-radio-button:nth-child(1)"
            ).click()


            try:
                await page.get_by_role(
                    "checkbox", name="Set as instant Premiere"
                ).is_visible()

                await  page.get_by_role("checkbox", name="Set as instant Premiere").click()

            except:
                self.log.debug(
                    "we could not find the Set as instant Premiere checkbox..."
                        )

        elif int(publish_policy) == 2:
            if release_date is None:
                release_date = datetime(
                    date.today().year, date.today().month, date.today().day
                )
            else:
                release_date = release_date

            if release_date_hour and release_date_hour in availableScheduleTimes:
                release_date_hour = datetime.strptime(release_date_hour, "%H:%M")
                release_date_hour = release_date_hour.strftime("%I:%M %p")
            else:
                self.log.debug(
                    f"your specified schedule time is not supported by youtube yet{release_date_hour}"
                )
                release_date_hour = release_date_hour.strftime("%I:%M %p")

            self.log.debug(
                f"Trying to set video schedule time...{release_date}...{release_date_hour}"
            )

            await setscheduletime(page, release_date, release_date_hour)
        else:
            self.log.debug(f'you should choose a valid publish_policy from {PublishpolicyOptions}')
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
        # self.log.debug(done_button)

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

            if publish_policy == 2:
                self.log.debug(await page.get_by_role("button", name="Schedule").is_visible())

                await page.get_by_role("button", name="Schedule").click()
            else:
                self.log.debug(await page.get_by_role("button", name="Save").is_visible())

                await page.get_by_role("radio", name="Save").click()
            self.log.debug("click done button")
        self.log.debug(f"{video_local_path} is upload process is done")

        sleep(5)
        logging.info("Upload is complete")

        # upload multi-language subtitles and title description
        # https://studio.youtube.com/video/_aaNTRwoJco/translations
        YoutubeSubtitleURL = (
            "https://studio.youtube.com/video/" + video_id + "/translations"
        )

        # submit first comment to drive more traffic for your website
        # firstComment
        # videourl access
        # locator the comment field
        # input 
        # submit and check
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
