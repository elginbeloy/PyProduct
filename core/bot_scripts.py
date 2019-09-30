import time
import core.config as config


def scroll_until_done(driver):
    with open('./core/js/scroll.js') as js_file:
        scroll_js = js_file.read()
        current_height = driver.execute_script(scroll_js)

    print(f'{config.PAGE_BOT_INDICATOR} Scrolled {scroll_times} times for additional content.')
