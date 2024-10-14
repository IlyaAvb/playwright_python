from playwright.sync_api import sync_playwright


# открыть соединение
with sync_playwright() as p:
    # инициализация браузера (без видимого открытия браузера)
    browser = p.chromium.launch()

    # инициализация браузера (с явным открытием браузера)
    # browser = p.chromium.launch(headless=False)
    # инициализация страницы
    page = browser.new_page()
    # переход по url адресу:
    page.goto('https://webdriver.io/docs/component-testing/')


    # сделать скриншот
    page.screenshot(path='./demo.png')
    browser.close()