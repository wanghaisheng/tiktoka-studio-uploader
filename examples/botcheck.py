from playwright.async_api import (
    Playwright,
    Browser,
    BrowserContext,
    async_playwright,
    expect,
)
from tsup.utils.webdriver.playwright_driver_async_stealth import (
    PlaywrightAsyncDriverStealth,
)
import asyncio
import os
from tsup.botright.botright import Botright
from cf_clearance import async_cf_retry, async_stealth
from datetime import datetime
from urllib.parse import urlparse, urlunsplit, urlsplit


class Botcheck:
    def __init__(self, page):
        self.page = page
        self.timestr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    async def goto(self, url, delay=2000000):
        try:
            if url:
                # await self.page.goto(url, wait_until="networkidle")
                await self.page.goto(url)

                # self.page.set_default_timeout(delay)
            else:
                raise ValueError("No url provided")
        except Exception as err:
            raise err

    async def isolatedWorld(self):
        try:
            await self.goto(
                "https://prescience-data.github.io/execution-monitor.html", 200
            )

            self.page.locator("#result")

            await self.page.evaluate(
                """
                let newDiv = document.createElement("div");
                let newContent = document.createTextNode("Creating an element on the page.");
                newDiv.appendChild(newContent);
                let currentDiv = document.getElementById("div1");
                document.body.insertBefore(newDiv, currentDiv);
            """
            )

            self.page.set_default_timeout(2000)

            element = self.page.locator("#result")
            output = await element.get_attribute("textContent")
            await self.page.screenshot(
                path=f"output/IsolatedWorld-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            print("IsolatedWorld", output)
            return output
        except Exception as err:
            raise err

    async def behaviorMonitor(self):
        try:
            await self.goto(
                "https://prescience-data.github.io/behavior-monitor.html", 200
            )

            resultElement = self.page.locator("#result")
            if not resultElement:
                raise ValueError("Failed to find #result")

            await resultElement.hover()
            await resultElement.click(delay=10)

            self.page.set_default_timeout(200)

            inputElement = self.page.locator("input#test-input")
            if not inputElement:
                raise ValueError("Failed to find input#test-input")

            await inputElement.click()
            await inputElement.type("Hello world...", delay=100, timeout=30000)

            # await self.page.evaluate(
            #     "Input.synthesizeScrollGesture",
            #     {"x": 0, "y": 0, "xDistance": 0, "yDistance": -100},
            # )
            await self.page.dispatch_event("input#test-input", "scroll")
            await self.page.wait_for_timeout(2500)
            await expect(self.page.locator("#result")).to_be_visible()
            element = self.page.locator("#result")
            output = await element.get_attribute("textContent")
            await self.page.screenshot(
                path=f"output/BehaviorMonitor-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            print("BehaviorMonitor", output)
            return output
        except Exception as err:
            raise err

    async def niespodd(self):
        access = False
        try:
            await self.page.goto("https://niespodd.github.io/browser-fingerprinting/")
            access = True
            await self.page.screenshot(
                path=f"output/niespodd-{self.timestr}.png", full_page=True
            )

        except Exception as err:
            output = "Failed"

    async def f5networkloginForm(self):
        access = False
        try:
            await self.page.goto("https://ib.bri.co.id/ib-bri")
            access = True
        except Exception as err:
            output = "Failed"

            print("can not open page,F5 Network", output)

            # await self.page.close()
        if access == True:
            try:
                element = await expect(
                    self.page.locator("form#loginForm")
                ).to_be_visible(
                    # timeout=500000
                )

                output = "Passed" if element else "Failed"
                await self.page.screenshot(
                    path=f"output/f5-{self.timestr}.png", full_page=True
                )

                print("F5 Network", output)
                return output

            except:
                output = "Failed"

                print("cannot find login form,F5 Network", output)

                # await self.page.close()
        else:
            print("falied F5")
        # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
        # print(f"Browser fingerprint fields:{fingerprint}")

    async def pixelscan(self):
        access = False
        try:
            await self.goto("https://pixelscan.net")
            access = True
        except:
            output = "Failed"

            print("PixelScan", output)
            await self.page.route("**", lambda route: route.continue_())
            self.page.on(
                "request", lambda request: print(request.headers.get("X-Forwarded-For"))
            )
            self.page.on("request", lambda request: print(request.headers))

            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
        # await self.page.close()
        if access == True:
            try:
                element = await expect(
                    self.page.locator("span.consistency-status-text")
                ).to_be_visible(timeout=50000)
                element = element.text_content()
                output = "Passed" if "inconsistent" in element else "Failed"
                await self.page.screenshot(
                    path=f"output/PixelScan-{self.timestr}.png", full_page=True
                )

                print("PixelScan", output)
                return output
            except:
                output = "Failed"

                print("PixelScan", output)

                # await self.page.close()
        else:
            print("falied F5")

    async def sannysoft(self):
        try:
            await self.goto("https://bot.sannysoft.com")

            await self.page.screenshot(
                path=f"output/Sannysoft-{self.timestr}.png", full_page=True
            )
            # print("Sannysoft", output)
            # return output
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
        except Exception as err:
            raise err

    async def recaptcha(self):
        try:
            await self.goto(
                "https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html",
                15000,
            )

            element = self.page.locator("#score")
            ishere = expect(element).to_be_visible()
            if ishere:
                output = await self.page.evaluate(
                    "(element) => element.textContent", element
                )
                await self.page.screenshot(
                    path=f"output/Recaptcha-{self.timestr}.png", full_page=True
                )
                # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
                # print(f"Browser fingerprint fields:{fingerprint}")
                print("Recaptcha Score", output)
                return output

            else:
                print("page not well load-antcpt Recaptcha ")
        except Exception as err:
            raise err

    async def hellobot(self):
        try:
            await self.goto("http://anonymity.space/hellobot.php", 3000)

            await self.page.locator("#result").is_visible()
            element = self.page.locator("#result")

            output = await element.get_attribute("textContent")
            await self.page.screenshot(
                path=f"output/HelloBot-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            print("HelloBot", output)
            return output
        except Exception as err:
            raise err

    async def areyouheadless(self):
        try:
            await self.goto("https://arh.antoinevastel.com/bots/areyouheadless", 2000)

            await self.page.locator("#res").is_visible()
            element = self.page.locator("#res")

            output = await element.get_attribute("textContent")
            await self.page.screenshot(
                path=f"output/AreYouHeadless-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            print("AreYouHeadless", output)
            return output
        except Exception as err:
            raise err

    async def fingerprintjs(self):
        try:
            await self.goto("https://fingerprintjs.com/demo", 5000)

            await self.page.locator("table.table-compact").is_visible()
            element = self.page.locator(
                "table.table-compact > tbody > tr:nth-child(4) > td.miriam"
            )

            text = await element.get_attribute("textContent")
            output = "Passed" if text == "NO" else "Failed"
            await self.page.screenshot(
                path=f"output/FingerprintJS-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            print("FingerprintJS", output)
            return output
        except Exception as err:
            raise err

    async def datadome(self):
        try:
            await self.goto("https://datadome.co", 2000)

            button = self.page.locator("#menu-item-18474")

            if button:
                await button.click(delay=10)
                await self.page.waitForNavigation(wait_until="networkidle2")
                await self.page.wait_for_timeout(500)
            else:
                print("Could not find the button!")

            captcha = self.page.locator(
                'iframe[src^="https://geo.captcha-delivery.com/captcha/"]'
            )
            output = "Failed" if captcha else "Passed"
            await self.page.screenshot(
                path=f"output/Datadome-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            print("Datadome", output)
            return output
        except Exception as err:
            raise err

    async def whiteops(self):
        try:
            await self.goto("https://www.whiteops.com", 3000)

            button = self.page.locator(
                'a[href="https://www.whiteops.com/company/about"]'
            )

            if button:
                await button.click(delay=8)
                await self.page.waitForNavigation(wait_until="networkidle2")
                await self.page.wait_for_timeout(500)
            else:
                print("Could not find the button!")

            test = self.page.locator(
                'a[href="https://resources.whiteops.com/data-sheets/white-ops-company-overview"]'
            )
            output = "Passed" if test else "Failed"
            await self.page.screenshot(
                path=f"output/Whiteops-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            print("Whiteops", output)
            return output
        except Exception as err:
            raise err

    async def sleep(ms):
        await asyncio.sleep(ms / 1000)

    async def incolumitas(self):
        page = self.page
        await page.goto("https://bot.incolumitas.com/")
        await page.wait_for_selector("#formStuff")
        user_name_input = await page.query_selector('[name="userName"]')
        await user_name_input.click(click_count=3)
        await user_name_input.type("bot3000")

        email_input = await page.query_selector('[name="eMail"]')
        await email_input.click(click_count=3)
        await email_input.type("bot3000@gmail.com")

        await page.select_option('[name="cookies"]', "I want all the Cookies")
        await page.click("#smolCat")
        await page.click("#bigCat")
        await page.click("#submit")

        async def handle_dialog(dialog):
            print(dialog.message())
            await dialog.accept()

        page.on("dialog", handle_dialog)

        await page.wait_for_selector("#tableStuff tbody tr .url")
        await self.sleep(100)

        await page.wait_for_selector("#updatePrice0")
        await page.click("#updatePrice0")
        await page.wait_for_function(
            '!!document.getElementById("price0").getAttribute("data-last-update")'
        )

        await page.wait_for_selector("#updatePrice1")
        await page.click("#updatePrice1")
        await page.wait_for_function(
            '!!document.getElementById("price1").getAttribute("data-last-update")'
        )

        data = await page.evaluate(
            """() => {
            let results = [];
            document.querySelectorAll('#tableStuff tbody tr').forEach((row) => {
                results.push({
                    name: row.querySelector('.name').innerText,
                    price: row.querySelector('.price').innerText,
                    url: row.querySelector('.url').innerText,
                })
            });
            return results;
        }"""
        )
        # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
        # print(f"Browser fingerprint fields:{fingerprint}")
        print(data)
        await self.sleep(6000)

        new_tests = await page.inner_text("#new-tests")
        old_tests = await page.inner_text("#detection-tests")
        await self.page.screenshot(
            path=f"output/incolumitas-{self.timestr}.png", full_page=True
        )

        print(new_tests)
        print(old_tests)

    async def Imperva(self):
        url = "https://driverpracticaltest.dvsa.gov.uk/login"
        url = "https://corretor.portoseguro.com.br/corretoronline/"
        url = "https://www.cma-cgm.com/"
        url = "https://www.nordstrom.com/"

        page = self.page
        await page.goto(url)
        await self.page.screenshot(
            path=f"output/Imperva-{self.timestr}.png", full_page=True
        )
        # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
        # print(f"Browser fingerprint fields:{fingerprint}")

    async def nowsecure(self):
        url = "www.nowsecure.nl"
        # https://bot.incolumitas.com/#botChallenge
        page = self.page
        await page.goto(url)
        await self.page.screenshot(
            path=f"output/nowsecure-{self.timestr}.png", full_page=True
        )
        # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
        # print(f"Browser fingerprint fields:{fingerprint}")
        return

    def uri_validator(self, x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc])
        except:
            return None

    async def checkIP(self,page, url):
        # url = "www.nowsecure.nl"
        # https://bot.incolumitas.com/#botChallenge
        if self.uri_validator(url):
            domain = urlparse(url).netloc
            await page.goto(url)
            await page.screenshot(
                path=f"output/{domain}-{self.timestr}.png", full_page=True
            )
            # fingerprint = await self.page.evaluate("Object.keys(window.navigator)")
            # print(f"Browser fingerprint fields:{fingerprint}")
            return


async def main():
    # browser = await async_playwright.chromium.launch()
    # context = await browser.newContext()
    # page = await context.newPage()
    proxy_option = "socks5://127.0.0.1:1080"
    proxy_option=None
    pl = await PlaywrightAsyncDriverStealth.create(
        proxy=proxy_option,
        driver_type="firefox",
        timeout=300,
#         headless=False,
#         for github action
        headless=True,
        
    )

    # await async_stealth(pl.page, pure=True)

    ipchecklist = [
        "https://niespodd.github.io/browser-fingerprinting/",
        "https://bgp.he.net/",
        "https://browserleaks.com/",
        "https://ip.voidsec.com/",
        "https://ipinfo.io/",
        "https://ipleak.com/",
        "https://ipleak.net/",
        "https://ipleak.org/",
        "https://ipx.ac/run",
        "https://nstool.netease.com/",
        "https://test-ipv6.com/",
        "https://whatismyipaddress.com/blacklist-check",
        "https://whoer.net/",
        "https://www.astrill.com/dns-leak-test",
        "https://www.astrill.com/ipv6-leak-test",
        "https://www.astrill.com/port-scan",
        "https://www.astrill.com/vpn-leak-test",
        "https://www.astrill.com/what-is-my-ip",
        "https://www.deviceinfo.me/",
        "https://www.dnsleaktest.com/",
        "https://www.doileak.com/",
        "https://www.expressvpn.com/webrtc-leak-test",
        "https://bot.incolumitas.com/proxy_detect.html",
        "https://corretor.portoseguro.com.br/corretoronline/",
        "https://ipapi.co/json/",
        "https://jsonip.com/",
        "https://ipinfo.io/json",
        "https://jsonip.com/",
        "https://api64.ipify.org/",
    ]
    for url in ipchecklist:
        botcheck = Botcheck(pl.page)
        print('raw pl',pl.page)
        
        await botcheck.checkIP(pl.page ,url)
    for url in ipchecklist:
        print('raw pl with async_stealth')

        botcheck = Botcheck(pl.page)
        await async_stealth(pl.page, pure=True)
        await botcheck.checkIP(pl.page ,url)
    for url in ipchecklist:
        print('raw pl with stealth js')
        
        path = os.path.join(os.path.dirname(__file__), "../tsup/utils/js/stealth.min.js")
        await pl.page.add_init_script(path=path)
        await botcheck.checkIP(pl.page ,url)

    # botright_client = await Botright(headless=False)
    # browser = await botright_client.new_browser(proxy=proxy_option)
    # page = await browser.new_page()
    # botcheck = Botcheck(page)
    # # Continue by using the Page

    # await botright_client.close()

    # await pl.page.context.storage_state(path="1.json")
    # await async_stealth(self.page, pure=True)

    # for debug purpose,we should print all request header to find the leak

    # Hey this is most likely caused, by the proxy you're using. You need to make sure your proxy connection does not forcefully send any of these headers

    # 'VIA',
    # 'X-FORWARDED-FOR',
    # 'X-FORWARDED',
    # 'FORWARDED-FOR',
    # 'FORWARDED-FOR-IP',
    # 'FORWARDED',
    # 'CLIENT-IP',
    # 'PROXY-CONNECTION'

#     await botcheck.isolatedWorld()
#     await botcheck.behaviorMonitor()
#     await botcheck.f5networkloginForm()
#     await botcheck.pixelscan()
#     await botcheck.sannysoft()
#     await botcheck.recaptcha()
#     await botcheck.hellobot()
#     await botcheck.areyouheadless()
#     await botcheck.fingerprintjs()
#     await botcheck.datadome()
#     await botcheck.whiteops()
#     await botcheck.incolumitas()

    # await pl.browser.close()


asyncio.run(main())
