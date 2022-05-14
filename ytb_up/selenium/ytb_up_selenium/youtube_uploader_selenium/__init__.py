
from typing import DefaultDict, Optional

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


from collections import defaultdict
import json
import time
from .Constant import *
from pathlib import Path
import logging
import platform
import os



logging.basicConfig()


class YouTubeUploader:
    """A class for uploading videos on YouTube via Selenium using metadata JSON file
    to extract its title, description etc"""

              
                
    def __init__(self,  metadata_json: str, thumbnail_path: Optional[str] = None) -> None:

        self.thumbnail_path = thumbnail_path
        self.metadata_dict = metadata_json
        
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(r"--user-data-dir=C:\Users\dd\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Default')
        #options.add_argument('headless')
        #self.driver = webdriver.Chrome(executable_path=config.get('chromedriver_path'), chrome_options=options)
        self.browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
        #self.browser = Firefox(current_working_dir, current_working_dir)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.__validate_inputs()

        

        self.video_path = self.metadata_dict[Constant.VIDEO_PATH]



    def __validate_inputs(self):
        if not os.path.isfile(self.metadata_dict[Constant.VIDEO_PATH]):
            self.logger.warning('No video path specified')
            exit(-1)
        if not self.metadata_dict[Constant.VIDEO_TITLE]:
            self.logger.warning("The video title was not found in a metadata file")
            self.logger.warning("The video title was set to {}".format(
                Path(self.video_path).stem))
        if not self.metadata_dict[Constant.VIDEO_DESCRIPTION]:
            self.logger.warning(
                "The video description was not found in a metadata file")

    def upload(self):
        try:
            #self.__login()
            return self.__upload()
        except Exception as e:
            print(e)
            self.__quit()
            raise

    def __login(self):
        self.browser.get(Constant.YOUTUBE_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        self.load_login_cookies()

        if self.browser.has_cookies_for_current_website():
            self.browser.load_cookies()
            time.sleep(Constant.USER_WAITING_TIME)
            self.browser.refresh()
        else:
            self.logger.info('Please sign in and then press enter')
            # input()
            self.load_login_cookies()
            time.sleep(Constant.USER_WAITING_TIME)
            self.browser.get(Constant.YOUTUBE_URL)
            time.sleep(Constant.USER_WAITING_TIME)
            self.browser.save_cookies()

    def __write_in_field(self, field, string, select_all=False):
        field.click()
        time.sleep(Constant.USER_WAITING_TIME)
        if select_all:
            field.send_keys(Keys.CONTROL + 'a')
            time.sleep(Constant.USER_WAITING_TIME)
        field.send_keys(string)

    def __upload(self) -> (bool, Optional[str]):
        self.browser.get(Constant.YOUTUBE_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        self.browser.get(Constant.YOUTUBE_UPLOAD_URL)
        time.sleep(Constant.USER_WAITING_TIME)
        absolute_video_path = str(Path.cwd() / self.video_path)
        self.browser.find_element_by_xpath( Constant.INPUT_FILE_VIDEO).send_keys(
            absolute_video_path)
        self.logger.debug('Attached video {}'.format(self.video_path))

        if self.thumbnail_path is not None:
            absolute_thumbnail_path = str(Path.cwd() / self.thumbnail_path)
            self.browser.find_element_by_xpath(Constant.INPUT_FILE_THUMBNAIL).send_keys(
                absolute_thumbnail_path)
            change_display = "document.getElementById('file-loader').style = 'display: block! important'"
            self.browser.driver.execute_script(change_display)
            self.logger.debug(
                'Attached thumbnail {}'.format(self.thumbnail_path))

        time.sleep(15)
        title_field = self.browser.find_element_by_id( Constant.TEXTBOX)
        self.__write_in_field(
            title_field, self.metadata_dict[Constant.VIDEO_TITLE], select_all=True)
        self.logger.debug('The video title was set to \"{}\"'.format(
            self.metadata_dict[Constant.VIDEO_TITLE]))

        video_description = self.metadata_dict[Constant.VIDEO_DESCRIPTION]
        video_description = video_description.replace("\n", Keys.ENTER)
        if video_description:
            #//ytcp-mention-textbox[@label='Description']//div[@id='textbox']
            description_field = self.browser.find_element_by_xpath("//ytcp-mention-textbox[@label='Description']//div[@id='textbox']")
            self.__write_in_field(description_field, video_description, select_all=True)
            self.logger.debug('Description filled.')

        kids_section = self.browser.find_element_by_name(Constant.NOT_MADE_FOR_KIDS_LABEL).click()
        #self.browser.find_element_by_id(Constant.RADIO_LABEL, kids_section).click()
        self.logger.debug('Selected \"{}\"'.format(Constant.NOT_MADE_FOR_KIDS_LABEL))

        # Advanced options
        self.browser.find_element_by_xpath( Constant.MORE_BUTTON).click()
        self.logger.debug('Clicked MORE OPTIONS')

        #tags_container = self.browser.find_element_by_xpath(Constant.TAGS_INPUT_CONTAINER)
        #tags_field = self.browser.find_element_by_id(Constant.TAGS_INPUT, element=tags_container)
        #self.__write_in_field(tags_field, ','.join(self.metadata_dict[Constant.VIDEO_TAGS]))
        #self.logger.debug('The tags were set to \"{}\"'.format(self.metadata_dict[Constant.VIDEO_TAGS]))

        self.browser.find_element_by_id( Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} one'.format(Constant.NEXT_BUTTON))

        # Thanks to romka777
        self.browser.find_element_by_id(Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} two'.format(Constant.NEXT_BUTTON))

        self.browser.find_element_by_id(Constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {} three'.format(Constant.NEXT_BUTTON))
        #public_main_button = self.browser.find_element_by_name( Constant.PUBLIC_BUTTON)
        
        self.browser.find_element_by_xpath("//tp-yt-paper-radio-button[@name='PUBLIC']//div[@id='radioLabel']").click()
        self.logger.debug('Made the video {}'.format(Constant.PUBLIC_BUTTON))

        video_id = self.__get_video_id()

        status_container = self.browser.find_element_by_xpath(Constant.STATUS_CONTAINER)
        while True:
            in_process = status_container.text.find(Constant.UPLOADED) != -1
            if in_process:
                print('Waiting uploading done....')
                time.sleep(Constant.USER_WAITING_TIME)
            else:
                break

        done_button = self.browser.find_element_by_id( Constant.DONE_BUTTON)

        # Catch such error as
        # "File is a duplicate of a video you have already uploaded"
        if done_button.get_attribute('aria-disabled') == 'true':
            error_message = self.browser.find_element_by_xpath(Constant.ERROR_CONTAINER).text
            self.logger.error(error_message)
            return False, None

        done_button.click()
        self.logger.debug(
            "Published the video with video_id = {}".format(video_id))
        time.sleep(Constant.USER_WAITING_TIME)
        
        #self.save_cookies()
        
        time.sleep(5)
        
        #self.browser.get(Constant.YOUTUBE_URL)
        self.__quit()
        return True, video_id

    def __get_video_id(self) -> Optional[str]:
        video_id = None
        try:
            video_url_container = self.browser.find_element_by_xpath(Constant.VIDEO_URL_CONTAINER)
            video_url_element = self.browser.find_element_by_xpath( Constant.VIDEO_URL_ELEMENT)
            video_id = video_url_element.get_attribute(
                Constant.HREF).split('/')[-1]
        except:
            self.logger.warning(Constant.VIDEO_NOT_FOUND_ERROR)
            pass
        return video_id

    def __quit(self):
        self.browser.close()
