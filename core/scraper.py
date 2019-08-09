import time
import tldextract
import core.config as config

from selenium.common.exceptions import NoSuchElementException
from core.bot_scripts import scroll_until_done
from core.cached_xpaths import cached_xpaths


def get_product_text_attr(product_container, attr_name, domain, not_found_value):
    try:
        return product_container.find_element_by_xpath(
            cached_xpaths[domain][attr_name]).text
    except NoSuchElementException:
        print(f'{config.SCRAPER_INDICATOR} Element {attr_name} not found.')
        return not_found_value
        

def get_product_image_attr(product_container, attr_name, domain, not_found_value):
    try:
        image_container = product_container.find_element_by_xpath(
            cached_xpaths[domain][attr_name])
        if image_container.get_attribute('src') != None:
            return image_container.get_attribute('src')
        else:
            return image_container.find_element_by_xpath(
                '//img').get_attribute('src')
    except NoSuchElementException:
        print(f'{config.SCRAPER_INDICATOR} Element {attr_name} not found.')
        return not_found_value


def scrape_products(driver, website, not_found_value):
    print(f"{config.SCRAPER_INDICATOR} Starting scraper...")
    print(f"{config.SCRAPER_INDICATOR} Scraping {website}...")

    domain = tldextract.extract(website).domain

    products_found = []

    # Get URL and wait for page to load (JavaScript & SPAs)
    driver.get(website)
    time.sleep(config.SPA_LOAD_WAIT_TIME)
    
    # Scroll page before getting products
    scroll_until_done(driver)

    # Go through all products by parent container
    product_containers = driver.find_elements_by_xpath(cached_xpaths[domain]['container'])
    for product_container in product_containers:

        current_product = {
            'name': get_product_text_attr(product_container, 'name',
                domain, not_found_value),
            'description': get_product_text_attr(product_container, 'description',
                domain, not_found_value),
            'image': get_product_image_attr(product_container, 'image',
                domain, not_found_value),
            'price': get_product_text_attr(product_container, 'price',
                domain, not_found_value),
        }

        products_found.append(current_product)

    print(f"{config.SCRAPER_INDICATOR} Complete!")
    print(f"{config.SCRAPER_INDICATOR} {len(products_found)} products found.")
    print('')

    return products_found
