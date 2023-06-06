import asyncio
from playwright import async_playwright

async def sleep(ms):
    await asyncio.sleep(ms / 1000)

async def solve_challenge(page):
    await page.wait_for_selector('#formStuff')
    user_name_input = await page.query_selector('[name="userName"]')
    await user_name_input.click(click_count=3)
    await user_name_input.type("bot3000")

    email_input = await page.query_selector('[name="eMail"]')
    await email_input.click(click_count=3)
    await email_input.type("bot3000@gmail.com")

    await page.select_option('[name="cookies"]', 'I want all the Cookies')
    await page.click('#smolCat')
    await page.click('#bigCat')
    await page.click('#submit')

    async def handle_dialog(dialog):
        print(dialog.message())
        await dialog.accept()

    page.on('dialog', handle_dialog)

    await page.wait_for_selector('#tableStuff tbody tr .url')
    await sleep(100)

    await page.wait_for_selector('#updatePrice0')
    await page.click('#updatePrice0')
    await page.wait_for_function('!!document.getElementById("price0").getAttribute("data-last-update")')

    await page.wait_for_selector('#updatePrice1')
    await page.click('#updatePrice1')
    await page.wait_for_function('!!document.getElementById("price1").getAttribute("data-last-update")')

    data = await page.evaluate('''() => {
        let results = [];
        document.querySelectorAll('#tableStuff tbody tr').forEach((row) => {
            results.push({
                name: row.querySelector('.name').innerText,
                price: row.querySelector('.price').innerText,
                url: row.querySelector('.url').innerText,
            })
        });
        return results;
    }''')

    print(data)

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False, args=['--start-maximized'])
        context = await browser.new_context(viewport=None)
        page = await context.new_page()

        await page.goto('https://bot.incolumitas.com/')

        await solve_challenge(page)

        await sleep(6000)

        new_tests = await page.inner_text('#new-tests')
        old_tests = await page.inner_text('#detection-tests')

        print(new_tests)
        print(old_tests)

        # await page.close()
        await browser.close()

asyncio.run(main())