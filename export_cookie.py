import json
import asyncio
from pathlib import Path
from fake_useragent import FakeUserAgent

from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        user_agent = FakeUserAgent().random
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://coinmarketcap.com/', timeout=100000)

        cookies = await context.cookies()
        print(cookies)

        highlights = page.locator('label[id="1"]')
        await highlights.wait_for(state='visible')
        await highlights.click()

        cookies = await context.cookies()
        print(cookies)

        Path('cookies.json').write_text((json.dumps(cookies)))
        await asyncio.sleep(10)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())