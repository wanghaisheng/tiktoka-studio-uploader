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
#from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import optparse
import shutil
import autoit
import sys
from pathlib import Path

def milli_time_of_next_day():
    return round( (time.time() + 3600* 24 ) *1000)


def load_cookies(browser):
    with open('cookies.json', 'r', newline='') as inputdata:
        cookies = json.load(inputdata)
        #print(vars(self.browser))
        for cookie in cookies:
            #print(cookie)
            cookie['sameSite'] = "None"
            if 'expirationDate' in cookie:
                if isinstance( cookie['expirationDate'], float):
                    cookie['expirationDate'] = milli_time_of_next_day()/1000
                elif isinstance( cookie['expirationDate'], int):
                    cookie['expirationDate'] = int(milli_time_of_next_day()/1000)
                
            if 'expiry' in cookie:
                if isinstance( cookie['expiry'], float):
                    cookie['expiry'] = milli_time_of_next_day()/1000
                elif isinstance( cookie['expiry'], int):
                    cookie['expiry'] = int(milli_time_of_next_day()/1000)
            browser.add_cookie(cookie)
            
        inputdata.close()

def save_cookies(browser):
     with open('cookies.json', 'w') as statusf:
        json.dump(browser.get_cookies(), statusf,indent=2)
        statusf.close()


class IXiguaChrome():
    def __init__(self, bw_profile, data):
        
        # self.title = title
        # self.date_title = None
        self.driver = None
        self.profile = bw_profile
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
        usr_dir = os. getcwd() + "\\" + self.profile + '_profile'
        print(usr_dir)
        Path(usr_dir).mkdir(parents=True, exist_ok=True)
                
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(r"--user-data-dir=" + usr_dir)
        #options.add_argument(r"--user-data-dir=C:\Users\dd\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Default')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
        
        
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source":
            "const newProto = navigator.__proto__;"
            "delete newProto.webdriver;"
            "navigator.__proto__ = newProto;"
        })
        # service_log_path=service_log_path)
        
        
        self.driver.get("https://studio.ixigua.com/upload?from=post_article")
        time.sleep(5)
        
        
        elm = r"//div[@class='user-info__username']"
        if False == self.is_element_exist( elm):
            print('Not loged in???')
            self.login()
            exit(-1)
         
        # print(driver.title)
        ret = self.add_videos(videopath)
        if False == ret:
            self.driver.save_screenshot('err.png')
            print('稿件提交失败，截图记录:' + videopath)
            time.sleep(300)
        else:
            print('提交成功:' + videopath)
            print('Remove ' + videopath)
            os.remove(videopath)

        self.driver.quit()
        print('浏览器驱动退出')
        #self.logger.info('浏览器驱动退出')
        return True

    def login(self):
        self.logger.info('Douyin need login!!!')
     
        time.sleep(120)
        print(self.driver.title)
       
       

    def add_videos(self, video_path):
        #video_path = 'D:\\m.mp4'
        formate_title = self.data["title"]
  
        self.driver.find_element_by_xpath('//div[@class="byte-upload xigua-upload-video-trigger upload-video-trigger-card has-extra-content"]/input[1]').send_keys(video_path)
    
        time.sleep(3)
        
        self.logger.info('开始上传' + formate_title)
        time.sleep(5)
        #status = r"//div[@class='status']"
        
        while True:
            try:
                if self.is_element_exist(r"//div[@class='status']"):
                    status = self.driver.find_element_by_xpath(r"//div[@class='status']")
                    txt = status.text
                    print(txt)
                    if txt == '上传成功':
                        break
                    
                    if txt == '上传失败':
                        r = self.driver.find_element_by_xpath(r"//span[@class='reason']")
                        print(r.text)
                        return False
                    
                percent = self.driver.find_element_by_xpath(r"//div[@class='percent']")       
                print(percent.text)
                #print(len(info))
                time.sleep(3)

            except Exception:
                print("Upload done???")
                break
        
        time.sleep(3)
        #title
        title = self.driver.find_element_by_xpath(r"//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
        title.send_keys(Keys.CONTROL + 'a')
        title.send_keys(Keys.BACKSPACE)
        print(self.data["title"])
        title.send_keys(self.data["title"])
        
        time.sleep(3)
        #简介
        #desc = self.driver.find_element_by_xpath(r"//div[@data-editor='abstract']//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
        #desc.send_keys(Keys.CONTROL + 'a')
        #desc.send_keys(Keys.BACKSPACE)
        #print(self.data["title"])
        #desc.send_keys(self.data["title"])
        
        #cover
        print('uploading cover...')
        self.driver.find_element_by_xpath(r"//div[@class='m-xigua-upload']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath(r"//li[contains(text(),'本地上传')]").click()
        time.sleep(2)
        #self.driver.find_element_by_xpath(r"//p[@class='mark']").click()
        
        cover_xpath = r"//div[@class='byte-upload xigua-upload-poster-trigger upload-thumb-trigger-card']/input"
        self.driver.find_element_by_xpath(cover_xpath).send_keys(self.data["cover"])
        time.sleep(5)
           # //div[@class='clip-btn-content']//div[@class='clip-btn-content']   
        if self.is_element_exist("//div[@class='clip-btn-content']"):
            btn = self.driver.find_element_by_xpath("//div[@class='clip-btn']")
            self.driver.implicitly_wait(15)
            print('confirm_modify')
            if btn.is_displayed():
                ActionChains(self.driver).move_to_element(btn).click(btn).perform()
        
        submit_covert_btn = WebDriverWait(self.driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-l btn-sure ml16')]")))
        time.sleep(10)
        print('submit cover')
        ActionChains(self.driver).move_to_element(submit_covert_btn).click(submit_covert_btn).perform()
       
        
        confirm_covert_btn = WebDriverWait(self.driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='m-button red undefined']")))
        time.sleep(10)
        print('confirm cover again')
        ActionChains(self.driver).move_to_element(confirm_covert_btn).click(confirm_covert_btn).perform()
        
        print('uploading cover done')
        
        submit_video_btn = WebDriverWait(self.driver, 300).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'发布')]")))
        time.sleep(10)
        
        #原创
        ele_xpath = r"//div[@class='video-form-item form-item-origin']//label[1]//span[1]//div[1]"
        if self.is_element_exist(ele_xpath):
            self_created = self.driver.find_element_by_xpath(ele_xpath)
            self_created.click()

        ActionChains(self.driver).move_to_element(submit_video_btn).click(submit_video_btn).perform()
        
        time.sleep(5)
        
        print(self.driver.current_url)
        if 'tudio.ixigua.com/content' in self.driver.current_url :
            print('Video uploaded successfuly')
            return True
  
        print('Video uploaded failed')
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

def up_from_json(json_data,profile):
    with open(json_data,encoding='utf8') as json_file:
            #print(json_file)
            videos = json.load(json_file)
            for video_info in videos:
                video_file = video_info['v_dst']
                
                if not os.path.isfile(video_file):
                    print(video_file + ' not exist' )
                    continue
                    
                bili_helper = IXiguaChrome(profile,video_info)
                #bili_helper.login()
                
                print('Uploading ' + video_file)
                bili_helper.upload(video_file)
                
                break


if __name__ == '__main__':
    os.system('taskkill /F /im chrome.exe /T')
    parser = optparse.OptionParser()
    parser.add_option( '--profile', default='ch_quotes', help='指定浏览器用户配置')
    parser.add_option( '--data', default='ch_quotes.json', help='指定JSON数据文件')

    options, args = parser.parse_args()
    profile= options.profile
            
    json_path = options.data

    up_from_json(json_path, profile)










