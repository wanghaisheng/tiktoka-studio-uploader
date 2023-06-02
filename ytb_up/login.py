import json
from typing import Dict, List
import os
from .constants import *
from time import sleep
import random
from datetime import datetime, date, timedelta, time

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


def confirm_logged_in(self) -> bool:
    """Confirm that the user is logged in. The browser needs to be navigated to a YouTube page."""
    try:
        self.page.locator(
            "yt-img-shadow.ytd-topbar-menu-button-renderer > img:nth-child(1)"
        )

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
    try:
        await page.get_by_role("link", name="Sign in").is_visible()
        await page.get_by_role("link", name="Sign in").click()

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
    except:
        self.log.debug("could not find language option ")

    try:
        await page.get_by_role("textbox", name="Email or phone").is_visible()
        await page.get_by_role("textbox", name="Email or phone").fill(self.username)
    except:
        self.log.debug("could not find email or phone input textbox")
    try:
        await page.get_by_role("textbox", name="Enter your password").is_visible()
        await page.get_by_role("textbox", name="Enter your password").fill(
            self.password
        )
    except:
        self.log.debug("could not find email or phone input textbox")
    #     page.get_by_text("We noticed unusual activity in your Google Account. To keep your account safe, y").click()

    await page.get_by_role("button", name="Next").click()
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
    if not self.CHANNEL_COOKIES:
        self.CHANNEL_COOKIES = self.username
    state = self.context.storage_state(path=self.CHANNEL_COOKIES)
    self.log.debug("we auto save your channel cookies to file:", self.CHANNEL_COOKIES)

    return


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


def youtube_login(self, account, password):
    # self.kill_orphan_chrome()
    # url = 'https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dzh-CN%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=zh-CN&ec=65620'
    url = "https://accounts.google.com/ServiceLogin"
    botcheck()
    if self.broswer:
        for i in range(10):
            # input('test:::: ')
            sleep(random.uniform(1, 2))
            current_url = self.broswer.current_url
            if i > 6:
                print(
                    f"6次未找到input 密码框,重新初始化chrome ",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                break
            elif "signin/identifier" in current_url:
                self.broswer.locator('//input[@type="email"]').click()
                sleep(1)
                # self.broswer.locator(by='xpath', value='//input[@type="email"]').send_keys(account)
                for one in account:
                    self.broswer.locator('//input[@type="email"]').send_keys(one)
                    sleep(random.uniform(0.1, 0.4))
                print(
                    f"输入账号: {account}! ",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                sleep(random.uniform(1, 2))
                self.broswer.locator('//*[@id="identifierNext"]/div/button').click()
                sleep(2)
                continue
            elif "challenge/pwd" in current_url:
                if self.is_element_exist_wait(self.wait, '//*[@id="selectionc1"]'):
                    self.broswer.locator('//input[@type="password"]').send_keys(
                        password
                    )
                    print(
                        f"输入密码: {password}! ",
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    sleep(0.5)
                    self.broswer.locator('//*[@id="passwordNext"]//button').click()
                    print(f"点击完成! ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    sleep(2)
                    self.page.goto("https://studio.youtube.com/channel/")
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
                self.broswer.quit()
                sleep(1)
                for i in range(3):
                    port = f"{random.randint(6, 9)}{random.randint(1, 9)}{random.randint(1, 9)}{random.randint(1, 9)}"
                    print(f"第 {i + 1} 次初始化chrome, 端口为:{port} ")
                    try:
                        chrome, wait = self.init_broswer_popen(url=url, port=port)
                        if "accounts" in chrome.current_url:
                            print(
                                "chrome 正常状态...",
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            )
                            break
                        else:
                            if chrome:
                                chrome.quit()
                            continue
                    except Exception as e:
                        print(f"初始化chrome异常: {e}")
                        if chrome:
                            chrome.quit()
                        continue
                # sleep(random.uniform(1, 2))
                continue
            else:
                print(
                    f"第{i+1}次未找到input 密码框! ",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                continue
        current_url = self.broswer.current_url
        print(f"current_url: {current_url}")
        if "/studio.youtube.com/" in current_url:
            print(
                f"youtube 登录成功!!!",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            if self.broswer:
                try:
                    self.broswer.quit()
                except:
                    pass
            return True
        else:
            print(
                f"youtube 登录失败!!!",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            if self.broswer:
                try:
                    self.broswer.quit()
                except:
                    pass
            return None
    else:
        print(f"初始化chrome失败! ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if self.broswer:
            try:
                self.broswer.quit()
            except:
                pass
        return None
