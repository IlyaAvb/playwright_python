import json
import asyncio
from asyncio import timeout
from datetime import timedelta
from pathlib import Path
from fake_useragent import FakeUserAgent
from nose.tools import timed

from playwright.async_api import async_playwright, expect

EXTENTION_PATH = 'C:/Users/ponom/AppData/Local/Google/Chrome/User Data/Default/Extensions/nkbihfbeogaeaoehlefnkodbefgpgknn/12.4.1_0/'
MM_PASSWORD = 'password12345'
# nkbihfbeogaeaoehlefnkodbefgpgknn

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=[
                f"--disable-extensions-except={EXTENTION_PATH}",
                f"--load-extension={EXTENTION_PATH}",
            ],
            # slow_mo=500
        )

        background = context.service_workers[0]
        if not background:
            background = context.wait_for_event("serviceworker")

        titles = [await p.title() for p in context.pages]
        while 'MetaMask' not in titles:
            titles = [await p.title() for p in context.pages]

        mm_page = context.pages[1]
        await mm_page.wait_for_load_state()

        # checkbox = mm_page.locator('#onboarding__terms-checkbox')
        # await expect(checkbox).to_be_visible()
        # await checkbox.click()

        checkbox = mm_page.locator('#onboarding__terms-checkbox')
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        create_wallet_btn = mm_page.get_by_test_id(test_id='onboarding-create-wallet')
        await expect(create_wallet_btn).to_be_enabled()
        await expect(create_wallet_btn).to_be_visible()
        await create_wallet_btn.click()

        no_thanks_btn = mm_page.get_by_test_id(test_id='metametrics-no-thanks')
        await expect(no_thanks_btn).to_be_attached()
        await no_thanks_btn.click()

        password1 = mm_page.get_by_test_id(test_id='create-password-new')
        password2 = mm_page.get_by_test_id(test_id='create-password-confirm')
        check_box = mm_page.get_by_test_id(test_id='create-password-terms')
        create_wallet = mm_page.get_by_test_id(test_id='create-password-wallet')
        await expect(password1).to_be_attached()
        await password1.fill(MM_PASSWORD)
        await password2.fill(MM_PASSWORD)
        await check_box.click()

        await expect(create_wallet).to_be_enabled()
        await create_wallet.click()

        protect_wallet_btn = mm_page.get_by_test_id(test_id='secure-wallet-recommended')
        await expect(protect_wallet_btn).to_be_attached()
        await protect_wallet_btn.click()

        recovery_phrase_btn = mm_page.get_by_test_id(test_id='recovery-phrase-reveal')
        await expect(recovery_phrase_btn).to_be_attached()
        await recovery_phrase_btn.click()

        seed_phrase = []

        for i in range(12):
            seed_phrase.append(
                await mm_page.get_by_test_id(test_id=f'recovery-phrase-chip-{i}').inner_text()
            )
        print(seed_phrase)

        recovery_phrase_next = mm_page.get_by_test_id(test_id='recovery-phrase-next')
        await recovery_phrase_next.click()


        seed_phrase_field = mm_page.get_by_test_id(test_id='recovery-phrase-input-2')
        await expect(seed_phrase_field).to_be_attached()

        await mm_page.get_by_test_id(test_id='recovery-phrase-input-2').fill(seed_phrase[2])
        await mm_page.get_by_test_id(test_id='recovery-phrase-input-3').fill(seed_phrase[3])
        await mm_page.get_by_test_id(test_id='recovery-phrase-input-7').fill(seed_phrase[7])

        confirm_phrase = mm_page.get_by_test_id(test_id='recovery-phrase-confirm')
        await expect(confirm_phrase).to_be_enabled()
        await confirm_phrase.click()

        got_it_btn = mm_page.get_by_test_id('onboarding-complete-done')
        await expect(got_it_btn).to_be_attached()
        await got_it_btn.click()

        got_it_btn = mm_page.get_by_test_id('pin-extension-next')
        await expect(got_it_btn).to_be_attached()
        await got_it_btn.click()

        got_it_btn = mm_page.get_by_test_id(test_id='pin-extension-done')
        await expect(got_it_btn).to_be_attached()
        await got_it_btn.click()


        await mm_page.close()

        await asyncio.sleep(50)

if __name__ == '__main__':
    asyncio.run(main())