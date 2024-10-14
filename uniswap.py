import asyncio
from fake_useragent import FakeUserAgent
from playwright.async_api import async_playwright, expect
from seleniumwire.thirdparty.mitmproxy.net.http.encoding import encode_zstd

TO_TOKEN_ADDRESS = '0xdac17f958d2ee523a2206206994597c13d831ec7'  # USDT

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        user_agent = FakeUserAgent().random
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()
        await page.goto('https://app.uniswap.org/swap', timeout=60000)

        await asyncio.sleep(5)
        try:
            dismiss_btn = page.locator('span.font_button:has-text("Dismiss")')
            await expect(dismiss_btn).to_be_visible()
            await dismiss_btn.click()
            await page.wait_for_timeout(1000)
        except Exception as error:
            print(error)

        inputs = page.get_by_placeholder('0')
        await expect(inputs.first).to_be_visible()
        await inputs.first.type('0.0001', delay=300)
        await page.wait_for_timeout(1000)

        choose_token = page.locator('//*[@id="swap-currency-output"]/div/div[1]/div[2]/div/button/span/div/div/span')
        await expect(choose_token).to_be_visible()
        await choose_token.click()
        await page.wait_for_timeout(1000)

        token_name_input = page.locator('input[data-testid="explore-search-input"]')
        await expect(token_name_input).to_be_visible()
        await token_name_input.type(TO_TOKEN_ADDRESS)
        await page.wait_for_timeout(1000)

        # target_token = page.locator('//html/body/div[5]/span/span/div/div[2]/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div/div')
        # await expect(target_token).to_be_visible()
        # await target_token.click()

        target_token = page.get_by_test_id('token-option-1-USDT')
        await expect(target_token).to_be_visible()
        await target_token.click()

        await asyncio.sleep(10)



if __name__ == '__main__':
    asyncio.run(main())