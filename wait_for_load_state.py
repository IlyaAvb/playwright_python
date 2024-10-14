import asyncio

from playwright.async_api import async_playwright, expect

async def main():
    uniswap_url = 'https://app.uniswap.org/swap'

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(uniswap_url)

        # await page.wait_for_load_state(state='load')

        # поиск по placeholder
        inputs = page.get_by_placeholder('0')

        await expect(inputs.first).to_be_visible()

        print(len(await inputs.all()))
        await context.close()


if __name__ == '__main__':
    asyncio.run(main())