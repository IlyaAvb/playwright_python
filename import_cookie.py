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
        await context.add_cookies(json.loads(Path('cookies.json').read_text()))

        page = await context.new_page()

        await page.goto('https://coinmarketcap.com/', timeout=100000)

        await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())