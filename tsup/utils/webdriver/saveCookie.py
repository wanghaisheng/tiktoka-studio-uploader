import subprocess
from tsup.utils.webdriver import PlaywrightAsyncDriver
from tsup.utils.webdriver.webdirver import InterceptResponse, InterceptRequest
from cf_clearance import async_cf_retry, async_stealth
from datetime import datetime, date, timedelta, time
from playwright.async_api import Page, expect

import random
from time import sleep


async def tiktok_manual_login(self):
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
                await self.page.locator('//input[@name="username"]').click()
                print("输入用户名", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                sleep(60)
                # for j in password:
                await self.page.locator('//input[@autocomplete="new-password"]').click()
                sleep(60)
                print("输入密码", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # input(';;;;:')
                await self.page.locator('//input[@autocomplete="new-password"]').click()

                await self.page.get_by_role("button", name="Log in").click()
                sleep(random.uniform(5, 6))
                # captcha
                error_msg = ""
                try:
                    expect(
                        await self.page.locator(
                            ".tiktok-3i0bsv-DivTextContainer > span:nth-child(1)"
                        ).is_visible()
                    )
                    error_msg = await self.page.locator(
                        ".tiktok-3i0bsv-DivTextContainer > span:nth-child(1)"
                    ).text_content

                    if (
                        not "Maximum number of attempts reached. Try again later"
                        in error_msg
                    ):
                        continue
                except:
                    print("we can not auto login", error_msg)
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


def getCookie(
    browserType: str = "firefox",
    proxyserver: str = "",
    channelname: str = "youtube-channel",
    url: str = "www.youtube.com",
):
    if browserType in ["firefox", "webkit", ""]:
        if proxyserver:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                # + ' --device "iPad Pro 11 landscape" '
                + " --proxy-server "
                + proxyserver
                + " --lang 'en-GB' --save-storage="
                + channelname
                + "-cookie.json "
                + url
            )
        else:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                + " --lang 'en-GB' --save-storage="
                + channelname
                + "-cookie.json "
                + url
            )
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        print(result)
        if result.returncode:
            print(f"failed to save cookie file:{result.stderr}")
        else:
            print("just check your cookie file", channelname + "-cookie.json")


async def getCookieWithProxy(self):
    if self.proxy_option == "":
        self.logger.debug(f"start web page without proxy:{self.proxy_option}")

        with PlaywrightAsyncDriver(
            proxy=None,
            driver_type=self.browserType,
            headless=self.headless,
            timeout=30,
            use_stealth_js=True,
        ) as pl:
            await pl._setup()
            self.pl = pl

            self._browser = pl.browser
            self.context = pl.context
            self.page = pl.page
        self.logger.debug(
            f"{self.browserType} is now running without proxy:{self.proxy_option}"
        )

    else:
        with PlaywrightAsyncDriver(
            proxy=self.proxy_option,
            driver_type=self.browserType,
            timeout=30,
            headless=self.headless,
            use_stealth_js=True,
        ) as pl:
            await pl._setup()
            self.pl = pl

            self._browser = pl.browser
            self.context = pl.context
            self.page = pl.page

        self.logger.debug(
            f"{self.browserType} is now running with proxy:{self.proxy_option}"
        )

        # check fakebrowser to bypass captcha and security violations

    await self.page.evaluate(
        "document.body.appendChild(Object.assign(document.createElement('script'), {src: 'https://gitcdn.xyz/repo/berstend/puppeteer-extra/stealth-js/stealth.min.js'}))"
    )
    await async_stealth(self.page, pure=True)
    # store the stealth state to reload next time
    # await botcheck(pl)
    await tiktok_manual_login(self)
    cookiepath = (
        "tiktok-stealth-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json"
    )
    await self.page.context.storage_state(path=cookiepath)
    self.logger.debug(f"we capture your account cookie at:{cookiepath}")
    return cookiepath


# if __name__ == "__main__":
#     sites = [
#         "https://www.youtube.com/upload?persist_gl=1",
#         "https://www.tiktok.com",
#         "https://www.douyin.com",
#         "https://www.tiktok.com/login/phone-or-email/email",
#     ]
# channelname is your account name or something else
# for youtube
# getCookie(browserType='firefox',proxyserver='socks5://127.0.0.1:1080',channelname='',url=sites[0])
# for tiktok
# i7SNiSG8V7jND^
# offloaddogsboner@outlook.com

# unboxdoctor@outlook.com
# 95Qa*G*za5Gb
# getCookie(
#     browserType="firefox",
#     proxyserver="socks5://127.0.0.1:1080",
#     channelname="",
#     url=sites[0],
# )
# for douyin
# getCookie(browserType='firefox',proxyserver='socks5://127.0.0.1:1080',channelname='',url=sites[2])
