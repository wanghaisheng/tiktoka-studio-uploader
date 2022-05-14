
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
 
 
def is_video_url(url):
    #print('=========')
    #print(url)
    url = url.replace('https://www.ixigua.com/','').strip()
    if '?' in url:
        url = url.split('?')[0]
    
    #print(url)
    #print(len(url))
    #print(url.isdigit())
    if len(url) == 19 and url.isdigit():
        return True
        
    return False
    
    
def get_uid_from_url(url):
    if not is_video_url(url):
        return 0

    url = url.replace('https://www.ixigua.com/','').strip()
    if '?' in url:
        url = url.split('?')[0]
        
    if len(url) == 19 and url.isdigit():
        return url
        
    return 0
    
 
def convet_datatime_to_seconds(date_str):
    #2021-10-18 09:41
    dd_str = date_str.split(' ')[0]
    dd1 = dd_str.split('-')
    yy = int(dd1[0])
    mm = int(dd1[1])
    dd = int(dd1[2])
    
    return datetime.datetime(yy, mm, dd, 0, 0, 0).timestamp()
    


comments = [
'默默路过',
'大陆北方网友路过',
'赞一个',
'点赞'

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
        #print(content.get_attribute('innerHTML'))
        likes = content.find_element_by_xpath('.//div[@class="commentItem__interaction"]/button/span')
        try:
            count = int(likes.get_attribute('innerHTML').strip())
        except:
            count = 10
        #print(likes.get_attribute('innerHTML'))
        #print('likes:')
        #print(count)
        if count > max_count:
            max_count = count
            max_idx = idx
        idx += 1
    
    if idx == 0:
        return get_comment()
        
    #print(max_idx)
    #print(idx)
    #print(len(comments_section))
    c = comments_section[max_idx]

    txt_div = c.find_element_by_xpath('.//div[@class="commentItem__text"]/pre')
    #print(c.get_attribute('innerHTML'))
    comment = txt_div.text
    comment = remove_emojis(comment)
    print('comment:' + comment)
    if len(comment) > 5:
        return comment + "--赞"
     
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
    
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, 900);")
    time.sleep(3)
     
    #弹幕
    #<input aria-labelledby="danmakuBar__input__placeholder" tabindex="0" type="text" value=""/>
    s_comment_input_xpath = "//input[@aria-labelledby='danmakuBar__input__placeholder']"
    WebDriverWait(browser, 200).until(EC.presence_of_element_located((By.XPATH, s_comment_input_xpath)))
    s_comment_input = browser.find_element_by_xpath(s_comment_input_xpath)
    s_comment_input.send_keys(get_comment())
    time.sleep(1)
    browser.find_element_by_xpath("//button[contains(@class,'danmakuBar__input__send')]").click()

    time.sleep(2)

    
    comments = browser.find_elements_by_xpath('//div[@class="commentItem"]')
    #print(len(comments))
    comment = get_comment2(comments)
    print(comment)
    

    comment_editor_xpath = "//textarea[@class='ant-input']"
    if not is_element_exist(browser,comment_editor_xpath):
        return
        
       
    time.sleep(2)
    
    print(comment)
    editor = browser.find_element_by_xpath(comment_editor_xpath)
    editor.send_keys(comment)
    time.sleep(3)
    
    submit_btn = browser.find_element_by_xpath("//div[@class='input-opt-right']//button")
    submit_btn.click()
    time.sleep(30)
        

#(1727, '7690934847')
def comment_to_videos(browser):
    video_links = browser.find_elements_by_xpath(".//a[@href]")
    
    links = []
    idx = 0
    for url_ele in video_links:
        url = url_ele.get_attribute('href')
        if not is_video_url(url):
            continue
             
        links.append(url)
        
    for url in links:
        #print(url)
        #continue
        idx += 1
        print("start=={}======{} of {}==========".format(url,idx ,len(links)))
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
        #break
  
   
    
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
    browser.get('https://www.ixigua.com/')
    time.sleep(10)
    
    comment_to_videos(browser)
            
    browser.close()

