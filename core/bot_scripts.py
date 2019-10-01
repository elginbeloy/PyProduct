import time
import core.config as config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

def scroll_until_done(driver):
    with open('./core/js/scroll.js') as js_file:
        scroll_js = js_file.read()
        driver.execute_script(scroll_js)

    try:
        WebDriverWait(driver, 500).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//div[@id='pyproduct__scrolling-complete-node']")))
    except:
        print(f'Timeout at URL: {driver.current_url}')
