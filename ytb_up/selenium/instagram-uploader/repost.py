
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
    url = url.replace('https://twitter.com/','').strip()
    if '?' in url:
        return url.split('?')[0]
    return url
    
 
#https://twitter.com/SMMTips247
def is_video_url(url):
    if not 'https://twitter.com/' in url:
        return False

    url = url.replace('https://twitter.com/','').strip()
    if '?' in url:
        url = url.split('?')[0]
        
    if len(url) > 16:
        return False
    
    return True
    

#2021-11-02T20:06:35.000Z
def convet_datatime_to_seconds(date_str):
    print(date_str)
    #2021-10-18 09:41
    dd_str = date_str.split('T')[0]
    dd1 = dd_str.split('-')
    yy = int(dd1[0])
    mm = int(dd1[1])
    dd = int(dd1[2])
    
    return datetime.datetime(yy, mm, dd, 0, 0, 0).timestamp()
    

    
def get_usr_from_url(url):
    #https://weibo.com/u/6207240934?aa
    url = url.replace('https://weibo.com/u/','')
    usr = url.split('?')[0]
    return url
 


def repost(browser, url):
    print('url:' + url)
    browser.get(url)
    
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, 700);")
    
    time.sleep(5)
    
    
    tweets = browser.find_elements_by_xpath('//article[@aria-labelledby]')
    print(len(tweets))
    
    for artical in tweets:
        t = artical.find_elements_by_xpath('.//time[@datetime]')
        create_time = convet_datatime_to_seconds(t.get_attribute('datetime'))
        if time.time() - 3600 * 24 > create_time:
            continue
            
        like_div = artical.find_elements_by_xpath('.//div[@data-testid="like"]')
        like_span = like_div.find_elements_by_xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
        
        count = int(like_span.get_attribute("innerHTML"))
        if count > 3:
            retweet_div = artical.find_elements_by_xpath('.//div[@data-testid="retweet"]')
            retweet_div.click()
            time.sleep(1)
            artical.retweet_div('.//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
            
            break
            

    
        

#(1727, '7690934847')
def start_repost(browser):
    browser.get('https://twitter.com/AutoPostSocial_/following')
    time.sleep(10)
    browser.execute_script("window.scrollTo(0, 700);")
    time.sleep(5)
    video_links = browser.find_elements_by_xpath("//a[@class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l']")
    
    links = []
    idx = 0
    for url_ele in video_links:
        #print(url_ele)
        url = url_ele.get_attribute('href')
        #print(url)
        if not is_video_url(url):
            continue
             
        links.append(url)
        
    for url in links:
        idx += 1
        print("start=={}======{} of {}==========".format(url,idx ,len(video_links)))
        
        vid = get_uid_from_url(url)
        if db_is_video_already_commented(vid):
            print(url + " already processed")
            continue
        
        repost(browser, url)

        db_update_status(vid)
        
        print(vid + ' processed')
        print('================')
        print('')
        
        time.sleep(10)
        
        break
        
  

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
        
    start_repost(browser)
            
    browser.close()

