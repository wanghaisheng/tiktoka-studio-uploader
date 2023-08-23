import json
from typing import Dict, List
import os
from tsup.utils.constants import *
from time import sleep
import random
from datetime import datetime, date, timedelta, time
from playwright.async_api import Page, expect

""" Login module """


def domain_to_url(domain: str) -> str:
    """Converts a (partial) domain to valid URL"""
    if domain.startswith("."):
        domain = "www" + domain
    return "http://" + domain


async def format_cookie_file(cookie_file: str):
    """Restore auth cookies from a file. Does not guarantee that the user is logged in afterwards.
    Visits the domains specified in the cookies to set them, the previous page is not restored.
    """
    domain_cookies: Dict[str, List[object]] = {}
    # cookie_file=r'D:\Download\audio-visual\make-reddit-video\auddit\assets\cookies\aww.json'
    with open(cookie_file) as file:
        cookies: List = json.load(file)
        # Sort cookies by domain, because we need to visit to domain to add cookies
        for cookie in cookies:
            if (
                cookie["sameSite"] != "no_restriction"
                or cookie["sameSite"].lower() != "no_restriction"
            ):
                cookie.update(sameSite="None")
            try:
                domain_cookies[cookie["domain"]].append(cookie)
            except KeyError:
                domain_cookies[cookie["domain"]] = [cookie]
    # print(str(domain_cookies).replace(",", ",\n"))

    # cookie.pop("sameSite", None)  # Attribute should be available in Selenium >4
    # cookie.pop("storeId", None)  # Firefox container attribute
    # print("add cookies", domain_cookies[cookie["domain"]])
    # await self.context.add_cookies(cookies)
    return domain_cookies[cookie["domain"]]


async def confirm_logged_in(self) -> bool:
    """Confirm that the user is logged in. The browser needs to be navigated to a YouTube page."""
    try:
        await expect(
            self.page.locator(
                "yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)"
            )
        ).to_be_visible()

        # WebDriverWait(page, 10).until(EC.element_to_be_clickable("avatar-btn")))
        return True
    except TimeoutError:
        return False


def confirm_logged_in_douyin(self) -> bool:
    try:
        self.page.locator(".avatar--1lU_a")
        return True
    except:
        return False


def confirm_logged_in_tiktok(self) -> bool:
    """Confirm that the user is logged in. The browser needs to be navigated to a YouTube page."""
    try:
        self.page.locator(
            "yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)"
        )

        return True
    except TimeoutError:
        return False


# async def loadExistingAccount(credentials: Credentials, messageTransport: MessageTransport, useCookieStore: boolean = true) {
#     try:
#         if os.path.exist(cookiesFilePath)==True and   useCookieStore==True:
#             await login(page, credentials, messageTransport, useCookieStore)
#         else:
#             print()
#     except:
#         if  'Recapcha found':
#             if browser:
#                 await browser.close()
#             else:
#                 break
#         # // Login failed trying again to login
#         try:
#             await login(page, credentials, messageTransport, useCookieStore)
#         except:
#             if browser:
#                 await browser.close()
#             else:
#                 break
#     try:
#         await changeHomePageLangIfNeeded(page)
#     except:
#         messageTransport.log(error)
#         await login(page, credentials, messageTransport, useCookieStore)


async def passwordlogin(self, page):
    await page.goto(YoutubeHomePageURL)
    self.log.debug("try to login in from youtube homepage")

    try:
        await page.get_by_role("link", name="Sign in").is_visible()
        await page.get_by_role("link", name="Sign in").click()
        self.log.debug("detected  sign in button")

    except:
        self.log.debug("could not find sign in button")
    # change sign in language
    try:
        await page.get_by_role("combobox").is_visible()
        s = await page.get_by_role("combobox").all_text_contents()
        s = "".join(s)
        if not "English" in s:
            await page.get_by_role("combobox").click()
            await page.get_by_role("option", name="English (United States)").click()
        self.log.debug("changed to english display language")
            
    except:
        self.log.debug("could not find language option ")

    try:
        await page.get_by_role("textbox", name="Email or phone").is_visible()
        await page.get_by_role("textbox", name="Email or phone").fill(self.username)
        self.log.debug("detected  Email or phone textbox")
        
    except:
        self.log.debug("could not find email or phone input textbox")
    await page.get_by_role("button", name="Next").click()
        
    try:
        await page.get_by_role("textbox", name="Enter your password").is_visible()
        await page.get_by_role("textbox", name="Enter your password").fill(
            self.password
        )
        self.log.debug("detected  password textbox")
        
    except:
        self.log.debug("could not find password input textbox")
    #     page.get_by_text("We noticed unusual activity in your Google Account. To keep your account safe, y").click()

    await page.get_by_role("button", name="Next").click()
    self.log.debug("detected  Next button")
    
    try:
        await page.locator("#headingText").get_by_text("2-Step Verification").click()
        await page.get_by_text("Google Authenticator").click()
        await page.get_by_text(
            "Get a verification code from the Google Authenticator app"
        ).click()
        await page.get_by_role("textbox", name="Enter code").click()
        sleep(6000)
    except:
        self.log.debug("failed to input code")
    await page.get_by_role("button", name="Next").click()

    # await page.get_by_text("选择频道").click()
    # await page.get_by_role("checkbox", name="不再询问").click()
    # await page.locator("ytd-identity-prompt-footer-renderer").click()
    # await page.locator("ytd-simple-menu-header-renderer").click()

    current_url = self.page.url
    if "/studio.youtube.com/" in current_url:
        print(f"studio.youtube.com in current_url: {current_url}")

        print(
            f"youtube 登录成功!!!",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        if not self.CHANNEL_COOKIES:
            self.CHANNEL_COOKIES = self.username
        state = self.context.storage_state(path=self.CHANNEL_COOKIES)
        self.log.debug("we auto save your channel cookies to file:", self.CHANNEL_COOKIES)

        if self.page:
            try:
                await self.page.close()
            except:
                pass
        return True
    else:
        print(
            f"youtube 登录失败!!!",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        if self.page:
            try:
                await self.page.close()
            except:
                pass
        return None

def kill_orphan_chrome(self):
    num = 1
    while True:
        if os.popen("ps -f --ppid 1 | grep chromedriver").read():
            try:
                os.system(
                    "ps -f --ppid 1 | grep chromedriver | awk '{print $2}' | xargs kill -9"
                )
            except:
                pass
        if os.popen("ps -f --ppid 1 | grep chrome").read():
            try:
                os.system(
                    "ps -f --ppid 1 | grep chrome | awk '{print $2}' | xargs kill -9"
                )
            except:
                pass
        if (
            os.popen("ps -f --ppid 1 | grep chromedriver").read() == ""
            and os.popen("ps -f --ppid 1 | grep chrome").read() == ""
        ):
            break
        num += 1
        sleep(0.2)
        if num > 3:
            break


async def botcheck(self):
    print('this is a placeholder for now,full code  is in the  examples/botcheck.py,but fake browser is a little bit diffcult for me now')
async def botcheck_sannysoft(self):
    # self.kill_orphan_chrome()
    url = "https://abrahamjuliot.github.io/creepjs/"
    url = "http://f.vision/"
    url = "https://coveryourtracks.eff.org"
    url = "https://bot.sannysoft.com/"

    # https://github.com/darbra/sperm/blob/e13bfe2134865f291531b4f8101cda6e62488b2b/md/simpread-Canvas%20%E6%8C%87%E7%BA%B9%E9%9A%90%E8%97%8F%E5%AE%9E%E6%88%98.md?plain=1#L121
    chrome = None
    wait = None
    for i in range(3):
        port = f"{random.randint(6, 8)}{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}"
        print(f"第 {i + 1} 次初始化浏览器, 端口为:{port} ")
        try:
            await self.page.goto(url)
            # input('test:: ')
            if "sannysoft" in self.page.url:
                print(
                    "浏览器 正常状态...",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                break
            else:
                continue
        except Exception as e:
            print(f"初始化浏览器异常: {e}")
            if self.broswer:
                self.broswer.quit()
            continue


async def tiktok_login(self, account, password):
    # self.kill_orphan_chrome()
    # botcheck()
    # 判断是否出现登录标签
    # 如果出现则直接保存图片扫码登录, 否则点击登录, 再保存图片扫码登录
    # sleep(random.uniform(0.2, 0.5))
    if self.page:
        index = 0
        while True:
            index += 1

            await self.page.goto("https://www.tiktok.com/login/phone-or-email/email")
            sleep(random.uniform(2, 3))
            current_url = self.page.url
            if index > 3:
                print(f"三次登录失败!!!")
                error_name = f"{str(time() * 1000)}_login_error.png"
                await self.page.screenshot(error_name)
                await self.page.close()
                return "三次登录失败!!!"
            elif "login" in current_url:
                await self.page.locator('//input[@name="username"]').fill(str(account))
                print("输入用户名", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                sleep(3)
                # for j in password:
                await self.page.locator('//input[@autocomplete="new-password"]').fill(
                    str(password)
                )
                sleep(1)
                print("输入密码", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # input(';;;;:')
                await self.page.locator('//input[@autocomplete="new-password"]').click()

                await self.page.get_by_role("button", name="Log in").click()
                sleep(random.uniform(5, 6))
                try:
                    continue
                except:
                    print("we can not auto login")
            else:
                if self.page:
                    try:
                        await self.page.close()
                    except:
                        pass
                return "登录成功!"
    else:
        print(f"初始化chrome失败! ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if self.broswer:
            try:
                self.broswer.quit()
            except:
                pass
        return "初始化chrome失败! "

def init_broswer_popen(self, url, port):
    self.kill_orphan_chrome()
    if self.arg == 'test':
        if self.proxy:
            os.popen(f'{self.chrome_path} --remote-debugging-port={port} --proxy-server="{self.proxy}" --user-data-dir="{path_config["Chrome_log"]}{port+ "_"+ str(time.time())}" --disable-gpu --incognito --disable-extensions --window-size="1920,1080" --no-first-run --disable-dev-shm-usage --no-first-run --mute-audio --disable-infobars ')
        else:
            os.popen(f'{self.chrome_path} --remote-debugging-port={port} --user-data-dir="{path_config["Chrome_log"]}{port+ "_"+ str(time.time())}" --disable-gpu --incognito --disable-extensions --window-size="1920,1080" --no-first-run --disable-dev-shm-usage --no-first-run --mute-audio --disable-infobars ')
    else:
        if self.proxy:
            os.popen(f'{self.chrome_path} --remote-debugging-port={port} --user-data-dir="{path_config["Chrome_log"]}{port+ "_"+ str(time.time())}" --proxy-server="{self.proxy}" --headless --disable-gpu --incognito --disable-extensions --window-size="1920,1080" --no-first-run --disable-dev-shm-usage --no-first-run --mute-audio --disable-infobars ')
        else:
            os.popen(
                f'{self.chrome_path} --remote-debugging-port={port} --user-data-dir="{path_config["Chrome_log"]}{port+ "_"+ str(time.time())}" --headless --disable-gpu --incognito --disable-extensions --window-size="1920,1080" --no-first-run --disable-dev-shm-usage --no-first-run --mute-audio --disable-infobars ')
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    print('chrome 正在连接', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    _browser = webdriver.Chrome(options=opt)
    print('chrome 连接成功', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    # with open('stealth.min.js', mode='r') as f:
    #     js = f.read()
    # _browser.execute_cdp_cmd(
    #     cmd_args={'source': js},
    #     cmd="Page.addScriptToEvaluateOnNewDocument",
    # )
    _browser.get(url)
    self.broswer = _browser
    self.wait = WebDriverWait(_browser, timeout=5, poll_frequency=0.5)
    return _browser, self.wait
async def youtube_login(self, account, password):
    # self.kill_orphan_chrome()
    # url = 'https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dzh-CN%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=zh-CN&ec=65620'
    url = "https://accounts.google.com/ServiceLogin"
    if self.page:
        print(f"init chrome success! ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



        try:

            await self.page.goto(url
                            #  , {'waitUntil': "load"}
                             )
            current_url = self.page.url            
            print(f"youtube_login auto login from {url}")
            
            for i in range(10):
                # input('test:::: ')
                print(f'trying in {i} times')
                # sleep(random.uniform(1, 2))
                
                if i > 6:
                    print(
                        f"6次未找到input 密码框,重新初始化chrome ",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    break
                elif "signin/identifier" in current_url:
                    self.log.debug("signin/identifier in url")

                    try:
                        
                        await self.page.locator('#identifierId').is_visible()
                        await self.page.locator('#identifierId').fill(self.username)
                        self.log.debug("detected  Email or phone textbox")
                        
                    except:
                        self.log.debug("could not find email or phone input textbox")
                    
                    await self.page.get_by_role("button", name="Next").click()
                    
                    self.log.debug("detected  Next button")
                    sleep(random.uniform(5, 6))
                    try:
                        self.log.debug(f"Trying to detect insecure browser...{self.page.url}")         
                        hint = await self.page.locator(".tCpFMc > form").all_text_contents()
                        hint = "".join(hint)
                        print(f'hints:{hint}')

                        if  'This browser or app may not be secure' in hint:
                            self.log.debug(f"you have detect insecure browser")
                            print(
                                f"被检测, 重新初始化chrome... ",
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            )
                            await self.page.quit()
                            sleep(1)
                            for i in range(3):
                                port = f"{random.randint(6, 9)}{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}"
                                print(f"第 {i + 1} 次初始化chrome, 端口为:{port} ")
                                try:
                                    chrome, wait = await self.init_broswer_popen(url=url, port=port)
                                    if "accounts" in chrome.current_url:
                                        print(
                                            "chrome 正常状态...",
                                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        )
                                        break
                                    else:
                                        if chrome:
                                            await chrome.quit()
                                        continue
                                except Exception as e:
                                    print(f"初始化chrome异常: {e}")
                                    if chrome:
                                        await chrome.quit()
                                    continue
                            # sleep(random.uniform(1, 2))
                            continue

                        else:
                            pass

                    except:
                        self.log.debug(f"Finishing detect insecure browser...")

                    try:
                        await self.page.get_by_role("textbox", name="Enter your password").is_visible()
                        await self.page.get_by_role("textbox", name="Enter your password").fill(
                            self.password
                        )
                        self.log.debug("detected  password textbox")
                        
                    except:
                        self.log.debug("could not find password input textbox")
                    #     page.get_by_text("We noticed unusual activity in your Google Account. To keep your account safe, y").click()
                    sleep(random.uniform(5, 6))
                    try:
                        self.log.debug(f"Trying to detect insecure browser...{self.page.url}")         
                        hint = await self.page.locator(".tCpFMc > form").all_text_contents()
                        hint = "".join(hint)
                        print(f'hints:{hint}')

                        if  'This browser or app may not be secure' in hint:
                            self.log.debug(f"you have detect insecure browser")

                            self.close()
                        else:
                            pass

                    except:
                        self.log.debug(f"Finishing detect insecure browser...")


                    try:
                        await self.page.locator("#headingText").get_by_text("2-Step Verification").click()
                        await self.page.get_by_text("Google Authenticator").click()
                        await self.page.get_by_text(
                            "Get a verification code from the Google Authenticator app"
                        ).click()
                        await self.page.get_by_role("textbox", name="Enter code").click()
                        sleep(6000)
                    except:
                        self.log.debug("failed to input code")
                    await self.page.get_by_role("button", name="Next").click()                
                    sleep(2)
                    continue
                elif "challenge/pwd" in current_url:
                    self.log.debug("challenge/pwd in url")

                    if self.is_element_exist_wait(self.wait, '//*[@id="selectionc1"]'):
                        await self.page.locator('//input[@type="password"]').send_keys(password)
                        print(
                            f"输入密码: {password}! ",
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        )
                        sleep(0.5)
                        await self.page.locator('//*[@id="passwordNext"]//button').click()
                        print(f"点击完成! ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        sleep(2)
                        await self.page.goto("https://studio.youtube.com/channel/")
                        sleep(random.uniform(1, 2))
                        break
                    else:
                        print(
                            f"第{i + 1}次未找到input 密码框! ",
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        )
                        sleep(1)
                        continue
                elif "signin/rejected" in current_url:
                    print(
                        f"被检测, 重新初始化chrome... ",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    await self.page.quit()
                    sleep(1)
                    for i in range(3):
                        port = f"{random.randint(6, 9)}{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}"
                        print(f"第 {i + 1} 次初始化chrome, 端口为:{port} ")
                        try:
                            chrome, wait = await self.init_broswer_popen(url=url, port=port)
                            if "accounts" in chrome.current_url:
                                print(
                                    "chrome 正常状态...",
                                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                )
                                break
                            else:
                                if chrome:
                                    await chrome.quit()
                                continue
                        except Exception as e:
                            print(f"初始化chrome异常: {e}")
                            if chrome:
                                await chrome.quit()
                            continue
                    # sleep(random.uniform(1, 2))
                    continue
                else:
                    print(
                        f"第{i+1}次未找到input 密码框! ",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    continue
            current_url = self.page.url
            if "/studio.youtube.com/" in current_url:
                print(f"studio.youtube.com in current_url: {current_url}")

                print(
                    f"youtube 登录成功!!!",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                if self.page:
                    try:
                        await self.page.close()
                    except:
                        pass
                return True
            else:
                print(
                    f"youtube 登录失败!!!",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                if self.page:
                    try:
                        await self.page.close()
                    except:
                        pass
                return None

        except:
            print(f'due to network issue,we can not access: {url}. change another proxy to try')
            return None
        
    else:
        print(f"init chrome failed! ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if self.page:
            try:
                await self.page.close()
            except:
                pass
        return None