from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from configparser import ConfigParser
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\usman\VsCode Projects\Youtube Commenter Bot\localhost"
file = "config.ini"
config = ConfigParser()
config.read(file)
EMAIL = config['Account']['EMAIL']
PASSWORD = config['Account']['PASSWORD']
YOUTUBE_URL = "https://www.youtube.com/watch?v=nOv0mehKyyw"
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36")
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
action = ActionChains(driver)
driver.implicitly_wait(10)
driver.get("https://www.google.com/intl/en-GB/gmail/about/")
sign_in = driver.find_element(By.XPATH, '//a[@data-action="sign in"]')
action.move_to_element(sign_in).perform()
action.click(on_element=sign_in)
action.perform()

while True:
    try:
        use_accounts = driver.find_elements(By.XPATH, "(//ul)[1]/li")
        if  len(use_accounts) > 0:
            account = use_accounts[len(use_accounts) - 1]
            account.click()
    except:
        pass

    time.sleep(1)
    email_element = driver.find_element(By.XPATH, "//input[@type='email']")
    action.move_to_element(email_element).perform()
    action.click(on_element=email_element)
    action.perform()

    for key in EMAIL:
        time.sleep(0.2)
        email_element.send_keys(key)
    email_element.send_keys(Keys.ENTER)

    try:
        time.sleep(1)
        next_button = driver.find_element(By.XPATH, '//div[@id = "next"]')
        action.move_to_element(next_button).perform()
        action.click(on_element=next_button)
        action.perform()
    except:
        break

time.sleep(1)
password_input = driver.find_element(By.XPATH, "//input[@type='password']")
for key in PASSWORD:
    time.sleep(0.2)
    password_input.send_keys(key)
password_input.send_keys(Keys.ENTER)

time.sleep(1)
driver.get(YOUTUBE_URL)
time.sleep(2)
driver.execute_script("window.scrollTo(0, 500)") 
time.sleep(2)
comment_box = driver.find_element(By.XPATH, "//div[@id='placeholder-area']")
comment_box.click()
msg_box = driver.find_element(By.XPATH, "//div[@id='contenteditable-root']")


# comment msg here
for key in "NICE":
    msg_box.send_keys(key)
driver.implicitly_wait(10)
submit_comment = driver.find_element(By.XPATH, '(//a[@class="yt-simple-endpoint style-scope ytd-button-renderer"])[7]')
submit_comment.click()
