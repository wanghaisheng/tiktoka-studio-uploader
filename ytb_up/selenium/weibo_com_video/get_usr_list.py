
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
from db_helper import *
import datetime


def milli_time_of_next_day():
    return round( (time.time() + 3600* 24 ) *1000)

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
    

 
def get_usr_from_url(url):
    #https://weibo.com/u/6207240934?aa
    #print(url)
    url = url.replace('https://weibo.com/u/','')
    usr = url.split('?')[0]
    #print(usr)
    return usr
 
 
def get_last_post_time(browser):
    posts = browser.find_elements_by_xpath('//div[@class="vue-recycle-scroller__item-view"]')

    for post in posts:
        post_time = post.find_element_by_xpath(".//div[@class='woo-box-flex woo-box-alignCenter woo-box-justifyCenter head-info_info_2AspQ']//a").get_attribute('title')
        print(post_time)
                
        post_sec = convet_datatime_to_seconds(post_time)
        print(post_sec)
        if post_sec is None:
            return 0
        return post_sec
 
    return 0
 
def get_recommended_usr(browser):
    WebDriverWait(browser, 200).until(EC.presence_of_element_located((By.XPATH, '//a[@class="ALink_none_1w6rm"]')))
    usr_link_elms = browser.find_elements_by_xpath('//a[@class="ALink_none_1w6rm"]')
    
    usr_links = []
    for ele in usr_link_elms:
        url = ele.get_attribute('href')
        #print(url)
        if 'https://weibo.com/u/' in url :
            if not 'page' in url:
                #print(url)
                usr_links.append(url)

    if len(usr_links) < 1:
        return "https://weibo.com/u/6267734888"
    
    usr_links = list(dict.fromkeys(usr_links))
    print(usr_links)
    idx = randrange(0,len(usr_links))
    print('next idx ' + str(idx))
    usr_link = usr_links[idx]
    usr = get_usr_from_url(usr_link)
    db_add_usr(usr)
    
    return usr_link
 
 
def check_user(browser,usr_link):
    print('usr_link:' + usr_link)
    browser.get(usr_link)
    time.sleep(10)
    
    post_time = get_last_post_time(browser)
    
    cur_secs = time.time()
    #print(cur_secs)
    if cur_secs - 10 * 24 * 3600 > post_time:
        usr = get_usr_from_url(usr_link)
        print(usr)
        db_add_usr(usr)
 
    return get_recommended_usr(browser)
 
 

def get_users(browser,comments_section):

    content = comments_section[0]
 
    next_usr_link = content.find_element_by_xpath('.//div[@class="txt"]/a[@class="name"]').get_attribute('href')

    while True:
        count = db_get_usr_count()
        print('========Get usr link {} count {}========='.format(next_usr_link,count))
        next_usr_link = check_user(browser,next_usr_link)
        
        if count > 10000 * 10:
            break

        
    
 
def get_acivate_usr_from_top_search(browser):
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
        get_users(browser,comments_section)
        print('Done =================')
        
        break
        
  
def start(browser):
  
    get_acivate_usr_from_top_search(browser)

def current_milli_time():
    return round( (time.time() + 3600* 24 ) *1000) 
    
    

#selenium_login(usr, pwd)
#selenium_enter_weibo()
if __name__ == "__main__":
    os.system('taskkill /F /im chrome.exe /T')
    #db_create_db()
    
    try_count = 100
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\Users\dd\AppData\Local\Google\Chrome\User Data")
    options.add_argument('--profile-directory=Default')
    #options.add_argument('headless')
    #self.driver = webdriver.Chrome(executable_path=config.get('chromedriver_path'), chrome_options=options)
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
    #start(browser)
    while True:
        try:
            start(browser)
        except:
            print("Error")
            try_count -= 1
            time.sleep(10)
            if try_count < 1:
                break
    
    browser.close()
    #print(db_get_last_usr())
    
    
    
    
    
    

