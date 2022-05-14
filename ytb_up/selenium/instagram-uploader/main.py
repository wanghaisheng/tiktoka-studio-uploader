import os
import time
from selenium import webdriver
from credentials import username, password, description_file
from selenium.webdriver.common import action_chains
import pickle
from webdriver_manager.chrome import ChromeDriverManager
import autoit
import json


def bw_init():
    # FIREFOX
    user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
    profile = webdriver.FirefoxProfile() 
    profile.set_preference("general.useragent.override", user_agent)
    driver = webdriver.Firefox(profile)
    driver.set_window_size(360,640)
    return driver


def login(driver):
    url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
    driver.get(url)
    time.sleep(3)

    field = driver.find_element_by_css_selector("input[type='text']")
    field.send_keys(username)
    field = driver.find_element_by_css_selector("input[type='password']")
    field.send_keys(password)
    time.sleep(2)
    button=driver.find_elements_by_xpath("//*[contains(text(), 'Log In')]")
    button[0].click()

    time.sleep(5)
    button=driver.find_elements_by_xpath("//*[contains(text(), 'Not Now')]")
    if len(button) > 0:
        button[0].click()

    time.sleep(5)
    button=driver.find_elements_by_xpath("//*[contains(text(), 'Cancel')]")
    if len(button) > 0:
        button[0].click()
        
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    

def enter_ins(driver):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    driver.get('https://www.instagram.com/')
    
    for cookie in cookies:
        driver.add_cookie(cookie)
 
    driver.get('https://www.instagram.com/')
    time.sleep(2)

def post(driver, img_path, img_caption):
    try:
        button = driver.find_elements_by_css_selector('[aria-label="New Post"]')
        button[0].click()
    except:
        login(driver)
        exit(-1)
        
    #driver.switch_to.active_element.send_keys(r'D:\obsolute\social_media\instagram-uploader\img0000000.png');

    time.sleep(1)
    #hWnd = autoit.win_get_handle("File Upload")
    #print(hWnd)
    #autoit.control_send(hWnd,"Edit1",r'D:\obsolute\social_media\instagram-uploader\img0000000.png') 
    #autoit.control_send("Open","Edit1","{ENTER}")

    autoit.win_wait("[CLASS:#32770;TITLE:File Upload]", 10)
    autoit.control_send("[CLASS:#32770;TITLE:File Upload]", "Edit1", img_path)
    autoit.control_click("[CLASS:#32770;TITLE:File Upload]", "Button1")


    #os.system('autokey-run -s select_image')

    #img_input = driver.find_element_by_xpath("//nav//div[@class='_8MQSO ZoygQ ']//div[1]//form[1]//input[1]")
    img_input = driver.find_element_by_xpath("//div[@id='react-root']//form[1]//input[1]")
    img_input.send_keys(img_path)



    time.sleep(10)
    button=driver.find_elements_by_xpath("//*[contains(text(), 'Expand')]")
    if len(button) > 0:
        button[0].click()

    time.sleep(10)
    button=driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")
    button[0].click()

    time.sleep(10)
    field = driver.find_elements_by_tag_name('textarea')[0]
    field.click()


    field.send_keys(img_caption)

    time.sleep(5)
    button = driver.find_elements_by_xpath("//*[contains(text(), 'Share')]")[1]

    driver.execute_script("arguments[0].scrollIntoView();", button);
    action = action_chains.ActionChains(driver)
    action.move_to_element(button)
    action.click()
    action.perform()
    
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

    time.sleep(10)
    driver.quit()
    
if __name__ == "__main__":
    bw = bw_init()
    if not os.path.isfile('cookies.pkl'):
        login(bw)
    
    enter_ins(bw)
    
    #"word": "Work hard in silence, let your success be your noise.",
    #"author": "Anonymous",
    #"img_idx": 0
  
    with open('D:\\obsolute\\social_media\\quotefancy\\result.json', encoding='utf-8') as f:
        quotes = json.load(f)
        
    for q in quotes:
        word = q['word']
        img_idx = q['img_idx']
        file_name = "D:\quote_image\\img{0:07d}.png".format(img_idx)
        if not os.path.isfile(file_name):
            continue
        
        print(file_name)
        print(word)
        post(bw,file_name,word)
        
        os.remove(file_name)
        break
        
    














