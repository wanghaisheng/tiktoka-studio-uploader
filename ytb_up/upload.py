import json
from .constants import *
from .logging import Log
from .exceptions import *
from .login import *

from pathlib import Path
from typing import Tuple, Optional
from time import sleep
from datetime import datetime,date
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

import logging
import re

def get_path(file_path: str) -> str:
    # no clue why, but this character gets added for me when running
    return str(Path(file_path)).replace("\u202a", "")


class Upload:
    def __init__(
        self,
        root_profile_directory: str,
        proxy_option: str ="",
        executable_path: str = "geckodriver",
        timeout: int = 3,
        headless: bool = True,
        debug: bool = True,
        CHANNEL_COOKIES:str=""

    ) -> None:

        firefox_profile = webdriver.FirefoxProfile(root_profile_directory)

        firefoxoptions = webdriver.FirefoxOptions()
        firefoxoptions.headless = headless
        if proxy_option =="":
            self.driver = webdriver.Firefox(options=firefoxoptions,
            firefox_profile=firefox_profile, executable_path=executable_path)            
        else:
            self.driver = webdriver.Firefox(options=firefoxoptions,
            firefox_profile=firefox_profile,seleniumwire_options=proxy_option, executable_path=executable_path)
        self.timeout = timeout
        self.log = Log(debug)
        self.CHANNEL_COOKIES=CHANNEL_COOKIES
        self.log.debug("Firefox is now running")

    def click(self, element):
        element.click()
        sleep(self.timeout)
        return element

    def send(self, element, text: str) -> None:
        element.clear()
        sleep(self.timeout)
        element.send_keys(text)
        sleep(self.timeout)

    def click_next(self, modal) -> None:
        modal.find_element_by_id(NEXT_BUTTON).click()
        sleep(self.timeout)

    def not_uploaded(self, modal) -> bool:
        return modal.find_element_by_xpath(STATUS_CONTAINER).text.find(UPLOADED) != -1

    def upload(
        self,
        file: str,
        title: str = "",
        description: str = "",
        thumbnail: str = "",
        publish_date:datetime =datetime( date.today().year,  date.today().month,  date.today().day+1, 20, 15),
        tags: list = [],
    ) -> Tuple[bool, Optional[str]]:
        """Uploads a video to YouTube.
        Returns if the video was uploaded and the video id.
        """
        if not file:
            raise FileNotFoundError(f'Could not find file with path: "{file}"')
        if self.CHANNEL_COOKIES and not self.CHANNEL_COOKIES=='':
            print('loading existing cookies from',self.CHANNEL_COOKIES)
            login_using_cookie_file(self.driver, cookie_file=self.CHANNEL_COOKIES)
        elif self.driver.has_cookies_for_current_website():
            self.driver.load_cookies()
            sleep(USER_WAITING_TIME)
            self.driver.refresh()
        else:
            # self.logger.info('Please sign in and then press enter')
            input()
            self.driver.get(YOUTUBE_URL)
            sleep(USER_WAITING_TIME)
            self.driver.save_cookies()
        self.driver.get(YOUTUBE_URL)
        sleep(self.timeout)
        # logincheck?


        confirm_logged_in(self.driver)
        wait = WebDriverWait(self.driver, 10)
        self.__set_channel_language_english()
        self.driver.get(YOUTUBE_UPLOAD_URL)
        sleep(self.timeout)

        self.log.debug(f'Trying to upload "{file}" to YouTube...')

        self.driver.find_element_by_xpath(INPUT_FILE_VIDEO).send_keys(get_path(file))
        sleep(self.timeout)

        modal = self.driver.find_element_by_css_selector(UPLOAD_DIALOG_MODAL)
        self.log.debug("Found YouTube upload Dialog Modal")

# fix google account verify
        try:

            while True:
                check =self.driver.find_element(By.XPATH,'//*[@id="dialog-title"]')
                self.log.debug(f'found to YouTube account check')
                sleep(30)
                # gmail =''
                # password='%R00b'
                # self.driver.find_element(By.XPATH,'//*[@id="confirm-button"]').click()
                # self.__verifyitsyou(self,gmail,password)
                x_path = '//*[@id="textbox"]'
                if self.driver.find_element(By.XPATH,x_path):                        
                    self.log.debug(f'fix  YouTube account check')
                    break      

        except:
            sleep(1)
        sleep(60)


        self.log.debug(f'Trying to set "{title}" as title...')

        # TITLE
        title_field = self.click(modal.find_element_by_id(TEXTBOX))

        # get file name (default) title
        title = title if title else title_field.text

        if len(title) > TITLE_COUNTER:
            raise ExceedsCharactersAllowed(
                f"Title was not set due to exceeding the maximum allowed characters ({len(title)}/{TITLE_COUNTER})"
            )

        # clearing out title which defaults to filename
        for i in range(len(title_field.text) + 10):
            # more backspaces than needed just to be sure
            title_field.send_keys(Keys.BACKSPACE)
            sleep(0.1)

        self.send(title_field, title)

        if description:
            if len(description) > DESCRIPTION_COUNTER:
                raise ExceedsCharactersAllowed(
                    f"Description was not set due to exceeding the maximum allowed characters ({len(description)}/{DESCRIPTION_COUNTER})"
                )

            self.log.debug(f'Trying to set "{description}" as description...')
            container = modal.find_element_by_xpath(DESCRIPTION_CONTAINER)
            description_field = self.click(container.find_element_by_id(TEXTBOX))

            self.send(description_field, description)

        if thumbnail:
            self.log.debug(f'Trying to set "{thumbnail}" as thumbnail...')
            modal.find_element_by_xpath(INPUT_FILE_THUMBNAIL).send_keys(
                get_path(thumbnail)
            )
            sleep(self.timeout)

        self.log.debug('Trying to set video to "Not made for kids"...')
        kids_section = modal.find_element_by_name(NOT_MADE_FOR_KIDS_LABEL)
        kids_section.find_element_by_id(RADIO_LABEL).click()
        sleep(self.timeout)

        if tags:
            self.click(modal.find_element_by_xpath(MORE_OPTIONS_CONTAINER))

            tags = ",".join(str(tag) for tag in tags)

            if len(tags) > TAGS_COUNTER:
                raise ExceedsCharactersAllowed(
                    f"Tags were not set due to exceeding the maximum allowed characters ({len(tags)}/{TAGS_COUNTER})"
                )

            self.log.debug(f'Trying to set "{tags}" as tags...')
            container = modal.find_element_by_xpath(TAGS_CONTAINER)
            tags_field = self.click(container.find_element_by_id(TEXT_INPUT))
            self.send(tags_field, tags)

        # sometimes you have 4 tabs instead of 3
        # this handles both cases
        for _ in range(3):
            try:
                self.click_next(modal)
            except:
                pass
        if publish_date:
            print('schedule time',type(publish_date),publish_date)
            self._set_time(publish_date)
        else:
            self.log.debug("Trying to set video visibility to public...")
            public_main_button = modal.find_element_by_name(PUBLIC_BUTTON)
            public_main_button.find_element_by_id(RADIO_LABEL).click()
            
        video_id = self.get_video_id(modal)

        while self.not_uploaded(modal):
            self.log.debug("Still uploading...")
            sleep(1)

        done_button = modal.find_element_by_id(DONE_BUTTON)

        if done_button.get_attribute("aria-disabled") == "true":
            error_message = self.driver.find_element_by_xpath(ERROR_CONTAINER).text
            return False, error_message

        self.click(done_button)

        return True, video_id

    def get_video_id(self, modal) -> Optional[str]:
        video_id = None
        try:
            video_url_container = modal.find_element_by_xpath(VIDEO_URL_CONTAINER)
            video_url_element = video_url_container.find_element_by_xpath(
                VIDEO_URL_ELEMENT
            )

            video_id = video_url_element.get_attribute(HREF).split("/")[-1]
        except:
            raise VideoIDError("Could not get video ID")

        return video_id
    def __set_channel_language_english(self):
        try:
            print('start change locale to english')
            self.driver.find_element(By.ID,"img").click()
            sleep(USER_WAITING_TIME)
            self.driver.find_element(By.XPATH,"(//yt-icon[@id='right-icon'])[6]").click()
            sleep(USER_WAITING_TIME)
            self.driver.find_element(By.XPATH,"(//yt-formatted-string[@id='label'])[26]").click()
            sleep(USER_WAITING_TIME)
        except:
            pass




    def _wait_for_processing(self):
        driver = self.driver

        # Wait for processing to complete
        progress_label: WebElement = driver.find_element_by_css_selector("span.progress-label")
        pattern = re.compile(r"(finished processing)|(processing hd.*)|(check.*)")
        current_progress = progress_label.get_attribute("textContent")
        last_progress = None
        while not pattern.match(current_progress.lower()):
            if last_progress != current_progress:
                logging.info(f'Current progress: {current_progress}')
            last_progress = current_progress
            sleep(5)
            current_progress = progress_label.get_attribute("textContent")


    def _set_basic_settings(self, title: str, description: str, thumbnail_path: str = None):
        driver = self.driver

        title_input: WebElement = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//ytcp-mention-textbox[@label="Title"]//div[@id="textbox"]',

                )
            )
        )

        # Input meta data (title, description, etc ... )
        description_input: WebElement = driver.find_element_by_xpath(
            '//ytcp-mention-textbox[@label="Description"]//div[@id="textbox"]'
        )
        thumbnail_input: WebElement = driver.find_element_by_css_selector(
            "input#file-loader"
        )

        title_input.clear()
        title_input.send_keys(title)
        description_input.send_keys(description)
        if thumbnail_path:
            thumbnail_input.send_keys(thumbnail_path)


    def _set_advanced_settings(self,game_title: str, made_for_kids: bool):
        # Open advanced options
        driver = self.driver

        driver.find_element_by_css_selector("#toggle-button").click()
        if game_title:
            game_title_input: WebElement = driver.find_element_by_css_selector(
                ".ytcp-form-gaming > "
                "ytcp-dropdown-trigger:nth-child(1) > "
                ":nth-child(2) > div:nth-child(3) > input:nth-child(3)"
            )
            game_title_input.send_keys(game_title)

            # Select first item in game drop down
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#text-item-2",  # The first item is an empty item
                    )
                )
            ).click()

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.NAME, "VIDEO_MADE_FOR_KIDS_MFK" if made_for_kids else "VIDEO_MADE_FOR_KIDS_NOT_MFK")
        )).click()


    def _set_endcard(self):
        driver = self.driver

        # Add endscreen
        driver.find_element_by_css_selector("#endscreens-button").click()
        sleep(5)

        for i in range(1, 11):
            try:
                # Select endcard type from last video or first suggestion if no prev. video
                driver.find_element_by_css_selector("div.card:nth-child(1)").click()
                break
            except (NoSuchElementException, ElementNotInteractableException):
                logging.warning(f"Couldn't find endcard button. Retry in 5s! ({i}/10)")
                sleep(5)

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "save-button"))).click()


    def _set_time(self, publish_date: datetime):
        # Start time scheduling
        driver = self.driver
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "SCHEDULE"))).click()

        # Open date_picker
        driver.find_element_by_css_selector("#datepicker-trigger > ytcp-dropdown-trigger:nth-child(1)").click()

        date_input: WebElement = driver.find_element_by_css_selector("input.tp-yt-paper-input")
        date_input.clear()
        # Transform date into required format: Mar 19, 2021
        date_input.send_keys(publish_date.strftime("%b %d, %Y"))
        date_input.send_keys(Keys.RETURN)

        # Open time_picker
        driver.find_element_by_css_selector(
            "#time-of-day-trigger > ytcp-dropdown-trigger:nth-child(1) > div:nth-child(2)"
        ).click()

        time_list = driver.find_elements_by_css_selector("tp-yt-paper-item.tp-yt-paper-item")
        # Transform time into required format: 8:15 PM
        time_str = publish_date.strftime("%I:%M %p").strip("0")
        time = [time for time in time_list[2:] if time.text == time_str][0]
        time.click()       
    def close(self):
        self.driver.quit()
        self.driver.close()

        self.log.debug("Closed Firefox")
