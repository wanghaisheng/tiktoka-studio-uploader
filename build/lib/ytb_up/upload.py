import json
from .constants import *
from .logging import Log
from .exceptions import *
from .login import *
import os
from datetime import timedelta, date

from typing import Tuple, Optional
from time import sleep
from datetime import datetime,date
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from pathlib import Path
import logging
import re
from selenium.webdriver import ActionChains

def get_path(file_path: str) -> str:
    # no clue why, but this character gets added for me when running
    # return str(os.path(file_path)).replace("\u202a", "")
    # return file_path.replace("\u202a", "")
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
        publishpolicy:str='0',
        release_offset:str='0-1',
        publish_date:datetime =datetime( date.today().year,  date.today().month,  date.today().day, 20, 15),
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
            self.log.info('Please sign in and then press enter')
            input()
            self.driver.get(YOUTUBE_URL)
            sleep(USER_WAITING_TIME)
            os.rename(self.CHANNEL_COOKIES,self.CHANNEL_COOKIES+'.bak')
            with open(self.CHANNEL_COOKIES, 'w') as filehandler:
                json.dump(self.driver.get_cookies(), filehandler)     
            os.remove(self.CHANNEL_COOKIES+'.bak')       
            self.driver.save_cookies()
        self.driver.get(YOUTUBE_URL)
        sleep(self.timeout)
        # logincheck?


        islogin =confirm_logged_in(self.driver)
        if not islogin:

            print('it seems network is not that well try an proxy setting')
            firefox_profile = webdriver.FirefoxProfile(self.root_profile_directory)

            firefoxoptions = webdriver.FirefoxOptions()
            firefoxoptions.headless = True    
            proxy_option = {
                'backend': 'mitmproxy',
                'proxy': {
                    'http': 'socks5://127.0.0.1:1080',
                    'https': 'socks5://127.0.0.1:1080',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }        
            self.driver = webdriver.Firefox(options=firefoxoptions,
            
            firefox_profile=firefox_profile,seleniumwire_options=proxy_option, executable_path=executable_path)
            login_using_cookie_file(self.driver, cookie_file=self.CHANNEL_COOKIES)
            islogin =confirm_logged_in(self.driver)
            if not islogin:
                input()
                self.driver.get(YOUTUBE_URL)
                sleep(USER_WAITING_TIME)
                os.rename(self.CHANNEL_COOKIES,self.CHANNEL_COOKIES+'.bak')
                with open(self.CHANNEL_COOKIES, 'w') as filehandler:
                    json.dump(self.driver.get_cookies(), filehandler)     
                os.remove(self.CHANNEL_COOKIES+'.bak')       
                # self.driver.save_cookies()
                login_using_cookie_file(self.driver, cookie_file=self.CHANNEL_COOKIES)
                islogin =confirm_logged_in(self.driver)
                if not islogin:
                    print('we need find the bug')

        self.driver.get(YOUTUBE_URL)       
        print('start change locale to english')

        self.__set_channel_language_english()
        print('finish change locale to english')

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



        # Catch max uploads/day limit errors
        next_button = self.driver.find_element(By.ID, NEXT_BUTTON)
        if next_button.get_attribute('hidden') == 'true':
            error_short_by_xpath = self.driver.find(By.XPATH, ERROR_SHORT_XPATH)
            # print(f"ERROR: {error_short_by_xpath.text} {self.cookie_working_dir}")
            return False

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
        description=description[:5000]
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
            if type(tags)==list:
                tags = ",".join(str(tag) for tag in tags)
                tags=tags[:500]
            else:
                tags=tags
            if len(tags) > TAGS_COUNTER:
                raise ExceedsCharactersAllowed(
                    f"Tags were not set due to exceeding the maximum allowed characters ({len(tags)}/{TAGS_COUNTER})"
                )

            self.log.debug(f'Trying to set "{tags}" as tags...')
            container = modal.find_element_by_xpath(TAGS_CONTAINER)
            tags_field = self.click(container.find_element_by_id(TEXT_INPUT))
            self.send(tags_field, tags)

        self._wait_for_processing(process=False)                    


        # sometimes you have 4 tabs instead of 3
        # this handles both cases
        for _ in range(3):
            try:
                self.click_next(modal)
            except:
                pass
        if not int(publishpolicy) in [0,1,2]:
            publishpolicy=0
        if int(publishpolicy)==0:
            self.log.debug("Trying to set video visibility to private...")

            public_main_button = modal.find_element_by_name(PRIVATE_BUTTON)
            public_main_button.find_element_by_id(RADIO_LABEL).click()
        elif int(publishpolicy)==1:
            self.log.debug("Trying to set video visibility to public...")

            public_main_button = modal.find_element_by_name(PUBLIC_BUTTON)
            public_main_button.find_element_by_id(RADIO_LABEL).click()
        else:
            self.log.debug("Trying to set video schedule time...{publish_date}")
            publish_date = datetime( date.today().year,  date.today().month,  date.today().day, 20, 15)
            offset=timedelta(days=1)
            if release_offset and not release_offset=="":
                print('1--',release_offset)
                if not int(release_offset.split('-')[0])==0:
                    offset =timedelta(months=int(release_offset.split('-')[0]),days=int(release_offset.split('-')[-1]))   
            else:
                offset=timedelta(days=1)
            publish_date += offset

            self._set_time(publish_date)   
            # self.__set_scheduler(publish_date)    
        video_id = self.get_video_id(modal)
        # self.waitfordone() 
        self._wait_for_processing(False) 
        # option 1 to check final upload status 
        while self.not_uploaded(modal):
            self.log.debug("Still uploading...")
            sleep(1)

        done_button = modal.find_element_by_id(DONE_BUTTON)

        if done_button.get_attribute("aria-disabled") == "true":
            error_message = self.driver.find_element_by_xpath(ERROR_CONTAINER).text
            return False, error_message

        self.click(done_button)
        print('upload process is done') 

        # # option 2 to check final upload status 

        # # Go back to endcard settings
        # self.driver.find_element_by_css_selector("#step-badge-1").click()
        # self._set_endcard()

        # for _ in range(2):
        #     # Sometimes, the button is clickable but clicking it raises an error, so we add a "safety-sleep" here
        #     sleep(5)
        #     WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "next-button"))).click()

        # sleep(5)
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "done-button"))).click()

        # # Wait for the dialog to disappear
        # sleep(5)
        # logging.info("Upload is complete")




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
        # why does not work again
        try:
            print('Click your profile picture .',self.driver.find_element(By.ID,"img"))

            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, "avatar-btn")))
            self.driver.find_element(By.ID,"avatar-btn").click()
            print(' Click Language or Location.')
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//yt-icon[@id='right-icon'])[6]")))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//yt-icon[@id='right-icon'])[6]")))
            self.driver.find_element(By.XPATH,"(//yt-icon[@id='right-icon'])[6]").click()
            print('Click the language or location you’d like to use.')
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//yt-formatted-string[@id='label'])[26]")))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "(//yt-formatted-string[@id='label'])[26]")))
            self.driver.find_element(By.XPATH,"(//yt-formatted-string[@id='label'])[26]").click()            
            return True
        except TimeoutError:
            return False

    def waitfordone(self):

        # wait until video uploads
        # uploading progress text contains ": " - Timp ramas/Remaining time: 3 minutes.
        # we wait until ': ' is removed, so we know the text has changed and video has entered processing stage
        uploading_progress_text = self.browser.find(By.CSS_SELECTOR, UPLOADING_PROGRESS_SELECTOR).text
        while ': ' in uploading_progress_text:
            sleep(5)
            uploading_progress_text = self.browser.find(By.CSS_SELECTOR, UPLOADING_PROGRESS_SELECTOR).text
    def _wait_for_processing(self,process):
        driver = self.driver
        if process==True:
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
        else:
            while True:
                x_path = '//span[@class="progress-label style-scope ytcp-video-upload-progress"]' 
    #TypeError: 'WebElement' object  is not subscriptable
                upload_progress = self.driver.find_elements_by_css_selector('[class="progress-label style-scope ytcp-video-upload-progress"]')[0].text

                innerhtml =self.driver.find_element(By.XPATH,x_path).get_attribute('innerHTML')
                if re.match(r"\D \.\.\. \D", innerhtml) or re.match(r"^[^\.]+$",innerhtml):
                    break
                if  not '%' in upload_progress.lower():
                    break
                if 'complete' in upload_progress.lower():
                    break


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
        print('==time_str==',time_str)
        print('==time_str==',time_list[2:])
        print('==time_str==',[time for time in time_list[2:] if time.text == time_str])

        time = [time for time in time_list[2:] if time.text == time_str][0]
        time.click()       
    def close(self):
        self.driver.close()
        self.driver.quit()

        self.log.debug("Closed Firefox")


    def remove_unwatched_videos(self, remove_copyrighted, remove_unwatched_views):
        try:
            self.browser.get(YOUTUBE_URL)
            sleep(USER_WAITING_TIME)

            # set english as language
            self.__set_channel_language_english()

            self.driver.get("https://studio.youtube.com/")
            sleep(USER_WAITING_TIME)
            self.driver.find_element_by_id("menu-paper-icon-item-1").click()
            sleep(USER_WAITING_TIME)

            if self.__is_videos_available():
                return True

            self.driver.find_element_by_css_selector("#page-size .ytcp-text-dropdown-trigger").click()
            sleep(USER_WAITING_TIME)
            # clock 50 items per page
            pagination_sizes = self.driver.find_elements_by_css_selector("#select-menu-for-page-size #dialog .paper-item")
            pagination_sizes[2].click()
            sleep(USER_WAITING_TIME)

            # filter to delete only copyrighted videos
            if remove_copyrighted:
                self.driver.find_element_by_id("filter-icon").click()
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_css_selector("ytcp-text-menu#menu tp-yt-paper-dialog tp-yt-paper-listbox paper-item#text-item-1 ytcp-ve div").click()
                sleep(USER_WAITING_TIME)

            # filter to delete videos with views lower than 100
            if remove_unwatched_views:
                views_no = "100000"
                self.driver.find_element_by_id("filter-icon").click()
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_css_selector("ytcp-text-menu#menu tp-yt-paper-dialog tp-yt-paper-listbox paper-item#text-item-5 ytcp-ve div").click()
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_xpath("//iron-input[@id='input-2']/input").click()
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_xpath("//iron-input[@id='input-2']/input").clear()
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_xpath("//iron-input[@id='input-2']/input").send_keys(views_no)
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_xpath("//input[@type='text']").click()
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_xpath("//tp-yt-paper-listbox[@id='operator-list']/paper-item[2]").click()
                sleep(USER_WAITING_TIME)
                self.driver.find_element_by_xpath("//ytcp-button[@id='apply-button']/div").click()
                sleep(USER_WAITING_TIME)

            return self.__remove_unwatched_videos()
        except Exception as e:
            print(e)
            return False

    def __is_videos_available(self):
        # if there are no videos to be deleted, this element should be visible
        # if not visible throw error, and proceed to delete more videos
        try:
            self.driver.find_element_by_xpath("//ytcp-video-section-content[@id='video-list']/div/div[2]/div")
            # return True, there are no more video to be deleted
            return True
        except:
            return False
    def __set_scheduler(self,publish_date):
        # Set upload time
        action = ActionChains(self.driver)
        schedule_radio_button = self.driver.find_element_by_id("schedule-radio-button")

        action.move_to_element(schedule_radio_button)
        action.click(schedule_radio_button).perform()
        self.log.debug('Set delevery to {}'.format("schedule"))
        sleep(.33)

        #Set close action
        action_close = ActionChains(self.driver)
        action_close.send_keys(Keys.ESCAPE)

        #date picker
        action_datepicker = ActionChains(self.driver)
        datepicker_trigger = self.driver.find_element_by_id("datepicker-trigger")

        action_datepicker.move_to_element(datepicker_trigger)
        action_datepicker.click(datepicker_trigger).perform()
        sleep(.33)

        date_string = publish_date.strftime("%d.%m.%Y")
        date_input = self.driver.find_element_by_xpath('//ytcp-date-picker/tp-yt-paper-dialog//iron-input/input')

        self.__write_in_field(date_input, date_string, True)
        self.log.debug('Set schedule date to {}'.format(date_string))

        action_close.perform()
        sleep(.33)


        #time picker
        action_timepicker = ActionChains(self.driver)
        time_of_day_trigger = self.driver.find_element_by_id("time-of-day-trigger")
        
        action_timepicker.move_to_element(time_of_day_trigger)
        action_timepicker.click(time_of_day_trigger).perform()
        sleep(.33)

        time_dto = (publish_date - timedelta( 
                            minutes = publish_date.minute % 15,
                            seconds = publish_date.second,
                            microseconds = publish_date.microsecond))
        time_string = time_dto.strftime("%H:%M")
        
        time_container = self.driver.find_element_by_xpath('//ytcp-time-of-day-picker//*[@id="dialog"]')
        time_item = self.driver.find_element_by_xpath('//ytcp-time-of-day-picker//tp-yt-paper-item[text() = "{}"]'.format(time_string))
        
        self.log.debug('Set schedule date to {}'.format(time_string))
        self.driver.execute_script("arguments[0].scrollTop = arguments[1].offsetTop; ", time_container, time_item)

        time_item.click()

        action_close.perform()
        sleep(.33)


    def __remove_unwatched_videos(self):
        DELETE_WAIT_TIME = 60 * 2

        # check if videos deletion process has finished
        # if not visible throw error, and proceed to delete more videos
        try:
            self.driver.find_element_by_xpath("//div[@id='header']/div/span[2]")
            # wait for the videos to be deleted and try delete videos after
            sleep(DELETE_WAIT_TIME)
            return self.__remove_unwatched_videos()
        except:
            pass

        if self.__is_videos_available():
            return True

        self.driver.find_element_by_id("checkbox-container").click()
        sleep(USER_WAITING_TIME)
        self.driver\
            .find_element_by_css_selector(".ytcp-bulk-actions .toolbar .ytcp-select .ytcp-text-dropdown-trigger .ytcp-dropdown-trigger .right-container .ytcp-dropdown-trigger")\
            .click()
        sleep(USER_WAITING_TIME)
        self.driver.find_element_by_css_selector("#select-menu-for-additional-action-options #dialog #paper-list #text-item-1").click()
        sleep(USER_WAITING_TIME)
        self.driver.find_element_by_css_selector("#dialog-content-confirm-checkboxes #confirm-checkbox #checkbox-container").click()
        sleep(USER_WAITING_TIME)
        self.driver.find_element_by_css_selector(".ytcp-confirmation-dialog #dialog-buttons #confirm-button").click()
        # wait 5 minutes for the videos to be deleted
        sleep(DELETE_WAIT_TIME)

        return self.__remove_unwatched_videos()

