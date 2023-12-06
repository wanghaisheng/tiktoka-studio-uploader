from playwright import async_playwright
from upgenius.utils.webdriver import PlaywrightAsyncDriver



class Botcheck:
    def __init__(self, page):
        self.page = page

    async def goto(self, url, delay=2000):
        try:
            if url:
                await self.page.goto(url, waitUntil="networkidle")
                await self.page.waitForTimeout(delay)
            else:
                raise ValueError("No url provided")
        except Exception as err:
            raise err

    async def isolatedWorld(self):
        try:
            await self.goto(
                "https://prescience-data.github.io/execution-monitor.html", 200
            )

            await self.page.querySelector("#result")

            await self.page.evaluate(
                """
                let newDiv = document.createElement("div");
                let newContent = document.createTextNode("Creating an element on the page.");
                newDiv.appendChild(newContent);
                let currentDiv = document.getElementById("div1");
                document.body.insertBefore(newDiv, currentDiv);
            """
            )

            await self.page.waitForTimeout(2000)

            element = await self.page.querySelector("#result")
            output = await element.getProperty("textContent").jsonValue()

            print("IsolatedWorld", output)
            return output
        except Exception as err:
            raise err

    async def behaviorMonitor(self):
        try:
            await self.goto(
                "https://prescience-data.github.io/behavior-monitor.html", 200
            )

            resultElement = await self.page.querySelector("#result")
            if not resultElement:
                raise ValueError("Failed to find #result")

            await resultElement.hover()
            await resultElement.click(delay=10)

            await self.page.waitForTimeout(200)

            inputElement = await self.page.querySelector("input#test-input")
            if not inputElement:
                raise ValueError("Failed to find input#test-input")

            await inputElement.click()
            await inputElement.type("Hello world...", delay=3)

            await self.page._client.send(
                "Input.synthesizeScrollGesture",
                {"x": 0, "y": 0, "xDistance": 0, "yDistance": -100},
            )

            await self.page.waitFor(2500)

            element = await self.page.querySelector("#result")
            output = await element.getProperty("textContent").jsonValue()

            print("BehaviorMonitor", output)
            return output
        except Exception as err:
            raise err

    async def f5network(self):
        try:
            await self.goto("https://ib.bri.co.id/ib-bri", 2000)

            element = await self.page.querySelector("form#loginForm")
            output = "Passed" if element else "Failed"

            print("F5 Network", output)
            return output
        except Exception as err:
            raise err

    async def pixelscan(self):
        try:
            await self.goto("https://pixelscan.net", 3000)

            element = await self.page.querySelector("span.consistency-status-text")
            output = await element.getProperty("textContent").jsonValue()

            print("PixelScan", "Browser Fingerprint: " + output)
            return output
        except Exception as err:
            raise err

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

            element = await self.page.querySelector("#score")
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

            await self.page.waitForSelector("#result")
            element = await self.page.querySelector("#result")

            output = await element.getProperty("textContent").jsonValue()

            print("HelloBot", output)
            return output
        except Exception as err:
            raise err

    async def areyouheadless(self):
        try:
            await self.goto("https://arh.antoinevastel.com/bots/areyouheadless", 2000)

            await self.page.waitForSelector("#res")
            element = await self.page.querySelector("#res")

            output = await element.getProperty("textContent").jsonValue()

            print("AreYouHeadless", output)
            return output
        except Exception as err:
            raise err

    async def fingerprintjs(self):
        try:
            await self.goto("https://fingerprintjs.com/demo", 5000)

            await self.page.waitForSelector("table.table-compact")
            element = await self.page.querySelector(
                "table.table-compact > tbody > tr:nth-child(4) > td.miriam"
            )

            text = await element.getProperty("textContent").jsonValue()
            output = "Passed" if text == "NO" else "Failed"

            print("FingerprintJS", output)
            return output
        except Exception as err:
            raise err

    async def datadome(self):
        try:
            await self.goto("https://datadome.co", 2000)

            button = await self.page.querySelector("#menu-item-18474")

            if button:
                await button.click(delay=10)
                await self.page.waitForNavigation(waitUntil="networkidle2")
                await self.page.waitFor(500)
            else:
                print("Could not find the button!")

            captcha = await self.page.querySelector(
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

            button = await self.page.querySelector(
                'a[href="https://www.whiteops.com/company/about"]'
            )

            if button:
                await button.click(delay=8)
                await self.page.waitForNavigation(waitUntil="networkidle2")
                await self.page.waitFor(500)
            else:
                print("Could not find the button!")

            test = await self.page.querySelector(
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

    pl = await PlaywrightAsyncDriver.create(
        proxy=proxy_option,
        driver_type="chromium",
        timeout=3000,
        use_stealth_js=True,
    )

    botcheck = Botcheck(pl.page)

    await botcheck.isolatedWorld()
    await botcheck.behaviorMonitor()
    await botcheck.f5network()
    await botcheck.pixelscan()
    await botcheck.sannysoft()
    await botcheck.recaptcha()
    await botcheck.hellobot()
    await botcheck.areyouheadless()
    await botcheck.fingerprintjs()
    await botcheck.datadome()
    await botcheck.whiteops()

    await pl.browser.close()
