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
import optparse
import sys
from pathlib import Path
import autoit
import re


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F900-\U0001F9FF"  # flags (iOS)
                             "]+", re.UNICODE)
    return re.sub(emoj, '', data)

class BiliChrome():
    def __init__(self, bw_profile, data):
        
        # self.title = title
        # self.date_title = None
        self.driver = None
        self.profile = bw_profile
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        #self.logger
        self.data = data
        self.logger.info('start bili up==================')
        

    @staticmethod
    def is_element_exist(driver, xpath):
        s = driver.find_elements_by_xpath(xpath=xpath)
        if len(s) == 0:
            print("元素未找到:%s" % xpath)
            return False
        elif len(s) == 1:
            return True
        else:
            print("找到%s个元素：%s" % (len(s), xpath))
            return False

    def upload(self, videopath):
        usr_dir = os. getcwd() + "\\" + self.profile + '_profile'
        print(usr_dir)
        Path(usr_dir).mkdir(parents=True, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument(r"--user-data-dir=" + usr_dir)
        #options.add_argument(r"--user-data-dir=C:\Users\dd\AppData\Local\Google\Chrome\User Data")
        options.add_argument('--profile-directory=Default')
        
        #options.add_argument('headless')
        
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
        # service_log_path=service_log_path)
        try:
            print('get upload page')
            self.driver.get("https://member.bilibili.com/video/upload.html")
            
            time.sleep(3)
            
            print(self.driver.current_url)
            if not 'member.bilibili.com/video/upload.html' in self.driver.current_url :
                print('bilibili need login!!!===============')
                time.sleep(60)
                print('Try again after login')
                exit(0)

            #check if loged in
            self.add_videos(videopath)

            # js = "var q=document.getElementsByClassName('content-header-right')[0].scrollIntoView();"
            # driver.execute_script(js)

            print('set info')
            self.add_information()
            
            time.sleep(35)
            #//h3[@class='upload-3-v2-success-hint-1']
            WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH, r"//h3[@class='upload-3-v2-success-hint-1']")))
            upload_success = self.driver.find_element_by_xpath(r"//h3[@class='upload-3-v2-success-hint-1']").get_attribute("innerHTML")
            print('upload_success:' + upload_success)
            #time.sleep(3500)
            if not '稿件投递成功' in upload_success:
                self.driver.save_screenshot('err.png')
                print('稿件提交失败，截图记录')
                return False
                
            # logger.info('%s提交完成！' % title_)
            
            os.remove(videopath)
            print('rm ' + videopath)
            #folder = os.path.dirname(videopath)
            #print('rm ' + folder)
            #shutil.rmtree(folder)
            
            return True
        except selenium.common.exceptions.NoSuchElementException:
            self.logger.exception('发生错误')
        # except selenium.common.exceptions.TimeoutException:
        #     logger.exception('超时')
        except selenium.common.exceptions.TimeoutException:
            self.login()
        except Exception as e:
            print(e)
            print('Exception not captured')
        finally:
            self.driver.quit()
            #print('浏览器驱动退出')
            self.logger.info('浏览器驱动退出')
            return False


       

    def add_videos(self, videopath):
        formate_title = self.data["title"]
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.NAME, 'buploader')))
        up_xpath = '//input[contains(@accept, ".mp4,.flv,.avi,.wmv,.mov") and @name="buploader"]'
        upload = self.driver.find_element_by_xpath(up_xpath)
        # logger.info(driver.title)
        upload.send_keys(videopath)  # send_keys
        self.logger.info('开始上传' + formate_title)
        time.sleep(2)
        button = r'//*[@class="new-feature-guide-v2-container"]/div/div/div/div/div[1]'
        if self.is_element_exist(self.driver, button):
            sb = self.driver.find_element_by_xpath(button)
            sb.click()
            sb.click()
            sb.click()
            self.logger.debug('点击')
        while True:
            try:
                info = self.driver.find_elements_by_class_name(r'item-upload-info')
                for t in info:
                    if t.text != '':
                        print(t.text)
                time.sleep(10)
                text = self.driver.find_elements_by_xpath(r'//*[@class="item-upload-info"]/span')
                aggregate = set()
                for s in text:
                    if s.text != '':
                        aggregate.add(s.text)
                        print(s.text)
                print(aggregate)
                if len(aggregate) >= 1 and ('Upload complete' in aggregate or '上传完成' in aggregate):
                    break
            except selenium.common.exceptions.StaleElementReferenceException:
                self.logger.exception("selenium.common.exceptions.StaleElementReferenceException")
        self.logger.info('上传:%s 个数:%s' % (formate_title, len(info)))

    def add_information(self):
        link = self.data["ytb_link"]
        # 点击模板
        self.driver.find_element_by_xpath(r'//*[@class="normal-title-wrp"]/div/p').click()
        self.driver.find_element_by_class_name(r'template-list-small-item').click()
        # driver.find_element_by_xpath(
        #     r'//*[@id="app"]/div[3]/div[2]/div[3]/div[1]/div[1]/div/div[2]/div[1]').click()
        # 输入转载来源
     
        time.sleep(3)
        input_o = self.driver.find_element_by_xpath(r'//input[contains(@placeholder, "转载视频请注明来源")]')
        input_o.send_keys(link)
        # 选择分区
        # driver.find_element_by_xpath(r'//*[@id="item"]/div/div[2]/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div').click()
        # driver.find_element_by_xpath(r'//*[@id="item"]/div/div[2]/div[3]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div[6]').click()
        # 稿件标题
        time.sleep(5)
        title = self.driver.find_element_by_xpath('//div[@class="content-title-v2-input-wrp"]//div[@class="input-box-v2-1-container"]//div[@class="input-box-v2-1-instance"]//input[@class="input-box-v2-1-val"]')
        title.send_keys(Keys.CONTROL + 'a')
        title.send_keys(Keys.BACKSPACE)
        title.send_keys(self.data["title"])
        
        time.sleep(3)
        
        if 'tags' in self.data and len(self.data['tags']) > 2:
            tag_element = self.driver.find_element_by_xpath('//div[@class="content-tag-v2-input-wrp"]//div[@class="input-box-v2-1-container"]//div[@class="input-box-v2-1-instance"]//input[@class="input-box-v2-1-val"]')
            tags = self.data['tags'].split(',')
            for tag in tags:
                tag_element.send_keys(tag)
                tag_element.send_keys(Keys.ENTER)
                time.sleep(1)
        
        print('up cover')
        if 'cover' in self.data and len(self.data['cover']) > 2:
            # <div class="cover-v2-preview"
            #div class="cover-v2-upload-show-tip" data-v-7ad74b03="">
            #<span class="cover-v2-upload-show-tip-upload
            up_cover_btn = self.driver.find_element_by_xpath('//div[@class="cover-v2-upload-show-tip"]//span[@class="cover-v2-upload-show-tip-upload"]')
            up_cover_btn.click()
            
            cover = self.data['cover']
            print(cover)
            
            time.sleep(2)
            autoit.win_wait("[CLASS:#32770;TITLE:打开]", 10)
            autoit.control_send("[CLASS:#32770;TITLE:打开]", "Edit1", cover)
            autoit.control_click("[CLASS:#32770;TITLE:打开]", "Button1")
            
            time.sleep(3)
            time.sleep(5)
            #print('waiting........')
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cover-chop-modal-v2-btn']"))).click()
            #self.driver.find_element_by_xpath('//div[@class="cover-chop-modal-v2-btn"]').click()
            time.sleep(10)

            
            
        # js = "var q=document.getElementsByClassName('content-tag-list')[0].scrollIntoView();"
        # driver.execute_script(js)
        # time.sleep(3)
        # 输入相关游戏
        # driver.save_screenshot('bin/err.png')
        # print('截图')
        # text_1 = driver.find_element_by_xpath(
        #     '//*[@id="item"]/div/div[2]/div[3]/div[2]/div[2]/div[1]/div[5]/div/div/div[1]/div[2]/div/div/input')
        # text_1.send_keys('星际争霸2')
        # 简介
        
        time.sleep(3)
        text_2 = self.driver.find_element_by_xpath('//div[@class="content-desc-v2-text-wrp"]//div[@class="archive-info-editor"]//div[@class="editor ql-container"]//div[@class="ql-editor ql-blank"]')
        desc = self.data["desc"]
        desc = remove_emojis(desc)
        if len(desc) > 210:
            desc = desc[0:210]
        text_2.send_keys(desc + '\n本视频从外网转载, 字幕为机翻')
        
        time.sleep(5)
        
        self.driver.find_element_by_xpath("//span[@class='submit-btn-group-add']").click()
        
        #time.sleep(5)



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


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option( '--profile', default='handmake', help='指定浏览器用户配置')
    parser.add_option( '--data', default='handmade2_video.json', help='指定JSON数据文件')
    
    options, args = parser.parse_args()
    profile= options.profile
    json_path = options.data

    with open(json_path,encoding='utf8') as json_file:
            #print(json_file)
            videos = json.load(json_file)
            for video_info in videos:
                video_file = video_info['v_dst']
                
                if not os.path.isfile(video_file):
                    print(video_file + ' not exist' )
                    continue
                    
                bili_helper = BiliChrome(profile, video_info)
                #bili_helper.login()
                
                print('Uploading ' + video_file)
                bili_helper.upload(video_file)
                
                break













