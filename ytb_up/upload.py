import json
from tkinter import EXCEPTION
from .constants import *
from .logging import Log
from .exceptions import *
from .utils import *
import os
from .login import *
from time import sleep
from datetime import datetime, date,timedelta
import logging
import re
from playwright.sync_api import *




class Upload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 3,
        headless: bool = True,
        debug: bool = True,
        username:str ="",
        password:str ="",
        CHANNEL_COOKIES: str = "",
        ytb_cookies:str="",
        tiktok_cookies:str="",

    ) -> None:
        self._playwright = self._start_playwright()
            #     browser = p.chromium.launch()

        PROXY_SOCKS5 = "socks5://127.0.0.1:1080"

        if not headless:
            headless = True
        if proxy_option == "":
            print('start web page without proxy')

            browserLaunchOptionDict = {
                "headless": headless,
                # "executable_path": executable_path,
                "timeout": 30000
            }

            if not root_profile_directory:
                self.browser = self._start_browser("firefox", **browserLaunchOptionDict)
            else:
                self.browser = self._start_persistent_browser(
                    "firefox", user_data_dir=root_profile_directory, **browserLaunchOptionDict
                )
        # Open new page
            self.context = self.browser.new_context()
        else:
            print('start web page with proxy')

            browserLaunchOptionDict = {
                "headless": False,
                "proxy": {
                    "server": PROXY_SOCKS5,
                },

                # timeout <float> Maximum time in milliseconds to wait for the browser instance to start. Defaults to 30000 (30 seconds). Pass 0 to disable timeout.#
                "timeout": 30000
            }

            if not root_profile_directory:
                self.browser = self._start_browser("firefox", **browserLaunchOptionDict)
            else:
                self.browser = self._start_persistent_browser(
                    "firefox", user_data_dir=root_profile_directory, **browserLaunchOptionDict
                )
        # Open new page
            self.context = self.browser.new_context()
        self.timeout = timeout
        self.log = Log(debug)
        self.username=username
        self.password=password
        self.CHANNEL_COOKIES = CHANNEL_COOKIES
        self.log.debug("Firefox is now running")

    def click(self, elementSelector):
        element.click()
        sleep(self.timeout)
        return element

    def send(self, element, text: str) -> None:
        element.clear()
        sleep(self.timeout)
        element.send_keys(text)
        sleep(self.timeout)

    def click_next(self, page) -> None:
        page.locator(NEXT_BUTTON).click()
        sleep(self.timeout)

    def not_uploaded(self, page) -> bool:
        return page.locator(STATUS_CONTAINER).text_content().find(UPLOADED) != -1

    def upload(
        self,
        file: str,
        title: str = "",
        description: str = "",
        thumbnail: str = "",
        publishpolicy: str = 0,
        # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow
        release_offset: str = '0-1',
        publish_date: datetime = datetime(
            date.today().year,  date.today().month,  date.today().day, 10, 15),
        tags: list = [],
        process100:int =0
    ) -> Tuple[bool, Optional[str]]:
        """Uploads a video to YouTube.
        Returns if the video was uploaded and the video id.
        """
        page = self.context.new_page()
        print('============tags',tags)
        if not file:
            raise FileNotFoundError(f'Could not find file with path: "{file}"')


        if self.CHANNEL_COOKIES and not self.CHANNEL_COOKIES == '':
            print('cookies existing', self.CHANNEL_COOKIES)

            self.context.clear_cookies()

            self.context.add_cookies(
                json.load(
                    open(
                        self.CHANNEL_COOKIES, 
                        'r'
                    )
                )
            )            
            # login_using_cookie_file(self,self.CHANNEL_COOKIES,page)         
            page.goto(YOUTUBE_URL)

            page.reload()
        else:
            self.log.info('Please sign in and then press enter')
            # input()

            page.goto(YOUTUBE_URL)
            # Interact with login form
            browser_context = self.browser.new_context(
                ignore_https_errors=True)
            browser_context.clear_cookies()
            # page.click('text=Login')
            # page.fill('input[name="login"]', USERNAME)
            # page.fill('input[name="password"]', PASSWORD)
            # page.click('text=Submit')
            sleep(USER_WAITING_TIME)
            storage = browser_context.storage_state(path=self.CHANNEL_COOKIES)
            self.context = browser_context

        islogin = confirm_logged_in(page)
        print('checking login status', islogin)

        if not islogin:
            print('try to load cookie files')
            self.context.clear_cookies()

            self.context.add_cookies(
                json.load(
                    open(
                        self.CHANNEL_COOKIES, 
                        'r'
                    )
                )
            )            

            print('success load cookie files')
            page.get(YOUTUBE_URL)
            print('start to check login status')

            islogin = confirm_logged_in(page)

        print('start change locale to english')

        set_channel_language_english(page)
        print('finish change locale to english')
        page.goto(YOUTUBE_UPLOAD_URL)
        # sleep(self.timeout)
        self.log.debug("Found YouTube upload Dialog Modal")

        self.log.debug(f'Trying to upload "{file}" to YouTube...')
        if os.path.exists(get_path(file)):
            page.locator(
                INPUT_FILE_VIDEO)
            page.set_input_files(INPUT_FILE_VIDEO, get_path(file))
        else:
            if os.path.exists(file.encode('utf-8')):
                print('file found', file)
                page.locator(
                    INPUT_FILE_VIDEO)
                page.set_input_files(INPUT_FILE_VIDEO, file.encode('utf-8'))
        sleep(self.timeout)
        if not page.locator(TEXTBOX).is_editable:
            self.log.debug(f'found to YouTube account check')

            try:
                page.locator(CONFIRM_CONTAINER).is_visible()
                print('try to input credentials')
                verify(self,page)
                page.goto(YOUTUBE_UPLOAD_URL)
            except:
                print('there is no verify')
        #confirm-button > div:nth-child(2)
        # # Catch max uploads/day limit errors
        # if page.get_attribute(NEXT_BUTTON, 'hidden') == 'true':
        #     error_short_by_xpath=page.locator(ERROR_SHORT_XPATH)
        #     # print(f"ERROR: {error_short_by_xpath.text} {self.cookie_working_dir}")
        #     return False

        self.log.debug(f'Trying to set "{title}" as title...')


        # get file name (default) title
        # title=title if title else page.locator(TEXTBOX).text_content()
        # print(title)
        sleep(self.timeout)
        if len(title) > TITLE_COUNTER:
            print(f"Title was not set due to exceeding the maximum allowed characters ({len(title)}/{TITLE_COUNTER})")
            title=title[:TITLE_COUNTER-1]

                # TITLE
        print('click title field to input')
        page.locator(TEXTBOX).click()
        print('clear existing title')
        page.keyboard.press("Backspace")
        page.keyboard.press("Control+KeyA")
        page.keyboard.press("Delete")
        print('filling new  title')

        page.keyboard.type(title)

        self.log.debug(f'Trying to set "{title}" as description...')

        if description:
            if len(description) > DESCRIPTION_COUNTER:
                print(
                    f"Description was not set due to exceeding the maximum allowed characters ({len(description)}/{DESCRIPTION_COUNTER})"
                )
                description=description[:4888]

            self.log.debug(f'Trying to set "{description}" as description...')
            print('click description field to input')
            page.locator(DESCRIPTION_CONTAINER).click()
            print('clear existing description')
            page.keyboard.press("Backspace")
            page.keyboard.press("Control+KeyA")
            page.keyboard.press("Delete")
            print('filling new  description')

            page.keyboard.type(description)


        if thumbnail:
            self.log.debug(f'Trying to set "{thumbnail}" as thumbnail...')
            if os.path.exists(get_path(thumbnail)):
                page.locator(
                    INPUT_FILE_THUMBNAIL).set_input_files(get_path(thumbnail))
            else:
                if os.path.exists(thumbnail.encode('utf-8')):
                    print('thumbnail found', thumbnail)
                    page.locator(INPUT_FILE_THUMBNAIL).set_input_files(
                        thumbnail.encode('utf-8'))
            sleep(self.timeout)

        self.log.debug('Trying to set video to "Not made for kids"...')
        
        kids_section=page.locator(NOT_MADE_FOR_KIDS_LABEL)
        page.locator(NOT_MADE_FOR_KIDS_RADIO_LABEL).click()
        sleep(self.timeout)
        print('not made for kids done')
        if tags is None or tags =="" or len(tags)==0:
            pass
        else:
            print('tags you give',tags)
            if type(tags) == list:
                tags=",".join(str(tag) for tag in tags)
                tags=tags[:500]
            else:
                tags=tags
            print('overwrite prefined channel tags',tags)
            if len(tags) > TAGS_COUNTER:
                print(f"Tags were not set due to exceeding the maximum allowed characters ({len(tags)}/{TAGS_COUNTER})")
                tags=tags[:TAGS_COUNTER]
            print('click show more button')
            sleep(self.timeout)
            page.locator(MORE_OPTIONS_CONTAINER).click()

            self.log.debug(f'Trying to set "{tags}" as tags...')
            page.locator(TAGS_CONTAINER).locator(TEXT_INPUT).click()
            print('clear existing tags')
            page.keyboard.press("Backspace")
            page.keyboard.press("Control+KeyA")
            page.keyboard.press("Delete")
            print('filling new  tags')
            page.keyboard.type(tags)

# Language and captions certification
# Recording date and location
# Shorts sampling
# Category
        if process100==0:
            pass
        else:
            wait_for_processing(page,process=False)
        # if "complete" in page.locator(".progress-label").text_content():

        # sometimes you have 4 tabs instead of 3
        # this handles both cases
        for _ in range(3):
            try:
                self.click_next(page)
                print('next next!')
            except:
                pass
        if not int(publishpolicy) in [0, 1, 2]:
            publishpolicy=0
        if int(publishpolicy) == 0:
            self.log.debug("Trying to set video visibility to private...")

            public_main_button=page.locator(PRIVATE_BUTTON)
            page.locator(PRIVATE_RADIO_LABEL).click()
        elif int(publishpolicy) == 1:
            self.log.debug("Trying to set video visibility to public...")

            public_main_button=page.locator(PUBLIC_BUTTON)
            page.locator(PUBLIC_RADIO_LABEL).click()
        else:
        # mode a:release_offset exist,publish_data exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow            
            self.log.debug(
                "Trying to set video schedule time...{publish_date}")
            if release_offset and not release_offset == "":
                    print('mode a sta')
                    if not int(release_offset.split('-')[0]) == 0:
                        offset = timedelta(months=int(release_offset.split(
                            '-')[0]), days=int(release_offset.split('-')[-1]))
                    else:
                        offset = timedelta(days=1)
                    if publish_date is None:
                        publish_date =datetime(
                            date.today().year,  date.today().month,  date.today().day, 10, 15)
                    publish_date += offset
                
            else:
                if publish_date is None:
                    publish_date =datetime(
                        date.today().year,  date.today().month,  date.today().day, 10, 15)
                    offset = timedelta(days=1)  
                else:
                    publish_date = publish_date
                # dailycount=4

                # release_offset=str(int(start_index/30))+'-'+str(int(start_index)/int(setting['dailycount']))
                

            setscheduletime(page,publish_date)
            # set_time_cssSelector(page,publish_date)

        video_id=self.get_video_id(page)
        # option 1 to check final upload status
        while self.not_uploaded(page):
            self.log.debug("Still uploading...")
            sleep(5)

        done_button=page.locator(DONE_BUTTON)

        if done_button.get_attribute("aria-disabled") == "true":
            error_message=page.locator(
                ERROR_CONTAINER).text_content()
            return False, error_message

        done_button.click()
        print('upload process is done')

        # # option 2 to check final upload status

        # # Go back to endcard settings
        # page.wait_for_selector("#step-badge-1").click()
        # # self._set_endcard()

        # for _ in range(2):
        #     # Sometimes, the button is clickable but clicking it raises an error, so we add a "safety-sleep" here
        #     sleep(5)
        #     self.click_next(page)

        # sleep(5)
        # page.locator("done-button").click()

        # # Wait for the dialog to disappear
        sleep(5)
        logging.info("Upload is complete")
        self.browser.close()
        # page.locator("#close-icon-button > tp-yt-iron-icon:nth-child(1)").click()
        # print(page.expect_popup().locator("#html-body > ytcp-uploads-still-processing-dialog:nth-child(39)"))
        # page.wait_for_selector("ytcp-dialog.ytcp-uploads-still-processing-dialog > tp-yt-paper-dialog:nth-child(1)")
        # page.locator("ytcp-button.ytcp-uploads-still-processing-dialog > div:nth-child(2)").click()
        return True, video_id

    def get_video_id(self, page) -> Optional[str]:
        video_id=None
        try:
            video_url_container=page.locator(
                VIDEO_URL_CONTAINER)
            video_url_element=video_url_container.locator(
                VIDEO_URL_ELEMENT
            )

            video_id=video_url_element.get_attribute(HREF).split("/")[-1]
        except:
            raise VideoIDError("Could not get video ID")

        return video_id

    @staticmethod
    def _start_playwright():
        return sync_playwright().start()

    def _start_browser(self, browser: str, **kwargs):
        if browser == "chromium":
            return self._playwright.chromium.launch(**kwargs)

        if browser == "firefox":
            return self._playwright.firefox.launch(**kwargs)

        if browser == "webkit":
            return self._playwright.webkit.launch(**kwargs)

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox', or 'webkit' as browser."
        )

    def _start_persistent_browser(
        self, browser: str, user_data_dir: Optional[Union[str, Path]], **kwargs
    ):
        if browser == "chromium":
            return self._playwright.chromium.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "firefox":
            return self._playwright.firefox.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "webkit":
            return self._playwright.webkit.launch_persistent_context(
                user_data_dir, **kwargs
            )

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox' or 'webkit' as browser."
        )
    def close(self):
        self.browser.close()
        self._playwright.stop()