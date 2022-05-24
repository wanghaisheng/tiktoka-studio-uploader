from lib2to3.pgen2 import driver
from re import A
from ssl import Options
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as uc
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from random import randint, random




list = ["살면서 우리가 해야 할 말은",
"힘을 내세요라는 말입니다.",
"그 말을 들을 때 정말 힘이 나거든요.",
"오늘 이 말을 꼭 해 보도록 하세요.",
"그러면 당신도 힘을 얻게 될 테니까요.",

"살면서 우리가 해야 할 말은",
"걱정하지 마세요라는 말입니다.",
"그 말을 들을 때 정말 걱정이 사라지거든요.",
"오늘 이 말을 꼭 들려 주세요.",
"그러면 당신도 걱정이 줄어들 테니까요.",

"살면서 우리가 해야 할 말은",
'"용기를 잃지 마세요"라는 말입니다.',
"그 말을 들을 때 정말 용기가 생겨나거든요.",
"오늘 이 말을 꼭 속삭이세요.",
"그러면 당신도 용기를 얻게 될 테니까요.",

"살면서 우리가 해야 할 말은 조건없이",
'"용서합니다"라는 말입니다.',
"그 말을 들을 때 정말 감격하거든요.",
"그러면 당신도 용서를 받게 될 테니까요.",

"살면서 우리가 해야 할 말은",'"감사합니다"라는 말입니다.',
"그 말을 들을 때 정말 따사롭고 푸근해 지거든요.",
"오늘 이 말을 꼭 또렷하게 해 보세요.",
"그러면 당신도 감사를 받게 될 테니까요.",

"살면서 우리가 해야 할 말은",
'"아름다워요"라는 말입니다.',
"그 말을 들을 때 정말 따사롭고 환해 지거든요.",
"오늘 이 말을 꼭 소근거리세요.",
"그러면 당신도 아름다워지게 될 테니까요.",
       
"살면서 우리가 해야 할 말은",
'"사랑해요"라는 말입니다.',
"그 말을 들을 때 정말 사랑이 깊어지거든요.",
"오늘 이 말을 꼭 하셔야 해요.",
"그러면 당신도 사랑을 받게 될 테니까요"]

print(len(list))
def delay(n):
    time.sleep(randint(2, n))

if __name__ == "__main__":

    id = input("write your id : ")
    pw = input("write your pw : ")
    driver = uc.Chrome()

    options = {}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    # chrome_options.add_argument("--headless")
    # driver = uc.Chrome("C:/Users/soo86/Desktop/chromedriver_win32 (1)/chromedriver.exe", options=chrome_options)
    # driver = uc.Chrome("C:/Users/soo86/Desktop/chromedriver_win32 (1)/chromedriver.exe",options=options)




    driver.get("https://www.youtube.com")

    print("enter " + driver.title)
    delay(5)

    # click SIGN IN button
    item = driver.find_element_by_css_selector("ytd-masthead div#buttons ytd-button-renderer a")
    item.click()
    delay(5)

    # login google account
    driver.find_element_by_id("identifierId").send_keys(id)
    driver.find_element_by_id("identifierNext").click()
    delay(5)

    password_locator = (By.CSS_SELECTOR, 'div#password input[name="password"]')
    WebDriverWait(driver, 10).until(
        expect.presence_of_element_located(password_locator)
    )
    password = driver.find_element(*password_locator)
    WebDriverWait(driver, 10).until(
        expect.element_to_be_clickable(password_locator)
    )
    password.send_keys(pw)
    driver.find_element_by_id("passwordNext").click()
    delay(5)

    print("wait for login ...")
    WebDriverWait(driver, 300).until(
        expect.presence_of_element_located((By.CSS_SELECTOR, "ytd-masthead button#avatar-btn"))
    )
    print("login ok")
    time.sleep(5)
    search = driver.find_element(by=By.CSS_SELECTOR, value="ytd-masthead form#search-form input#search")
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//form[@id='search-form']//div[@id='container']//div[@id='search-input']//input[@id='search']")))
    print(search)
    print(element)
    time.sleep(1)
    search.send_keys(Keys.ENTER)
    print("클릭 완료")
    time.sleep(5)
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Message @Ticketing'][data-slate-editor='true'][role='textbox']"))).send_keys("1분 1000만원")
    search.send_keys("1분 1000만원")
    print("검색 완료")
    search.submit()
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='button primary' and contains(@id, 'termsPopup_lbConfirm')]"))).click()

    delay(5)
    

    item = driver.find_element(by=By.CSS_SELECTOR, value="ytd-search a#video-title")
    item.click()
    delay(5)

    # scroll to the bottom in order to load the comments


    print("wait for comments to load ...")
    # WebDriverWait(driver, 10).until(
    #     expect.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer"))
    # )

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    driver.execute_script("window.scrollTo(0, 2500);")
    WebDriverWait(driver, 10).until(
    expect.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer"))
    )
   

    count = 0
    while True:
        a = randint(0,33)
        b = randint(1,10)
        c = randint(1,9)
        print(a)
        # time.sleep(5)


        # driver.find_element_by_id('trigger').click()
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menu"]/a[2]'))).click()
        time.sleep(3+c)
        driver.find_element_by_id('placeholder-area').click()
        time.sleep(2+c)
        inputBox = driver.find_element_by_id('contenteditable-root')
        if c == 1:
            inputBox.send_keys("좋은 글귀 " + str(count)+str(a)+str(b)+str(c)+str(a)+str(b)+str(a)+str(c)+str(b)+str(a)+str(c)+str(b)+str(c)+" 번 : " +list[a] + "안녕하세요 여러분들 천만원 저 주세요!!!"+str(a)+str(b)+str(c))
        elif c == 2 :
            inputBox.send_keys("안녕안녕 천만원 받으러 왓어 ㅋㅋㅋ")
        elif c == 3 :
            inputBox.send_keys("진짜 부탁인데 천만원 나 주면 안되냐")
        elif c == 4 :
            inputBox.send_keys("모두 좋은 하루 되세요~~")
        elif c == 5 :
            inputBox.send_keys(str(a)+str(b)+str(c)+str(a)+str(b)+str(a)+str(c)+str(b)+str(a)+str(c)+str(b)+str(c))
        elif c == 6 :
            inputBox.send_keys(str(a)+str(b)+str(c))
        elif c == 7 :
            inputBox.send_keys("저 매크로임 포기하셈 코드 : " + str(count))
        elif c == 8 :
            inputBox.send_keys(str(a)+str(b)+str(c)+str(b)+str(a)+str(a))
        elif c == 9 :
            inputBox.send_keys("매크로 방지는 해두신거임?" + str(c))
            
        inputBox.send_keys(Keys.CONTROL, Keys.ENTER)
        time.sleep(55+b)
        count += 1 
        # driver.refresh()


