
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
import optparse
import sqlite3
from db_helper import *
import datetime
from langdetect import detect
import re
  
def is_element_exist(browser,  elm):
    s = browser.find_elements_by_xpath(xpath=elm)
    if len(s) == 0:
        print("元素未找到:%s" % elm)
        return False
    else:
        print("找到%s个元素：%s" % (len(s), elm))
        return True


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F900-\U0001F9FF"  # flags (iOS)
                             "]+", re.UNICODE)
    return re.sub(emoj, '', data)
 
 
def get_uid_from_url(url):
    return url.split('=')[1].strip()
    
 
def convet_datatime_to_seconds(date_str):
    #2021-10-18 09:41
    dd_str = date_str.split(' ')[0]
    dd1 = dd_str.split('-')
    yy = int(dd1[0])
    mm = int(dd1[1])
    dd = int(dd1[2])
    
    return datetime.datetime(yy, mm, dd, 0, 0, 0).timestamp()
    


comments = [
'thumb up',
'Keep it up'

]

def get_comment():
    max_idx = len(comments)
    idx = randrange(max_idx)
    return comments[idx]
 
def getOnlyTextFromNode(elem):
    text = elem.text.strip()
   
    children = elem.find_elements_by_xpath("./*")
    for child in children:
        text = text.replace(child.text, "",1).strip()
    print(text)
    return text;


def get_comment2(comments_section):
    #contents = comments_section.find_elements_by_xpath('.//div[@class="content"]')
    
    idx = 0
    max_count = 0
    max_idx = 0
    for content in comments_section:
        likes = content.find_element_by_xpath('.//span[@id="vote-count-left"]')
        try:
            count = int(likes.get_attribute('innerHTML').strip())
        except:
            count = 0
        #print(likes.get_attribute('innerHTML'))
        #print('likes:')
        #print(count)
        if count > max_count:
            max_count = count
            max_idx = idx
        idx += 1
    
    if idx == 0:
        return get_comment()
        
    print(max_idx)
    print(idx)
    #print(len(comments_section))
    c = comments_section[max_idx]
    txt_div = c.find_element_by_xpath('.//*[@id="content-text"]')
    #print(c.get_attribute('innerHTML'))
    comment = txt_div.text
    comment = remove_emojis(comment)
    print('comment:' + comment)
    if len(comment) > 5:
        return comment + "--thumb up"
     
    #exit(0)
    return get_comment()
    
    
def get_usr_from_url(url):
    #https://weibo.com/u/6207240934?aa
    url = url.replace('https://weibo.com/u/','')
    usr = url.split('?')[0]
    return url
 

 
 
def comment_on_video(browser, url):
    print('url:' + url)
    browser.get(url)
    
    time.sleep(10)
    browser.execute_script("window.scrollTo(0, 900);")
    
    time.sleep(5)
    
    comments = browser.find_elements_by_xpath('//div[@class="style-scope ytd-item-section-renderer"]/ytd-comment-thread-renderer[@class="style-scope ytd-item-section-renderer"]')
    comment = get_comment2(comments)
    print(comment)
    
    comment_editor_xpath = "//yt-formatted-string[@class='style-scope ytd-comment-simplebox-renderer']"
    if not is_element_exist(browser,comment_editor_xpath):
        return
        
    e1e = browser.find_element_by_xpath(comment_editor_xpath)
    #print(e1e)
    e1e.click()
    #time.sleep(2)
    #ele.send_keys(comment)
    
    time.sleep(2)
    
    print(comment)
    editor = browser.find_element_by_xpath("//div[@id='contenteditable-root']")
    editor.send_keys(comment)
    time.sleep(3)
    
    submit_btn = browser.find_element_by_xpath("//ytd-button-renderer[@id='submit-button']//yt-formatted-string[@id='text']")
    submit_btn.click()
    time.sleep(30)
        

#(1727, '7690934847')
def comment_to_videos(browser):
    videos = browser.find_elements_by_xpath('//ytd-rich-grid-media[@class="style-scope ytd-rich-item-renderer"]')
    print(len(videos))
    v_urls = []
    for v in videos:
        #print(v.get_attribute('innerHTML'))
        #print('===========')
        LIVE_TAG_XPATH = './/span[@class="style-scope ytd-badge-supported-renderer"]'
        if is_element_exist(v,LIVE_TAG_XPATH):
            span = v.find_element_by_xpath(LIVE_TAG_XPATH)
            print(span.text)
            if 'LIVE NOW' in span.text:
                continue
 
        url = v.find_element_by_xpath('.//a[@class="yt-simple-endpoint inline-block style-scope ytd-thumbnail"]').get_attribute('href')
        vid = get_uid_from_url(url)
        if db_is_video_already_commented(vid):
            print(vid + ' already processed')
            continue
        
        v_urls.append(url)
     
    idx = 0
    for url in v_urls:
        idx += 1
        print("start=={}======{} of {}==========".format(url,idx ,len(v_urls)))
        
        vid = get_uid_from_url(url)
        if db_is_video_already_commented(vid):
            print(url + " already processed")
            continue
        
        comment_on_video(browser, url)

        db_update_status(vid)
        
        print(vid + ' processed')
        print('================')
        print('')
        
        time.sleep(5)
        
  
   
    
#selenium_login(usr, pwd)
#selenium_enter_weibo()
if __name__ == "__main__":
    db_create_db()
    db_clear_db()

    os.system('taskkill /F /im chrome.exe /T')
       
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\Users\dd\AppData\Local\Google\Chrome\User Data")
    options.add_argument('--profile-directory=Default')
    #options.add_argument('headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
    browser.get('https://www.youtube.com/')
    time.sleep(10)
    
    comment_to_videos(browser)
            
    browser.close()

