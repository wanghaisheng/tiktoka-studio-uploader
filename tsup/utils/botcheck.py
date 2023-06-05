from playwright import async_playwright


class Botcheck:
    def __init__(self, page):
        self.page = page

    async def goto(self, url, delay=2000):
        try:
            if url:
                await self.page.goto(url, wait_until="networkidle")
                await self.page.wait_for_timeout(delay)
            else:
                raise ValueError("No URL provided")
        except Exception as err:
            raise err

    async def isolated_world(self):
        try:
            await self.goto(
                "https://prescience-data.github.io/execution-monitor.html", 200
            )

            await self.page.query_selector("#result")

            await self.page.evaluate(
                """
                let newDiv = document.createElement("div");
                let newContent = document.createTextNode("Creating an element on the page.");
                newDiv.appendChild(newContent);
                let currentDiv = document.getElementById("div1");
                document.body.insertBefore(newDiv, currentDiv);
            """
            )

            await self.page.wait_for_timeout(2000)

            element = await self.page.query_selector("#result")
            output = await (await element.property("textContent")).json_value()

            print("IsolatedWorld", output)
            return output
        except Exception as err:
            raise err

    async def behavior_monitor(self):
        try:
            await self.goto(
                "https://prescience-data.github.io/behavior-monitor.html", 200
            )

            result_element = await self.page.query_selector("#result")
            if not result_element:
                raise ValueError("Failed to find #result")

            await result_element.hover()
            await result_element.click(delay=10)

            await self.page.wait_for_timeout(200)

            input_element = await self.page.query_selector("input#test-input")
            if not input_element:
                raise ValueError("Failed to find input#test-input")

            await input_element.click()
            await input_element.type("Hello world...", delay=3)

            await self.page._client.send(
                "Input.synthesizeScrollGesture",
                {"x": 0, "y": 0, "xDistance": 0, "yDistance": -100},
            )

            await self.page.wait_for_timeout(2500)

            element = await self.page.query_selector("#result")
            output = await (await element.property("textContent")).json_value()

            print("BehaviorMonitor", output)
            return output
        except Exception as err:
            raise err

    async def f5network(self):
        try:
            await self.goto("https://ib.bri.co.id/ib-bri", 2000)

            element = await self.page.query_selector("form#loginForm")
            output = "Passed" if element else "Failed"

            print("F5 Network", output)
            return output
        except Exception as err:
            raise err

    async def pixelscan(self):
        try:
            await self.goto("https://pixelscan.net", 3000)

            element = await self.page.query_selector("span.consistency-status-text")
            output = await (await element.property("textContent")).json_value()

            print("PixelScan", "Browser Fingerprint: " + output)
            return output
        except Exception as err:
            raise err
