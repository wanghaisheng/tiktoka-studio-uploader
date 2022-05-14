
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
import re
from pathlib import Path

  
def is_element_exist(browser,  elm):
    s = browser.find_elements_by_xpath(xpath=elm)
    if len(s) == 0:
        print("元素未找到:%s" % elm)
        return False
    else:
        print("找到%s个元素：%s" % (len(s), elm))
        return True


 
def convet_datatime_to_seconds(date_str):
    #2021-10-18 09:41
    dd_str = date_str.split(' ')[0]
    dd1 = dd_str.split('-')
    yy = int(dd1[0])
    mm = int(dd1[1])
    dd = int(dd1[2])
    
    return datetime.datetime(yy, mm, dd, 0, 0, 0).timestamp()
    


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F900-\U0001F9FF"  # flags (iOS)
                             "]+", re.UNICODE)
    return re.sub(emoj, '', data)
 
def rm_special_char(fname):
    return "".join([c for c in fname if c.isdigit() ]).rstrip()


comments = [
'thumb up',
'Keep it up',
'Great post'
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
    #if len(comments_section) < 1:
    return get_comment()
    
    #print(comments_section)
    #//button[@class='wpO6b ZQScA ']//div[@class='QBdPU B58H7']//*[name()='svg']
    idx = 0
    max_count = 0
    max_idx = 0
    for content in comments_section:
        print(content.get_attribute('innerHTML'))
        try:
            likes_div = content.find_elements_by_xpath('.//button[@class="FH9sR"]')[0]
            like_txt = likes_div.get_attribute("innerHTML")
            print(like_txt)
            count = int(rm_special_char(like_txt))
        except:
            count = 0
        if count > 5:
            max_idx = idx
            idx += 1
            break
            
        print(count)
        if count > max_count:
            max_count = count
            max_idx = idx
            
        idx += 1
     
    #print(max_idx)
    #print(idx)
    #print(len(comments_section))
    c = comments_section[max_idx]
    
    #<div class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0" 
    txt_div = c.find_element_by_xpath('.//span')
    #//span[normalize-space()='Blah']
    comment = getOnlyTextFromNode(txt_div)
    print(comment)
    comment = remove_emojis(comment)
    if len(comment) > 10 and len(comment) < 100:
        return comment + "--thumb up"
    
    if len(comment) >= 100:
        return comment[0:100] + "--thumb up"
        
    return get_comment()
    
    
    
   

 
def get_usr_from_url(url):
    #https://weibo.com/u/6207240934?aa
    url = url.replace('https://weibo.com/u/','')
    usr = url.split('?')[0]
    return url
 
 
def get_last_post_time():
    browser.get(url)
    posts = browser.find_elements_by_xpath('//div[@class="vue-recycle-scroller__item-view"]')
    for post in posts:
        post_time = post.find_element_by_xpath(".//div[@class='woo-box-flex woo-box-alignCenter woo-box-justifyCenter head-info_info_2AspQ']//a[@title]")
        print(post_time)
        
        post_sec = convet_datatime_to_seconds(post_time)
        return post_sec


def get_postid_from_url(url):
    url = url.replace("https://www.instagram.com/p/",'')
    url = url.split('/')[0]
    
    return url


def comment_on_post(browser,url):
    pid = get_postid_from_url(url)
    
    if db_is_video_already_commented(pid):
        print(url + " already processed")
        return
        
    db_update_status(pid)
        

    browser.get(url)
    time.sleep(5)
    
    comments_section = browser.find_elements_by_xpath("//div[@class = 'C4VMK']")
    comment = get_comment2(comments_section)
    
    print(comment)
    
    time.sleep(10)

    browser.find_element_by_xpath("//form").click()
    editor = browser.find_element_by_xpath("//textarea[@placeholder='添加评论...']")
    time.sleep(1)
    editor.send_keys(Keys.CONTROL + "a");
    editor.send_keys(Keys.DELETE);
    editor.send_keys(comment)
    #editor.send_keys('thumb up')
    
    time.sleep(2)
    #data-testid="post-comment-input-button"
    submit_btn = browser.find_element_by_xpath("//button[@data-testid='post-comment-input-button']")
    submit_btn.click()
    
    time.sleep(5)
 
 
def comment_on_user(browser, url):
    print('url:' + url)
    browser.get(url)
    
    time.sleep(5)
    #browser.execute_script("window.scrollTo(0, 700);")
    #https://www.instagram.com/p/
    all_urls = browser.find_elements_by_xpath("//a[@href]")
    posts = []
    
    #,'https://www.instagram.com/p/'
    
    for url_ele in all_urls:
        url = url_ele.get_attribute('href')
        if 'https://www.instagram.com/p/' in url:
            if '?' in url:
                url = url.split('?')[0]
                
            posts.append(url)
    
    count = 0
    for p in posts:
        comment_on_post(browser,p)
        time.sleep(5)
        
        count += 1
        if count > 10:
            break
    
 
        

#(1727, '7690934847')
def start_comment(browser):
    browser.get('https://www.instagram.com/')
    time.sleep(5)
    self_page_link = browser.find_element_by_xpath("//a[@class='gmFkV']").get_attribute('href')
    browser.get(self_page_link)
    time.sleep(5)
    
    following_url = self_page_link + 'following'
    #print(following_url)
    self_page_link = browser.find_element_by_xpath("//a[contains(@href,'following')]").click()
    time.sleep(5)
    
    followers = browser.find_elements_by_xpath("//a[@class='_2dbep qNELH kIKUG']")
    recommend_followers = browser.find_elements_by_xpath("//a[@class='FPmhX notranslate MBL3Z']")
    
    urls = []
    for f in followers:
        urls.append(f.get_attribute('href'))
    
    for f in recommend_followers:
        urls.append(f.get_attribute('href'))
    
    #print(urls)   
    for url in urls:
        comment_on_user(browser,url)
        break
    
  

def current_milli_time():
    return round( (time.time() + 3600* 24 ) *1000) 
    
    
#selenium_login(usr, pwd)
#selenium_enter_weibo()
if __name__ == "__main__":
    os.system('taskkill /F /im chrome.exe /T')
    
    db_create_db()
    db_clear_db()
    
    usr = 'image_mkt'
    usr_dir = os. getcwd() + "\\" + usr + '_profile'
    print(usr_dir)
    Path(usr_dir).mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=" + usr_dir)
    options.add_argument('--profile-directory=Default')
    #options.add_argument('headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
    
    
    start_comment(browser)
        
    #browser.close()

