import time
import random
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def virtual_human(key, element):
    for j in key:
        element.send_keys(j)
        time.sleep(float("{:.2f}".format(random.uniform(0.1, 0.4))))


def youtube_login(email, password):

    op = webdriver.ChromeOptions()
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument('--disable-gpu')
    op.add_argument("--disable-infobars")
    op.add_argument("--log-level=3")
    op.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=op)
    driver.execute_script("document.body.style.zoom='80%'")
    driver.get('https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https'
               '%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dht'
               'tps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

    # finding email field and putting our email on it
    email_field = driver.find_element_by_xpath('//*[@id="identifierId"]')
    virtual_human(email, email_field)
    driver.find_element_by_id("identifierNext").click()
    time.sleep(5)

    # finding pass field and putting our pass on it
    find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located(find_pass_field))
    pass_field = driver.find_element(*find_pass_field)
    WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable(find_pass_field))
    virtual_human(password, pass_field)
    driver.find_element_by_id("passwordNext").click()
    time.sleep(5)
    print("password - done")
    WebDriverWait(driver, 200).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
    return driver


email = config.email
password = config.password

driver = youtube_login(email, password)
f = open("url.txt", "r")
urls = f.readlines()
for url in urls:
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(2)
    main_comments = driver.find_elements_by_css_selector('#contents #comment')
    iterator = 0
    replies = driver.find_elements_by_xpath('//*[@id="reply-button-end"]')
    for reply in replies:
        reply.click()
        driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
        time.sleep(float("{:.2f}".format(random.uniform(0.1, 0.4))))

    comment_box = driver.find_elements_by_xpath('//*[@id="contenteditable-root"]')
    submit = driver.find_elements_by_css_selector('#submit-button')
    print(len(comment_box))

    for i in range(len(main_comments)):
        mc = main_comments.pop(0)
        time.sleep(1)
        ActionChains(driver).move_to_element(comment_box[iterator]).click(comment_box[iterator]).perform()
        add_comment_onit = comment_box[iterator]
        virtual_human("comment", add_comment_onit)
        time.sleep(1)
        submit[iterator].click()
        iterator += 1