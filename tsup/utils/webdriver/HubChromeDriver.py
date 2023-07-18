import sys

from selenium.webdriver.chrome.service import Service
import tldextract
import socket
import ssl
import pickle, os, time
import json
import uuid
RANDOM_USERAGENT = 'random'
from selenium import webdriver
import traceback
ssl._create_default_https_context = ssl._create_unverified_context

class HubChromeDriver(object):
    '''
    自定义驱动
    '''
    def __init__(self,
                 cookies_folder_path: str,
                 extensions_folder_path: str,
                 container_name: str,
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
        # 端口
        socket_port = 22558
        group_name = '18946079633的团队'
        api_key = '12b1d1760bc0b886a5d40e87c75e94922398eb8095c21e16b4498d562aca39693cbbbb1378d32bc6e4ea7341238612dc'
        # 调用参数
        data1 = {
            'userInfo': '{\'apiKey\': \'%s\', \'loginGroupName\': \'%s\'}' % (api_key, group_name),
            'action': 'startBrowserByName',
            'browserName': container_name,
            'isHeadless': 0,
            'requestId': str(uuid.uuid4()),
            'isWebDriverReadOnlyMode': 0
        }

        print('初始化参数...')
        # 发送请求
        r = self.send_socket(data1, socket_port)
        if r.get('statusCode') == 0:
            print('正在启动环境...')
            store_port = r.get('debuggingPort')
        else:
            print('环境启动失败')
            exit()

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_experimental_option("debuggerAddress", '127.0.0.1:' + str(store_port))
        driver_path = 'D:/Chrome/chromedriver.exe'
        s = Service(driver_path)

        self.driver = webdriver.Chrome(service=s, options=options)

        # 初始化WebDriver
        print('初始化WebDriver...')
        # 打开环境检测页
        self.driver.get('chrome-extension://%s/index.html' % r.get('backgroundPluginId'))
        print('正在检测环境安全...')
        wait_s = 1
        # 检测环境是否安全，然后运行自己的逻辑
        while True:
            if wait_s >= 30:
                print('===>环境安全检测等待时间超过30秒，退出后续操作')
                break
            data2 = {
                'userInfo': '{\'apiKey\': \'%s\'}' % api_key,
                'action': 'getIsEnterStore',
                'containerName': container_name,
                'requestId': str(uuid.uuid4()),
            }
            # 发送请求
            r = self.send_socket(data2, socket_port)
            if r.get('isEnterStore'):
                print('环境检测通过')
                # 环境检测通过后，可执行自己的脚本逻辑
                self.driver.execute_script('window.open(\'https://www.baidu.com/\');')
                break
            time.sleep(1)
            wait_s += 1

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

    def send_socket(self, params, socket_port):
        try:
            client = socket.socket()
            client.settimeout(300)  # 超时时间
            client.connect(('127.0.0.1', socket_port))
            # 参数后需拼接上  + b'\r\n'，不可删除
            s = json.dumps(params).encode('utf-8') + b'\r\n'
            client.sendall(s)
            rec = client.recv(1024).decode()
            client.shutdown(2)
            # 返回值后面同样存在 '\r\n'，需删除后方可正常转为json
            return json.loads(str(rec).replace('\r\n', ''))
        except Exception as err:
            print(traceback.print_exc())
            print(err)

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
        return self.driver.find_element_by_xpath(xpath)

    def find_element_by_name(self, name):
        '''
        根据name定位元素
        :param name:
        :return:
        '''
        return self.driver.find_element_by_name(name)

    def find_element_by_id(self, id):
        '''
        通过ID定位元素
        :param xpath:
        :return:
        '''
        return self.driver.find_element_by_id(id)

    def find_elements_by_id(self, id):
        '''
        通过ID定位元素
        :param xpath:
        :return:
        '''
        return self.driver.find_elements_by_id(id)

    def find_element_by_class_name(self, class_name):
        '''
        通过class_name定位元素
        :param xpath:
        :return:
        '''
        return self.driver.find_element_by_class_name(class_name)

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