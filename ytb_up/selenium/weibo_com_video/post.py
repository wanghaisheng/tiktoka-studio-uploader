
import time
import pickle
import json
import os
import pickle
import autoit
import browser_cookie3
from random import randrange
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def milli_time_of_next_day():
    return round( (time.time() + 3600* 24 ) *1000)




def selenium_login():
    cj = browser_cookie3.firefox()
    for cookie in cj:
        if cookie.domain in '.weibo.com' and cookie.path == '/':
            #print(cookie)
            secure = True
            if cookie.secure == 0:
                secure = False
            cookie_dict = {'domain': cookie.domain, 'name': cookie.name,  'value': cookie.value, 'secure': secure}
            if cookie.expires:
                cookie_dict['expiry'] = cookie.expires
            if cookie.path_specified:
                cookie_dict['path'] = cookie.path
 
            cookie_dict['sameSite'] = "None"
            print(cookie_dict)
            browser.add_cookie(cookie_dict)
    
  
def is_element_exist(browser,  elm):
    s = browser.find_elements_by_xpath(xpath=elm)
    if len(s) == 0:
        print("元素未找到:%s" % elm)
        return False
    else:
        print("找到%s个元素：%s" % (len(s), elm))
        return True

            
def selenium_enter_weibo(video_path,title):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\Users\dd\AppData\Local\Google\Chrome\User Data")
    options.add_argument('--profile-directory=Default')
    #options.add_argument('headless')
    #self.driver = webdriver.Chrome(executable_path=config.get('chromedriver_path'), chrome_options=options)
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
    
    browser.get('https://weibo.com/upload/channel')
    
    #video_a = browser.find_element_by_xpath("//div[@class='func_area clearfix']//div[@class='kind']//a[@action-type='video']")

    up_btn_xpath = r"//div[@class='channel_top1_sHJWe']//div//button[@class='woo-button-main woo-button-flat woo-button-primary woo-button-m woo-button-round VideoUpload_btn1_2avmO']"
    #'//div[@class="VideoPop_top1_oL9sO"]//div[1]//div[1]//div[class="wbpro-file"]//button[starts-with(@id,"video_button_upload_")]'
    browser.find_element_by_xpath(up_btn_xpath).click()
    
    time.sleep(2)
    autoit.win_wait("[CLASS:#32770;TITLE:打开]", 10)
    autoit.control_send("[CLASS:#32770;TITLE:打开]", "Edit1", video_path)
    autoit.control_click("[CLASS:#32770;TITLE:打开]", "Button1")
    
    time.sleep(3)
    
    count = 0
    while count < 1000:
        try:
            
            print('Checking status')
            #//div[@class='channel_top1_sHJWe']//div//span[contains(text(),'上传完成')]
            #//div[@class='channel_top1_sHJWe']//div//span[contains(text(),'上传完成')]
            #//div[@class='channel_top1_sHJWe']//div//span[contains(text(),'上传中')]
            #//div[@class='modal-scroll channel_unmodal_33Zke']//div[@class='VideoUpload_abox4_1406j VideoUpload_gap2_1h6PT']//div[2]//span[2]
            #isDisplayed
            
            up_done = browser.find_element_by_xpath("//div[@class='channel_top1_sHJWe']//div//span[contains(text(),'上传完成')]")
            up_status = browser.find_element_by_xpath("//div[@class='channel_top1_sHJWe']//div//span[contains(text(),'上传中')]")
            
            if up_done.is_displayed():
                print('Upload done')
                break
            elif up_status.is_displayed():
                print('Uploading...')
                count = 0
                time.sleep(10)
            else:
                time.sleep(3)
                print('Can not find status info')
                count += 1
                continue
        except:
           time.sleep(30)
           print('Can not get the upload status!!!')
           break 
        
    
    video_title_input = browser.find_element_by_xpath("//div[@class='wbpro-form channel_top1_sHJWe']//div[@class='woo-box-flex']//div[@class='woo-box-item-flex']//input")
    video_title_input.send_keys(title)
    
    
    video_desc_input = browser.find_element_by_xpath("//textarea[@placeholder='有什么新鲜事想分享给大家？']")
    video_desc_input.send_keys(title)
    
    
    video_submit = browser.find_element_by_xpath("//button[@class='woo-button-main woo-button-flat woo-button-primary woo-button-m woo-button-round Tool_btn_2Eane Tool_btn1_2vfU9']")
    video_submit.click()
    
    print('Post done')
    time.sleep(30)
 
    
    print('bw true===============')
    print('Remove ' + video_path)
    os.remove(video_path)
 
    browser.close()
    
  


def post_video():
 
    #"v_src": "D:\\obsolute\\video_conv\\video_auto\\funny\\A bird that catches a flying fish-z48iktvgJns.mp4",
    #"title": "一只捕捉飞鱼的鸟",
    
    with open('D:\\obsolute\\video_conv\\video_auto\\funny\\info.json', encoding='utf-8') as f:
        videos = json.load(f)

    for v in videos:
        v_path = v['v_src']
        if not os.path.isfile(v_path):
            print(v_path + " doesn't exits")
            continue
            
        v_title = v['title']
        print(v_path)
        print(v_title)
        selenium_enter_weibo(v_path,v_title)
   
        break
 
from datetime import datetime
def convet_datatime_to_seconds(date_str):
    #2021-10-18 09:41
    dd_str = date_str.split(' ')[0]
    dd1 = dd_str.split('-')
    yy = dd1[0]
    mm = dd1[1]
    dd = dd1[2]
    
    datetime.datetime(yy, mm, dd, 0, 0, 0)
    
    return datetime.timetuple()
 

if __name__ == "__main__":
    os.system('taskkill /F /im chrome.exe /T')
    #print(current_milli_time())
    post_video()
    #comment_2_resou()
    
    

