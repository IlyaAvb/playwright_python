import asyncio

from playwright.async_api import async_playwright

async def main():
    uniswap_url = 'https://app.uniswap.org/swap'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # инициалиировать контекст
        # https://playwright.dev/python/docs/api/class-browsercontext
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(uniswap_url)

        await asyncio.sleep(10)
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())