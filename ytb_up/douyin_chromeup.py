import json
import os
import random
import time
import logging
import selenium.common
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import shutil

import sys


def milli_time_of_next_day():
    return round( (time.time() + 3600* 24 ) *1000)



class DouyinChrome():
    def __init__(self, data):
        
        # self.title = title
        # self.date_title = None
        self.driver = None
        #self.COOKIE_FILE = 'dy_cookie.bin'
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        #self.logger
        self.data = data
        self.logger.info('start douyin up==================')
        

    def is_element_exist(self,  elm):
        s = self.driver.find_elements_by_xpath(xpath=elm)
        if len(s) == 0:
            print("元素未找到:%s" % elm)
            return False
        else:
            print("找到%s个元素：%s" % (len(s), elm))
            return True

    def upload(self, videopath):

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(r"--user-data-dir=C:\Users\dd\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Default')
        #options.add_argument('headless')
        #self.driver = webdriver.Chrome(executable_path=config.get('chromedriver_path'), chrome_options=options)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
        
        
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source":
            "const newProto = navigator.__proto__;"
            "delete newProto.webdriver;"
            "navigator.__proto__ = newProto;"
        })
        # service_log_path=service_log_path)
        
        
        #self.driver.get("https://www.douyin.com")
        #time.sleep(20)
        #print('4')            
        #elm = r'//a[@class="caa4fd3df2607e91340989a2e41628d8-scss" and contains(text(),"个人中心")]'
        #if False == self.is_element_exist( elm):
        #    print('Not loged in???')
        #    self.login()
        #    exit(-1)
         
        #save_cookies(self.driver)
        #print('Goto upload page')
        self.driver.get("https://creator.douyin.com/creator-micro/content/upload")

        # print(driver.title)
        if False == self.add_videos(videopath):
            return False

        # js = "var q=document.getElementsByClassName('content-header-right')[0].scrollIntoView();"
        # driver.execute_script(js)

        print('set info')
        video_desc = r"//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']//span[1]"
        
        #//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']
        editor = self.driver.find_element_by_xpath(video_desc)
        editor.send_keys(Keys.CONTROL + 'a')
        editor.send_keys(Keys.BACKSPACE)
        time.sleep(10)
        print(self.data["title"])
        editor.send_keys(self.data["title"])
        
        #don't publish to toutiao
        if self.is_element_exist('//input[@role="switch"]'):
            pub2other = self.driver.find_element_by_xpath('//input[@role="switch"]')
            if pub2other.get_attribute('checked') :
                pub2other.click()
        
        time.sleep(3)

        self.driver.find_element_by_xpath('//div[@class="content-confirm-container--2AI6I"]/button[@class="button--1SZwR primary--1AMXd fixed--3rEwh"]').click()
        # screen_shot = driver.save_screenshot('bin/1.png')
        # print('截图')
        time.sleep(60)
        
        #print("Uploaded video:" + up_title)
           
        print(self.driver.current_url)
        if 'https://creator.douyin.com/creator-micro/content/manage' in self.driver.current_url :
            print('提交成功:' + videopath)
            print('Remove ' + videopath)
            os.remove(videopath)
        else:
            self.driver.save_screenshot('err.png')
            print('稿件提交失败，截图记录')
            return False

        # logger.info('%s提交完成！' % title_)
     
        self.driver.quit()
        #print('浏览器驱动退出')
        self.logger.info('浏览器驱动退出')
        return True

    def login(self):
        self.logger.info('Douyin need login!!!')
     
        time.sleep(120)
        print(self.driver.title)

        
       

    def add_videos(self, videopath):
        formate_title = self.data["title"]
        # class="upload-btn-input--1NeEX" name="upload-btn"
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.NAME, 'upload-btn')))
        time.sleep(3)
        upload = self.driver.find_element_by_xpath(r'//input[@class="upload-btn-input--1NeEX" and @name="upload-btn"]')
        # logger.info(driver.title)
        upload.send_keys(videopath)  # send_keys
        self.logger.info('开始上传' + formate_title)
        time.sleep(5)
        status = r'//div[@class="progress-inner--2l6st"]/span[@class="text--2bHjU"]'
  
        while True:
            try:
                info = self.driver.find_elements_by_xpath(status)
                if len(info) < 1:
                    print("Upload done???")
                    break
                    
                print(info[0].text)
                #print(len(info))
                time.sleep(3)
            except Exception:
                print("Upload done???")
                break
         
        #<div class="word-card--1neCx">  <div class="text--GjPv4">
        #retry_btn = r'//div[@class="word-card--1neCx"]/span[@class="text--GjPv4" and contains(text(),"重新上传")]'
        time.sleep(3)
        retry_btn = r'//div[@class="word-card--1neCx"]/*[@class="text--GjPv4" and contains(text(),"重新上传")]'
        if self.is_element_exist( retry_btn ):
            self.logger.info('上传%s 成功' % (formate_title))
            return True
            
        self.logger.info('上传%s 失败' % (formate_title))
        return False

    


def validate_json():
    with open('handmade_videos.json',encoding='utf8') as json_file:
        #print(json_file)
        videos = json.load(json_file)
        for video_info in videos:
            if not os.path.isfile( video_info['v_dst'] ):
                print(video_info['v_dst'] + ' not exist')

            print(video_info['ytb_link'] )
            
#validate_json()
#exit(0)

#        "cover": "D:\\handmade_gen\\72度的DIORAMA村庄房屋拥有自己的双手木屋的建造和绘画\\ДЕРЕВЕНСКИЕ ДОМА для ДИОРАМЫ в 72 масштабе СВОИМИ РУКАМИ. ПОСТРОЙКА и ПОКРАСКА деревянного ДОМА.-LzzoTl6FKYo.jpg",
#        "desc": "72 级坦克战斗立体模型！ 展示如何为未来的立体模型制作木制乡村房屋",
#        "folder": "D:\\handmade_gen\\72度的DIORAMA村庄房屋拥有自己的双手木屋的建造和绘画",
#        "title": "坦克战斗立体模型",
#        "v_dst": "D:\\handmade_gen\\72度的DIORAMA村庄房屋拥有自己的双手木屋的建造和绘画\\ДЕРЕВЕНСКИЕДОМАдляДИОРАМЫв72масштабеСВОИМИРУКАМИПОСТРОЙКАиПОКРАСКАдеревянногоДОМАLzzoTl6FKYo.mkv",
#        "v_src": "D:\\handmade\\ДЕРЕВЕНСКИЕ ДОМА для ДИОРАМЫ в 72 масштабе СВОИМИ РУКАМИ. ПОСТРОЙКА и ПОКРАСКА деревянного ДОМА.-LzzoTl6FKYo.mkv",
#        "ytb_link": "https://www.youtube.com/watch?v=LzzoTl6FKYo"


#video_info = {"format_title":'波士顿机器人',"url":'https://www.youtube.com/watch?v=omRAf5kvYDY'}
#video_file = 'D:\\obsolute\\social_media\\biliup_selenium\\HappyHolidays-RDZu04v7_hc.mp4'

def up_from_json():
    with open('final_funny2.json',encoding='utf8') as json_file:
            #print(json_file)
            videos = json.load(json_file)
            for video_info in videos:
                video_file = video_info['v_dst']
                
                if not os.path.isfile(video_file):
                    print(video_file + ' not exist' )
                    continue
                    
                bili_helper = DouyinChrome(video_info)
                #bili_helper.login()
                
                print('Uploading ' + video_file)
                bili_helper.upload(video_file)
                
                break

os.system('taskkill /F /im chrome.exe /T')
up_from_json()










