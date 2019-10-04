import os
import time
import json
import core.config as config
import core.bot_scripts as bot_scripts
import selenium

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Load dotenv variables
from dotenv import load_dotenv
load_dotenv()

checkout_info = {
    # shipping info
    "shipping_email": os.getenv("SHIPPING_EMAIL", ''),
    "shipping_first_name": os.getenv('SHIPPING_FIRST_NAME', ''),
    "shipping_last_name": os.getenv('SHIPPING_LAST_NAME', ''),
    "shipping_address": os.getenv('SHIPPING_ADDRESS', ''),
    "shipping_address_two": os.getenv('SHIPPING_ADDRESS_TWO', ''),
    "shipping_city": os.getenv('SHIPPING_CITY', ''),
    "shipping_state": os.getenv('SHIPPING_STATE', ''),
    "shipping_zipcode": os.getenv('SHIPPING_ZIPCODE', ''),
    "shipping_phone": os.getenv('SHIPPING_PHONE', ''),

    # billing info
    "billing_email": os.getenv('BILLING_EMAIL', ''),
    "billing_first_name": os.getenv('BILLING_FIRST_NAME', ''),
    "billing_last_name": os.getenv('BILLING_LAST_NAME', ''),
    "billing_address": os.getenv('BILLING_ADDRESS', ''),
    "billing_address_two": os.getenv('BILLING_ADDRESS_TWO', ''),
    "billing_city": os.getenv('BILLING_CITY', ''),
    "billing_state": os.getenv('BILLING_STATE', ''),
    "billing_zipcode": os.getenv('BILLING_ZIPCODE', ''),
    "billing_phone": os.getenv('BILLING_PHONE', ''),

    # card info
    "CC_NUMBER": os.getenv('CC_NUMBER'),
    "CC_NAME": os.getenv('CARD_NAME'),
    "CC_EXPIRATION": os.getenv('CARD_EXPIRY'),
    "CC_VERIFICATION": os.getenv('CARD_VERIFICATION'),
}


def checkout_from_url(domain, variant, product_url):
    print(f"{config.OMBOT_INDICATOR} Starting OMBot...")

    checkout_info.update(variant)

    with open('core/cached_oms_xpaths.json') as paths:
        paths = json.loads(paths.read())
        actions = paths[domain]['actions']
        print(f"{config.OMBOT_INDICATOR} Actions loaded for {domain}!")

    # Start selenium session with Chrome driver
    chrome_options = webdriver.ChromeOptions()
    # Comment this out to watch the bots go :D
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    print(f'{config.OMBOT_INDICATOR} Getting {product_url}')
    driver.get(product_url)
    time.sleep(10)

    for action in paths[domain]['actions']:
        xpath = action['xpath'].format(**checkout_info)

        if action['type'] == 'click':
            print(f'{config.OMBOT_INDICATOR} Clicking {action["name"]}.')
            elm = driver.find_element_by_xpath(xpath)
            elm.click()
        elif action['type'] == 'input':
            input_val = action['value'].format(**checkout_info)
            print(
                f'{config.OMBOT_INDICATOR} Sending "{input_val}" to {action["name"]}.')
            elm = driver.find_element_by_xpath(xpath)
            elm.send_keys(input_val)
        elif action['type'] == 'select':
            input_val = action['value'].format(**checkout_info)
            print(
                f'{config.OMBOT_INDICATOR} Sending "{input_val}" to {action["name"]}.')
            select = Select(driver.find_element_by_xpath(xpath))
            select.select_by_visible_text(input_val)
        elif action['type'] == 'frame':
            print(
                f'{config.OMBOT_INDICATOR} Changing frame to {action["name"]}.')
            frame = driver.find_element_by_xpath(xpath)
            driver.switch_to.frame(frame)

        time.sleep(action['wait'])


checkout_from_url(
    'adidas', 
    {'size': 'M 12.5 / W 13.5'},
    'https://www.adidas.com/us/nmd_r1-shoes/B42200.html')

