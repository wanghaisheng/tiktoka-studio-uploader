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

class Botcheck:
    def __init__(self, page):
        self.page = page

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

            print("BehaviorMonitor", output)
            return output
        except Exception as err:
            raise err

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
                    timeout=500000
                )

                output = "Passed" if element else "Failed"

                print("F5 Network", output)
                return output
            except:
                output = "Failed"

                print("cannot find login form,F5 Network", output)

                # await self.page.close()
        else:
            print("falied F5")

    async def pixelscan(self):
        access = False
        try:
            await self.goto("https://pixelscan.net")
            access = True
        except:
            output = "Failed"

            print("PixelScan", output)

            # await self.page.close()
        if access == True:
            try:
                element = await expect(
                    self.page.locator("span.consistency-status-text")
                ).to_be_visible(
                    timeout=50000
                )
                element = element.text_content()
                output = "Passed" if "inconsistent" in element else "Failed"

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
            await self.goto("https://bot.sannysoft.com", 5000)

            output = await self.page.evaluate(
                """
                return new Promise(async (resolve, reject) => {
                    let results = [];
                    const tables = document.querySelectorAll("table");
                    let rows;
                    let cols;
                    for (let i = 0; i < 2; i++) {
                        if (tables[i]) {
                            rows = tables[i].querySelectorAll("tr");
                            rows.forEach((row) => {
                                cols = row.querySelectorAll("td");
                                results.push({
                                    name: cols[0] ? cols[0] : null,
                                    result: cols[1] ? cols[1] : null,
                                });
                            });
                        }
                    }
                    resolve(results);
                });
            """
            )

            print("Sannysoft", output)
            return output
        except Exception as err:
            raise err

    async def recaptcha(self):
        try:
            await self.goto(
                "https://antcpt.com/eng/information/demo-form/recaptcha-3-test-score.html",
                15000,
            )

            element = self.page.locator("#score")
            output = await self.page.evaluate(
                "(element) => element.textContent", element
            )

            print("Recaptcha Score", output)
            return output
        except Exception as err:
            raise err

    async def hellobot(self):
        try:
            await self.goto("http://anonymity.space/hellobot.php", 3000)

            await self.page.locator("#result").is_visible()
            element = self.page.locator("#result")

            output = await element.get_attribute("textContent")

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

            print("Whiteops", output)
            return output
        except Exception as err:
            raise err

    

async def main():
    # browser = await async_playwright.chromium.launch()
    # context = await browser.newContext()
    # page = await context.newPage()
    proxy_option = "socks5://127.0.0.1:1080"

    pl = await PlaywrightAsyncDriverStealth.create(
        proxy=proxy_option,
        driver_type="firefox",
        timeout=300,
        headless=False,
    )
    await async_stealth(pl.page, pure=True)

    botcheck = Botcheck(pl.page)
    


    # botright_client = await Botright(headless=False)
    # browser = await botright_client.new_browser(proxy=proxy_option)
    # page = await browser.new_page()
    # botcheck = Botcheck(page)

    # # Continue by using the Page

    # await botright_client.close()

    # await pl.page.context.storage_state(path="1.json")
    # await async_stealth(self.page, pure=True)
    # undetected_driver
    # www.nowsecure.nl
    # https://bot.incolumitas.com/#botChallenge
    
    
    # await botcheck.isolatedWorld()
    # await botcheck.behaviorMonitor()
    await botcheck.f5networkloginForm()
    await botcheck.pixelscan()
    # await botcheck.sannysoft()
    # await botcheck.recaptcha()
    # await botcheck.hellobot()
    # await botcheck.areyouheadless()
    # await botcheck.fingerprintjs()
    await botcheck.datadome()
    await botcheck.whiteops()

    # await pl.browser.close()


asyncio.run(main())
