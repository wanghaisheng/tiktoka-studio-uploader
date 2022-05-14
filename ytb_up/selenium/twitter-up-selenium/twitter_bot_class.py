from selenium import webdriver
from selenium import common
from selenium.webdriver.common import keys
from webdriver_manager.firefox import GeckoDriverManager
import time

import pickle

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

class TwitterBot:

    """
    A Bot class that provide features of:
        - Logging into your Twitter account
        - Liking tweets of your homepage
        - Searching for some keyword or hashtag
        - Liking tweets of the search results
        - Posting tweets
        - Logging out of your account

    ........

    Attributes
    ----------
    email : str
        user email for Twitter account
    password : str
        user password for Twitter account
    bot : WebDriver
        webdriver that carry out the automation tasks
    is_logged_in : bool
        boolean to check if the user is logged in or not

    Methods
    -------
    login()
        logs user in based on email and password provided during initialisation
    logout()
        logs user out
    search(query: str)
        searches for the provided query string
    like_tweets(cycles: int)
        loops over number of cycles provided, scrolls the page down and likes the available tweets on the page in each loop pass
    """
    

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.bot = driver
        self.is_logged_in = False


    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(60 * 2)

        
        pickle.dump( bot.get_cookies() , open("cookies.pkl","wb"))
        time.sleep(2)
        self.is_logged_in = True
        
    def enter(self):
        bot = self.bot
        cookies = pickle.load(open("cookies.pkl", "rb"))
        bot.get('https://twitter.com/')
        
        for cookie in cookies:
            bot.add_cookie(cookie)
     
        bot.get('https://twitter.com/')
        time.sleep(2)
        
        #have a check??
        self.is_logged_in = True
        
        pickle.dump( bot.get_cookies() , open("cookies.pkl","wb"))


    def logout(self):
        if not self.is_logged_in:
            return 

        bot = self.bot
        bot.get('https://twitter.com/home')
        time.sleep(4)

        try:
            bot.find_element_by_xpath("//div[@data-testid='SideNav_AccountSwitcher_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@data-testid='SideNav_AccountSwitcher_Button']").click()

        time.sleep(1)

        try:
            bot.find_element_by_xpath("//a[@data-testid='AccountSwitcher_Logout_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(2)
            bot.find_element_by_xpath("//a[@data-testid='AccountSwitcher_Logout_Button']").click()

        time.sleep(3)

        try:
            bot.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()

        time.sleep(3) 
        self.is_logged_in = False


    def search(self, query=''):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot

        try:
            searchbox = bot.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']")
        except common.exceptions.NoSuchElementException:
            time.sleep(2)
            searchbox = bot.find_element_by_xpath("//input[@data-testid='SearchBox_Search_Input']")

        searchbox.clear()
        searchbox.send_keys(query)
        searchbox.send_keys(keys.Keys.RETURN)
        time.sleep(10)  


    def like_tweets(self, cycles=10):
        if not self.is_logged_in:
            raise Exception("You must log in first!") 

        bot = self.bot   

        for i in range(cycles):
            try:
                bot.find_element_by_xpath("//div[@data-testid='like']").click()
            except common.exceptions.NoSuchElementException:
                time.sleep(3)
                bot.execute_script('window.scrollTo(0,document.body.scrollHeight/1.5)') 
                time.sleep(3)
                bot.find_element_by_xpath("//div[@data-testid='like']").click()

            time.sleep(1)
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight/1.5)') 
            time.sleep(5)

      
    def post_tweets(self,tweetBody,img_path):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot  

        try:
            bot.find_element_by_xpath("//a[@data-testid='SideNav_NewTweet_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(4) 
        body = tweetBody

        try:
            bot.find_element_by_xpath("//div[@role='textbox']").send_keys(body)
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@role='textbox']").send_keys(body)
        
        if not img_path == None:
            img_ele = bot.find_element_by_xpath("//input[@class='r-8akbif r-orgf3d r-1udh08x r-u8s1d r-xjis5s r-1wyyakw']")
            img_ele.send_keys(img_path)

        time.sleep(4)
        bot.find_element_by_class_name("notranslate").send_keys(keys.Keys.ENTER)
        bot.find_element_by_xpath("//div[@data-testid='tweetButton']").click()
        time.sleep(10) 
        bot.close()
