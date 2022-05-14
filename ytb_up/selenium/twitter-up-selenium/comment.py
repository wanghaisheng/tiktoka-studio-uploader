
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
    #print(date_str)
    dd_str = date_str.split('T')[0]
    dd1 = dd_str.split('-')
    #print(dd1)
    yy = int(dd1[0])
    mm = int(dd1[1])
    dd = int(dd1[2])
    
    return datetime.datetime(yy, mm, dd).timestamp()
    


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F900-\U0001F9FF"  # flags (iOS)
                             "]+", re.UNICODE)
    return re.sub(emoj, '', data)


def get_num(fname):
    return "".join([c for c in fname if c.isdigit() ]).rstrip()

    
 
def is_validade_url(url):
    url = url.replace('https://twitter.com/','')
    if '?' in url:
        url = url.split('?')[0]
 
    if len(url) > 16:
        return False
    return True

def get_uid_from_url(url):
    if not is_validade_url(url):
        return ''

    url = url.replace('https://twitter.com/','')
    if '?' in url:
        url = url.split('?')[0]
 
    return url

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
    return get_comment()
    if len(comments_section) < 1:
        return get_comment()
    
    idx = 0
    max_count = 0
    max_idx = 0
    for content in comments_section:
        likes_div = content.find_element_by_xpath('.//div[@data-testid="like"]')
        likes_label = likes_div.get_attribute('aria-label')
        #print(likes_label)
        
        #like_span = likes_div.find_element_by_xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
        count = int(get_num(likes_label))
        #print(count)
        if count > 5:
            max_idx = idx
            idx += 1
            break
            
        print(count)
        if count > max_count:
            max_count = count
            max_idx = idx
        idx += 1
     
    print(max_idx)
    #print(idx)
    
    c = comments_section[max_idx]
    #print(c.get_attribute('innerHTML'))
    #<div class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0" 
    txt_div = c.find_element_by_xpath('.//div[@class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"]/span')
    comment = txt_div.get_attribute("innerHTML")
    #print(comment)
    comment = remove_emojis(comment)
    if len(comment) > 5 and len(comment) < 200:
        return comment + "--thumb up"
    
    if len(comment) >= 200:
        return comment[0:200] + "--thumb up"
        
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
 
 
def comment_on_tweet(browser, url):
    print('url:' + url)
    browser.get(url)
    
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, 700);")
    
    time.sleep(5)
    
    
    tweets = browser.find_elements_by_xpath('//article[@aria-labelledby]')
    print(len(tweets))
    tweet_urls = []
    for artical in tweets:
        #print(artical.get_attribute('innerHTML'))
        try:
            t = artical.find_element_by_xpath('.//time[@datetime]')
            create_time = convet_datatime_to_seconds(t.get_attribute('datetime'))
            if time.time() - 3600 * 24 * 10 > create_time:
                continue
        except:
            continue
        like_div = artical.find_element_by_xpath('.//div[@data-testid="like"]')
        #print(like_div.get_attribute('innerHTML'))
        try:
            like_span = like_div.find_element_by_xpath('.//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
            count = int(like_span.get_attribute("innerHTML"))
        except:
            count = 0
        if count > 2:
            a = artical.find_element_by_xpath('.//a[@class="css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"]')
            tweet_urls.append( a.get_attribute('href'))
    
    print(tweet_urls)
    for url in tweet_urls:
        print(url)
        browser.get(url)
    
        time.sleep(5)
        browser.execute_script("window.scrollTo(0, 400);")
        
        time.sleep(5)
        
        re_container = browser.find_elements_by_xpath('//div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]')
        #print(re_container.get_attribute('innerHTML'))
        comment = get_comment2(re_container)
        print(comment)
        
        editor = browser.find_element_by_xpath("//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
        editor.send_keys(comment)
        time.sleep(3)
        btn = browser.find_element_by_xpath("//span[@class='css-901oao css-16my406 css-bfa6kz r-poiln3 r-a023e6 r-rjixqe r-bcqeeo r-qvutc0']//span[1]")
        btn.click()
        
        time.sleep(5)
        #data-testid="retweet" 
        retweet_xpath = "//div[@data-testid='retweet']"
        browser.find_element_by_xpath(retweet_xpath).click()
        time.sleep(0.5)
        browser.find_element_by_xpath('//div[@data-testid="retweetConfirm"]').click()
            
    
        time.sleep(3)
        

#(1727, '7690934847')
def start_comment(browser,usr):
    browser.get('https://twitter.com/{}/following'.format(usr))
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
        if not is_validade_url(url):
            continue
             
        links.append(url)
        
    for url in links:
        idx += 1
        print("start=={}======{} of {}==========".format(url,idx ,len(video_links)))
        
        vid = get_uid_from_url(url)
        print(vid)
        if db_is_video_already_commented(vid):
            print(url + " already processed")
            continue
        
        comment_on_tweet(browser, url)

        db_update_status(vid)
        
        print(vid + ' processed')
        print('================')
        print('')
        
        time.sleep(10)
        
        break
    
  

def current_milli_time():
    return round( (time.time() + 3600* 24 ) *1000) 
    
    
#selenium_login(usr, pwd)
#selenium_enter_weibo()
if __name__ == "__main__":
    os.system('taskkill /F /im chrome.exe /T')
    
    db_create_db()
    db_clear_db()
    
    parser = optparse.OptionParser()
    parser.add_option( '--usr', default='AutoPostSocial_', help='Specifiy user name')
    
    options, args = parser.parse_args()
    usr= options.usr
    
    usr_dir = os. getcwd() + "\\" + usr + '_profile'
    print(usr_dir)
    Path(usr_dir).mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=" + usr_dir)
   
    options.add_argument('--profile-directory=Default')
    #options.add_argument('headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options = options)
    
    
    start_comment(browser,usr)
    #time.sleep(1000)  
    browser.close()

