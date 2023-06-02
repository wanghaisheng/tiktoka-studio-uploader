import asyncio
from playwright.async_api import async_playwright
from cf_clearance import async_cf_retry, async_stealth
import requests


## bypass cf challenge
async def main():
    # not use cf_clearance, cf challenge is fail
    proxy_sever = "socks5://127.0.0.1:1080"
    proxies = {"all": proxy_sever}
    res = requests.get("https://nowsecure.nl", proxies=proxies)
    if "<title>Just a moment...</title>" in res.text:
        print("cf challenge fail")
    # get cf_clearance
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, proxy={"server": proxy_sever})
        page = await browser.new_page()
        page.evaluate(
            "document.body.appendChild(Object.assign(document.createElement('script'), {src: 'https://gitcdn.xyz/repo/berstend/puppeteer-extra/stealth-js/stealth.min.js'}))"
        )
        await async_stealth(page, pure=True)
        await page.goto("https://nowsecure.nl")
        res = await async_cf_retry(page)
        if res:
            cookies = await page.context.cookies()
            for cookie in cookies:
                if cookie.get("name") == "cf_clearance":
                    cf_clearance_value = cookie.get("value")
                    print(cf_clearance_value)
            ua = await page.evaluate("() => {return navigator.userAgent}")
            print(ua)
        else:
            print("cf challenge fail")
        await browser.close()
    # use cf_clearance, must be same IP and UA
    headers = {"user-agent": ua}
    cookies = {"cf_clearance": cf_clearance_value}
    res = requests.get(
        "https://nowsecure.nl", proxies=proxies, headers=headers, cookies=cookies
    )
    if "<title>Just a moment...</title>" not in res.text:
        print("cf challenge success")


asyncio.get_event_loop().run_until_complete(main())
