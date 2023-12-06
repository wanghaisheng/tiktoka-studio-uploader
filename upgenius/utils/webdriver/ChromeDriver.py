import undetected_chromedriver.v2 as uc
import tldextract
import ssl
import pickle, os, time
RANDOM_USERAGENT = 'random'

ssl._create_default_https_context = ssl._create_unverified_context
class ChromeDriver(object):
    '''
    自定义驱动
    '''
    def __init__(self,
                 cookies_folder_path: str,
                 extensions_folder_path: str,
                 host: str = None,
                 port: int = None,
                 private: bool = False,
                 full_screen: bool = False,
                 headless: bool = False,
                 language: str = 'en-us',
                 manual_set_timezone: bool = False,
                 user_agent: str = None,
                 load_proxy_checker_website: bool = False
                 ):
        self.cookies_folder_path = cookies_folder_path
        options = uc.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = uc.Chrome(version_main=91, options=options)
        if full_screen:
            self.driver.fullscreen_window()

        try:
            change_timezone_id = None
            for (dirpath, _, filenames) in os.walk(extensions_folder_path):
                for filename in filenames:
                    if filename.endswith('.xpi') or filename.endswith('.zip'):
                        addon_id = self.driver.install_addon(os.path.join(dirpath, filename), temporary=False)

                        if 'change_timezone' in filename:
                            change_timezone_id = addon_id

            while len(self.driver.window_handles) > 1:
                time.sleep(0.5)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.close()

            self.driver.switch_to.window(self.driver.window_handles[0])

            if change_timezone_id is not None and manual_set_timezone:
                if host is not None and port is not None:
                    self.open_new_tab('https://whatismyipaddress.com/')
                    time.sleep(0.25)

                self.open_new_tab('https://www.google.com/search?client=firefox-b-d&q=my+timezone')
                time.sleep(0.25)

                self.driver.switch_to.window(self.driver.window_handles[0])

                input('\n\n\nSet timezone.\n\nPress ENTER, when finished. ')

                while len(self.driver.window_handles) > 1:
                    time.sleep(0.5)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self.driver.close()

                self.driver.switch_to.window(self.driver.window_handles[0])
            elif load_proxy_checker_website and host is not None and port is not None:
                self.driver.get('https://whatismyipaddress.com/')
        except:
            while len(self.driver.window_handles) > 1:
                time.sleep(0.5)
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.close()

    def get(self, url: str) -> bool:
        clean_current = self.driver.current_url.replace('https://', '').replace('www.', '').strip('/')
        clean_new = url.replace('https://', '').replace('www.', '').strip('/')

        if clean_current == clean_new:
            return False

        self.driver.get(url)

        return True

    def switch_to_frame(self, address):
        '''
        切换iframe
        :param index:
        :return:
        '''
        address_iframe = self.find_element_by_xpath(address)
        self.driver.switch_to.frame(address_iframe)

    def switch_to_default(self):
        '''
        切换回主文档
        :return:
        '''
        self.driver.switch_to.default_content()

    def find_element_by_xpath(self, xpath):
        '''
        通过XPath定位元素
        :param xpath:
        :return:
        '''
        return self.driver.find_element("xpath", xpath)
        # return self.driver.find_element_by_xpath(xpath)

    def find_element_by_name(self, name):
        '''
        根据name定位元素
        :param name:
        :return:
        '''
        return self.driver.find_element("name", name)
        # return self.driver.find_element_by_name(name)

    def find_element_by_id(self, id):
        '''
        通过ID定位元素
        :param xpath:
        :return:
        '''
        return self.driver.find_element("id", id)
        # return self.driver.find_element_by_id(id)

    def find_elements_by_id(self, id):
        '''
        通过ID定位元素
        :param xpath:
        :return:
        '''
        return self.driver.find_elements("id", id)
        # return self.driver.find_elements_by_id(id)

    def find_element_by_class_name(self, class_name):
        '''
        通过class_name定位元素
        :param xpath:
        :return:
        '''
        return self.driver.find_element("class_name", id)
        # return self.driver.find_element_by_class_name(class_name)

    def has_cookies_for_current_website(self, account: str = "", create_folder_if_not_exists: bool = True) -> bool:
        return os.path.exists(
            self.__cookies_path(account,
                create_folder_if_not_exists=create_folder_if_not_exists
            )
        )

    def __cookies_path(self, account: str = "", create_folder_if_not_exists: bool = True) -> str:
        url_comps = tldextract.extract(self.driver.current_url)
        formatted_url = url_comps.domain + '.' + url_comps.suffix + '.' + account

        return os.path.join(
            self.cookies_folder_path,
            formatted_url + '.pkl'
        )

    def save_cookies(self, account) -> None:
        pickle.dump(
            self.driver.get_cookies(),
            open(self.__cookies_path(account), "wb")
        )

    def load_cookies(self, account) -> None:
        '''
        加载cookies
        :return:
        '''
        if not self.has_cookies_for_current_website(account):
            self.save_cookies(account)
            return

        cookies = pickle.load(open(self.__cookies_path(account), "rb"))

        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def refresh(self) -> None:
        self.driver.refresh()

    def quit(self):
        self.driver.close()
        self.driver.quit()