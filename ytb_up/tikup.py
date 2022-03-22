import json
from .constants import *
from .logging import Log
from .exceptions import *
from .utils import *
import os
from .login import *
from datetime import timedelta, date

from time import sleep
import logging
import re
from playwright.sync_api import *
import pickle
PROTECTED_FILES = ["processed.mp4", "VideosSaveHere.txt"]

class TiktokUpload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str = "",
        timeout: int = 3,
        headless: bool = True,
        debug: bool = True,
        ytb_username:str ="",
        ytb_password:str ="",
        ytb_cookies:str="",
        tiktok_cookies:str="",
        tiktok_username:str="",
        tiktok_password:str=""

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
        self.ytb_username=ytb_username
        self.ytb_password=ytb_password
        self.ytb_cookies = ytb_cookies
        self.tiktok_username=tiktok_username
        self.tiktok_cookies=tiktok_cookies
        self.tiktok_password=tiktok_password
        self.log.debug("Firefox is now running")

    # Class used to upload video.

    def upload(
        self,
        videopath: str,
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
        self.page = self.context.new_page()
        print('============tags',tags)
        if not videopath:
            raise FileNotFoundError(f'Could not find file with path: "{videopath}"')

    def tiktokUpload(self):
        page=self.page
        # Cookies loaded here.

        if self.CHANNEL_COOKIES and not self.CHANNEL_COOKIES == '':
            print('cookies existing', self.CHANNEL_COOKIES)
            self.cookies = self.load_cookies(self.tiktok_cookies)

       
            # login_using_cookie_file(self,self.CHANNEL_COOKIES,page)         
            page.goto(TIKTOK_URL)

            page.reload()
        else:
            self.log.info('Please sign in and then press enter')
            # input()
            page.goto(TIKTOK_URL)
            # Interact with login form
            browser_context = self.browser.new_context(
                ignore_https_errors=True)
            browser_context.clear_cookies()
            # page.click('text=Login')
            # page.fill('input[name="login"]', USERNAME)
            # page.fill('input[name="password"]', PASSWORD)
            # page.click('text=Submit')
            sleep(USER_WAITING_TIME)
            storage = browser_context.storage_state(path=self.tiktok_cookies)
            self.context = browser_context

        islogin = confirm_logged_in(page)
        print('checking login status', islogin)

        if not islogin:
            print('try to load cookie files')
            self.cookies = self.load_cookies(self.tiktok_cookies)
            print('success load cookie files')
            page.goto(TIKTOK_URL)
            print('start to check login status')
            islogin = confirm_logged_in(page)
            
        print('start change locale to english')

        set_channel_language_english(page)
        print('finish change locale to english')
        page.goto(YOUTUBE_UPLOAD_URL)
        # sleep(self.timeout)
        self.log.debug(f'found to YouTube account check')

        if page.locator("#select-files-button")is None and page.locator("//*[@id='dialog-title']"):
            print('try to input credentials')
            verify(self,page)
        #confirm-button > div:nth-child(2)


        self.log.debug(f'Trying to upload "{videopath}" to YouTube...')
        if os.path.exists(get_path(videopath)):
            page.locator(
                INPUT_FILE_VIDEO)
            page.set_input_files(INPUT_FILE_VIDEO, get_path(videopath))
        else:
            if os.path.exists(videopath.encode('utf-8')):
                print('videopath found', videopath)
                page.locator(
                    INPUT_FILE_VIDEO)
                page.set_input_files(INPUT_FILE_VIDEO, videopath.encode('utf-8'))
        sleep(self.timeout)
        self.log.debug("Found YouTube upload Dialog Modal")

        # page = page.locator(UPLOAD_DIALOG_MODAL)


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
        # kids_section=page.locator(NOT_MADE_FOR_KIDS_LABEL)
        page.locator(RADIO_LABEL).click()
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



    # Method to check file is valid.
    def checkFileExtensionValid(self):
        if self.userRequest["dir"].endswith('.mp4'):
            pass
        else:
            self.bot.close()
            exit(f"File: {self.userRequest['dir']} has wrong file extension.")


    # This gets the hashtags from file and adds them to the website input
    def addCaptions(self, hashtag_file=None):
        if not hashtag_file:
            caption_elem = self.webbot.getCaptionElem()
            for hashtag in self.IO.getHashTagsFromFile():
                caption_elem.send_keys(hashtag)

    def clearCaptions(self):
        caption_elem = self.webbot.getCaptionElem()
        caption_elem.send_keys("")

    def inputScheduler(self, schdate, schtime):
        # In charge of selecting scheduler in the input.
        utils.randomTimeQuery()
        self.webbot.selectScheduleToggle()


    # This is in charge of adding the video into tiktok input element.
    def inputVideo(self, startTime=0, endTime=0):
        try:
            file_input_element = self.webbot.getVideoUploadInput()
        except Exception as e:
            print("Major error, cannot find the upload button, please update getVideoUploadInput() in Bot.py")
            print(f"Actual Error: {e}")
            file_input_element = ""
            exit()
        # Check if file has correct .mp4 extension, else throw error.
        self.video = Video(self.userRequest["dir"], self.userRequest["vidTxt"], self.userPreference)
        print(f"startTime: {startTime}, endTime: {endTime}")
        if startTime != 0 and endTime != 0 or endTime != 0:
            print(f"Cropping Video timestamps: {startTime}, {endTime}")
            self.video.customCrop(startTime, endTime)
        # Crop first and then make video.

        self.video.createVideo()  # Link to video class method
        while not os.path.exists(self.video.dir):  # Wait for path to exist
            time.sleep(1)
        abs_path = os.path.join(os.getcwd(), self.video.dir)
        file_input_element.send_keys(abs_path)



    def directUpload(self, filename, private=False, test=False):
        if self.bot is None:
            self.bot = Browser().getBot()
            self.webbot = Bot(self.bot)
        self.bot.get(self.url)
        utils.randomTimeQuery()
        self.cookies = Cookies(self.bot)
        self.bot.refresh()

        try:
            file_input_element = self.webbot.getVideoUploadInput()
        except Exception as e:
            print(f"Error: {e}")
            print("Major error, cannot find the file upload button, please update getVideoUploadInput() in Bot.py")
            file_input_element = None
            exit()
        abs_path = os.path.join(os.getcwd(), filename)
        try:
            file_input_element.send_keys(abs_path)
        except StaleElementReferenceException as e:
            try:
                self.bot.implicitly_wait(5)
                file_input_element = self.webbot.getVideoUploadInput()
                file_input_element.send_keys(abs_path)
            except Exception as e:
                print("Major error, cannot find the file upload button, please update getVideoUploadInput() in Bot.py")
                exit()


        # We need to wait until it is uploaded and then clear input.

        self.addCaptions()
        utils.randomTimeQuery()
        if private:
            self.webbot.selectPrivateRadio()  # private video selection
            utils.randomTimeQuery()
        else:
            """
            self.webbot.selectPublicRadio()  # public video selection
            utils.randomTimeQuery()
            """
            pass
        if not test:

            self.webbot.uploadButtonClick()  # upload button
        input("Press any button to exit")


    """
    Returns TikTok cookies
    """

    def load_cookies(self,cookies):
        self.context.clear_cookies()

        self.context.add_cookies(
            json.load(
                open(
                    cookies, 
                    'r'
                )
            )
        )             

    """
    Remove unnecessary fields from cookies
    """
    def strip_cookies(cookies):

        stripped_cookies = []
        for cookie in cookies:

            stripped_cookie = {
                'name' : cookie['name'],
                'value' : cookie['value']
            }

            stripped_cookies.append(stripped_cookie)

        return stripped_cookies

    """
    Save the TikTok cookies locally
    """
    def save_tiktok_cookies(new_cookies):

        stripped_cookies = strip_cookies(new_cookies)
        cookies_file_name = "tiktok_cookies.pkl"

        with open(cookies_file_name, 'wb') as cookies_file:
            pickle.dump(stripped_cookies, cookies_file)