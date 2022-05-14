
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
    

 
def comment_usr_post(browser, url, days_before,forward):
    browser.get(url)
    
    time.sleep(10)
    
    posts = browser.find_elements_by_xpath('//div[@class="vue-recycle-scroller__item-view"]')
    for post in posts:
        post_time = post.find_element_by_xpath(".//div[@class='woo-box-flex woo-box-alignCenter woo-box-justifyCenter head-info_info_2AspQ']//a").get_attribute('title')
        print(post_time)
        
        post_sec = convet_datatime_to_seconds(post_time)
        cur_secs = time.time()
        if cur_secs - days_before * 24 * 3600 > post_sec :
            #only process post created in [days_before]
            continue
        
        browser.execute_script("window.scrollTo(0, 700);")
        
        footer = post.find_element_by_xpath('.//div[@class="wbpro-scroller-item"]/article/footer')
        
        try:
            votes = footer.find_element_by_xpath('.//span[@class="woo-like-count"]')
            print(votes.text)
            like_count = int(votes.text)
            if like_count < 3:
                continue
        except:
            print('can not get vote')
        #woo-box-flex woo-box-alignCenter woo-box-justifyCenter toolbar_wrap_np6Ug toolbar_cur_JoD5A   
        comment_btn = post.find_element_by_xpath("//div[@class='woo-box-flex woo-box-alignCenter toolbar_left_2vlsY toolbar_main_3Mxwo']")
        comment_btn.click()
        
        time.sleep(5)
        
        #print(post.get_attribute("innerHTML"))
        
        #同时转发
        if forward:
            post.find_element_by_xpath("//span[@class='woo-checkbox-text']").click()

        
        comment = ""
        #//textarea[@action-type='check']
        #//textarea[@action-type='check']
        comments_section_xpath = '//div[@class="con1 woo-box-item-flex"]'
        comments_section = browser.find_elements_by_xpath(comments_section_xpath)
        if len(comments_section) < 1:
            comment = get_comment()
        else:
            txt_div = comments_section[0].find_element_by_xpath('.//div[@class="text"]/span')
            comment = getOnlyTextFromNode(txt_div)
            if len(comment) > 50:
                comment = comment[0 : 50]
            if len(comment) > 5:
                comment = comment + "--赞"
            else:
                comment = get_comment()
        
        editor = browser.find_element_by_xpath("//textarea[@placeholder='发布你的评论']")
        editor.send_keys(comment)
        
        time.sleep(4)
        
        submit_btn = browser.find_element_by_xpath("//button[@class='disabled woo-button-main woo-button-flat woo-button-primary woo-button-m woo-button-round Composer_btn_2XFOD']")
        submit_btn.click()
        
        time.sleep(5)
        break

  

comments = [
'默默路过',
'转发',
'转',
'大陆北方网友路过',
'赞一个',
'默默转发',
'点赞+转发'
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
        likes = content.find_element_by_xpath('.//span[@class="woo-like-count"]')
        print(likes)
        tmp = int(likes.text)
        print(tmp)
        if tmp > max_count:
            max_count = int(likes.text)
            max_idx = idx
        idx += 1
     
    #print(max_idx)
    #print(idx)
    #print(len(comments_section))
    c = comments_section[max_idx]
    
    txt_div = c.find_element_by_xpath('.//div[@class="txt"]')
    comment = getOnlyTextFromNode(txt_div)
    if len(comment) > 5:
        return comment + "--赞"
        
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
 
 
def comment_on_top_search(browser):
    browser.get('https://weibo.com/set/index')
    time.sleep(3)
     
    url = 'https://weibo.com/'
    browser.get(url)
    time.sleep(10)
    
    top_search_xpath = '//div[@class="wbpro-side-card7"]/div[@class="wbpro-side-panel"]'
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, top_search_xpath)))
    top_search_all = browser.find_elements_by_xpath(top_search_xpath)

    idx = randrange(1,len(top_search_all) - 1)
    
    top_search = top_search_all[idx]
    link = top_search.find_element_by_xpath('.//a').get_attribute('href')
    browser.get(link)
    
    time.sleep(10)
    comments_section_xpath = '//div[@node-type="feed_list_repeat"]/div[@class="card-together"]'
     
    posts = browser.find_elements_by_xpath('//div[@class="card-act"]')
    for post in posts:
              
        votes = post.find_element_by_xpath('.//span[@class="woo-like-count"]')
        like_count = int(votes.text)
        if like_count < 5:
            continue
         
        #print(post)
        
        comment_btn = post.find_element_by_xpath('.//a//i[@class="woo-font woo-font--comment toolbar_icon"]')
        comment_btn.click()
        
        time.sleep(15)
        
        comments_section = browser.find_elements_by_xpath(comments_section_xpath)
        span = browser.find_element_by_xpath("//input[@name='forward']")
        print(span)
        span.click()
        
        #//textarea[@action-type='check']
        #//textarea[@action-type='check']
        
        comments_section = browser.find_elements_by_xpath(comments_section_xpath)
        comment = get_comment2(comments_section)
        print(comment)
        
        editor = browser.find_element_by_xpath("//textarea[@action-type='check']")
        editor.send_keys(comment)
        
        time.sleep(10)
        
        submit_btn = browser.find_element_by_xpath(".//a[@class='s-btn-a']")
        submit_btn.click()
        
        time.sleep(10)
        break
        
        

#(1727, '7690934847')
def comment_to_exising_usr(browser):

    rowid = db_get_status()
    users = db_get_usr_list(rowid)
    print(len(users))
    
    for usr in users:
        row_id = usr[0]
        uid = usr[1]
        print(usr)
        
        url = 'https://weibo.com/u/' + uid
        print(url)
        comment_usr_post(browser,url,5,False)
        print("save:" + str(row_id))
        db_update_status(row_id)
        #break
        
  
def comment_to_tech_usr(browser):

    browser.get('https://weibo.com/u/page/follow/1794705261')
    time.sleep(10)
    
    users = browser.find_elements_by_xpath('//a[@class="ALink_none_1w6rm UserFeedCard_left_2XXOA"]')
    urls = []
    for usr in users:
        url = usr.get_attribute('href')
        urls.append(url)
        
    for url in urls:
        row_id = get_usr_from_url(url)
        if db_is_video_already_commented(row_id):
            print(url + " already processed")
            continue
        
        print(url)
        
        comment_usr_post(browser,url,5,True)
        print("save:" + str(row_id))
        db_update_status(row_id)
        break
        
  

def current_milli_time():
    return round( (time.time() + 3600* 24 ) * 1000) 
    
    
#selenium_login(usr, pwd)
#selenium_enter_weibo()
if __name__ == "__main__":

    db_create_db()
    db_clear_db()
    

    parser = optparse.OptionParser()
    parser.add_option( '--op', default='tech', help='指定操作类型，top:热搜，user:普通用户')
    
    options, args = parser.parse_args()
    op= options.op


    os.system('taskkill /F /im chrome.exe /T')
 
    usr_dir = os. getcwd() + "\\" + op + '_profile'
    print(usr_dir)
    Path(usr_dir).mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=" + usr_dir)
    options.add_argument('--profile-directory=Default')
    #options.add_argument('headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
    
    if op == 'user':
        comment_to_exising_usr(browser)
    
    if op == 'top':
        comment_on_top_search(browser)
        
    if op == 'tech':
        comment_to_tech_usr(browser)
        
    browser.close()

