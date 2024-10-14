import asyncio

from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://whatmyuseragent.com/')
        await page.screenshot(path='./demo.png')
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())