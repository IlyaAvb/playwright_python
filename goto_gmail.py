import json
import asyncio
from asyncio import timeout
from datetime import timedelta
from pathlib import Path
from fake_useragent import FakeUserAgent
from nose.tools import timed

from playwright.async_api import async_playwright, expect

email_login = 'ponomorevqqq@gmail.com'
email_pass = '01072002Ilya'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://gmail.com')
        await page.wait_for_timeout(50000)

        cookies = await context.cookies()
        print(cookies)
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)




if __name__ == '__main__':
    asyncio.run(main())