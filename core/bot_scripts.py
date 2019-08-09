import time
import core.config as config


def scroll_until_done(driver):
    with open('./core/js/scroll.js') as js_file:
        scroll_js = js_file.read()
    
    last_height = None
    current_height = 0
    scroll_times = 0
    while (current_height != last_height and scroll_times < config.SCROLL_LIMIT):
        last_height = current_height
        time.sleep(config.SPA_LOAD_WAIT_TIME)
        current_height = driver.execute_script(scroll_js)
        scroll_times += 1

    print(f'{config.PAGE_BOT_INDICATOR} Scrolled {scroll_times} times for additional content.')
