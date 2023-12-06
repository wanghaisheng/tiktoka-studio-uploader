#-*- coding: utf-8 -*-
from typing import DefaultDict, Optional
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from collections import defaultdict
import json
from pathlib import Path
import logging
from upgenius.tiktok.selenium.Constant import TIKTOK_CONSTANT
from  upgenius.utils.webdriver.ChromeDriver import ChromeDriver
from upgenius.utils.webdriver.AdsChrome import AdsChromeDriver
logging.basicConfig()


class AdspowerUploader:
    def __init__(self, pkl_path: str, account: str, video_path: str, title: str, caption: str, description: str, tags: str, title_tags: str, use_file_title:str, finger_web: str) -> None:
        self.account = account
        self.video_path = video_path
        self.title = title
        self.caption = caption
        self.description = description
        self.tags = tags
        self.title_tags = title_tags
        self.use_file_title = use_file_title == "true"
        current_working_dir = pkl_path
        if finger_web == "":
            self.browser = ChromeDriver(current_working_dir, current_working_dir)
        else:
            self.browser = AdsChromeDriver(current_working_dir, current_working_dir, finger_web)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def upload(self):
        try:
            self.logger.info("step 1: logging....")
            self.__login()
            self.logger.info("step 2: ready to upload....")
            self.__upload()
        except Exception as e:
            print(e)
            self.__quit()
            raise

    def __login(self):
        self.browser.driver.get(TIKTOK_CONSTANT.TIKTOK_URL)
        time.sleep(TIKTOK_CONSTANT.USER_WAITING_TIME)
        if self.browser.has_cookies_for_current_website(self.account):
            self.browser.load_cookies(self.account)
            time.sleep(TIKTOK_CONSTANT.USER_WAITING_TIME)
            self.browser.refresh()
        else:
            self.logger.info('Please sign in and then press enter')
            input()
            self.browser.get(TIKTOK_CONSTANT.TIKTOK_URL)
            time.sleep(TIKTOK_CONSTANT.USER_WAITING_TIME)
            self.browser.save_cookies(self.account)

    def __quit(self):
        self.browser.quit()

    def __upload(self) -> (bool, Optional[str]):
        # 要上传视频的路径
        absolute_video_path = self.video_path

        # 打开相应的网页
        self.logger.info("step 3: open the tiktok website....")
        self.browser.get(TIKTOK_CONSTANT.TIKTOK_UPLOAD_URL)
        time.sleep(TIKTOK_CONSTANT.LOAD_TIME)

        # 切换到iframe中
        self.browser.switch_to_frame(TIKTOK_CONSTANT.IFRAME)
        time.sleep(TIKTOK_CONSTANT.USER_WAITING_TIME)

        # 上传视频
        self.logger.info("step 4: uploading the video....")
        self.browser.find_element_by_xpath(TIKTOK_CONSTANT.INPUT_FILE_VIDEO)\
            .send_keys(absolute_video_path)
        self.browser.driver.implicitly_wait(15)

        self.logger.debug('Attached video {}'.format(self.video_path))
        time.sleep(TIKTOK_CONSTANT.WAIT_TIME)

        # 填写Caption
        self.logger.info("step 5: fill in the caption....")
        self.browser.find_element_by_xpath(TIKTOK_CONSTANT.Caption).send_keys(Keys.CONTROL, 'a')
        self.browser.find_element_by_xpath(TIKTOK_CONSTANT.Caption).send_keys(Keys.DELETE)

        caption = self.browser.find_element_by_xpath(TIKTOK_CONSTANT.Caption)
        self.browser.driver.implicitly_wait(10)
        ActionChains(self.browser.driver).move_to_element(caption).click(caption).perform()
        time.sleep(1)
        if self.use_file_title:
            pass
        else:
            ActionChains(self.browser.driver).send_keys(self.caption).perform()

        tags = self.tags.split("#")
        for tag in tags:
            ActionChains(self.browser.driver).send_keys("#" + tag.strip()).perform()
            time.sleep(2)
            ActionChains(self.browser.driver).send_keys(Keys.RETURN).perform()
            time.sleep(1)
        time.sleep(5)

        self.browser.driver.execute_script("window.scrollTo(150, 300);")
        time.sleep(5)

        # 允许审查
        self.logger.info("step 6: check the copyright....")
        check = self.browser.find_element_by_class_name(TIKTOK_CONSTANT.ALLOW_CHECK)
        ActionChains(self.browser.driver).move_to_element(check).click(check).perform()
        time.sleep(TIKTOK_CONSTANT.CHECK_TIME)

        # 发布
        self.logger.info("step 7: post the video....")
        post = WebDriverWait(self.browser.driver, 100).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[7]/div[2]/button')))
        post.click()

        time.sleep(TIKTOK_CONSTANT.WAIT_TIME)
        self.logger.info("step 8: finished....")
        self.browser.quit()

    def __write_field(self, xpath, dic):
        self.browser.find_element_by_xpath(xpath).click()
        self.browser.find_element_by_xpath(xpath).clear()
        time.sleep(TIKTOK_CONSTANT.USER_WAITING_TIME)

        self.browser.find_element_by_xpath(xpath).send_keys(dic['caption'])
        time.sleep(TIKTOK_CONSTANT.USER_WAITING_TIME)

        # # todo: 将@和#的部分也做出来
        # tags = dic['tags'].split(",")
        # self.browser.find_element_by_xpath(xpath).send_keys("  ")
        # if len(tags) > 0:
        #     for tag in tags:
        #         self.browser.find_element_by_xpath(xpath).send_keys("#" + tag)
        #         self.browser.find_element_by_xpath(xpath).send_keys(Keys.ENTER)
        #         time.sleep(TIKTOK_CONSTANT.USER_WAITING_TIME)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--video",
    #                     help='Path to the video file',
    #                     required=True)
    # parser.add_argument("-t",
    #                     "--thumbnail",
    #                     help='Path to the thumbnail image', )
    # parser.add_argument("--meta", help='Path to the JSON file with metadata')
    # args = parser.parse_args()
    # uploader = TiktokUploader(args.video, args.meta, args.thumbnail)
    uploader = AdspowerUploader("jie", "new bag.mp4", "conf.json", None)
    uploader.upload()
