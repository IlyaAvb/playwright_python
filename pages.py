import json
import asyncio
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

        await page.goto('https://app.uniswap.org/swap', timeout=100000)

        page2 = await context.new_page()
        await page2.goto('https://mail.google.com/mail/u/0/#inbox')


        print(context.pages)

        await context.pages[0].bring_to_front()

        await asyncio.sleep(10)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())