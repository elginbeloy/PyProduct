import time
import json
import tldextract
import core.config as config

from selenium.common.exceptions import NoSuchElementException
from core.bot_scripts import scroll_until_done

def get_cached_xpaths():
    with open('core/cached_xpaths.json') as xpaths_file:
        return json.loads(xpaths_file.read())


def get_product_tag_attr(domain_xpath, product_container, xpath_name, attr_name, domain, not_found_value):
    try:
        if attr_name == 'text':
            return product_container.find_element_by_xpath(
                domain_xpath[xpath_name]).text

        return product_container.find_element_by_xpath(
            domain_xpath[xpath_name]).get_attribute(attr_name)
    except NoSuchElementException:
        print(f'{config.SCRAPER_INDICATOR} Element {xpath_name} not found.')
        return not_found_value


def get_product_tag_text(domain_xpath, product_container, xpath_name, attr_name, domain, not_found_value):
    try:
        return product_container.find_element_by_xpath(
            domain_xpath[xpath_name]).text
    except NoSuchElementException:
        print(f'{config.SCRAPER_INDICATOR} Element {xpath_name} not found.')
        return not_found_value


def get_product_image_attr(domain_xpath, product_container, attr_name, domain, not_found_value):
    try:
        image_container = product_container.find_element_by_xpath(
            domain_xpath[attr_name])
        if image_container.get_attribute('src') != None:
            return image_container.get_attribute('src')
        else:
            return image_container.find_element_by_xpath(
                '//img').get_attribute('src')
    except NoSuchElementException:
        print(f'{config.SCRAPER_INDICATOR} Element {attr_name} not found.')
        return not_found_value


def scrape_products(driver, website, not_found_value):
    # TODO: Use default xpath or autogenerate when not found
    try:
        domain = tldextract.extract(website).domain
        domain_xpath = get_cached_xpaths().get(domain)
    except:
        print(f"{config.SCRAPER_INDICATOR} !! xpath error:")
        print(f"Unable to get cached xpath for {website}!")
        exit()

    products_found = []

    # Get URL and wait for page to load (JavaScript & SPAs)
    driver.get(website)
    time.sleep(config.SPA_LOAD_WAIT_TIME)
    
    # Scroll page before getting products
    scroll_until_done(driver)
    time.sleep(config.SPA_LOAD_WAIT_TIME)

    # Go through all products by parent container
    product_containers = driver.find_elements_by_xpath(
        domain_xpath['container'])
    for product_container in product_containers:

        current_product = {
            'name': get_product_tag_attr(domain_xpath, product_container, 'name', 'text', domain, not_found_value),
            'description': get_product_tag_attr(domain_xpath, product_container, 'description', 'text', domain, not_found_value),
            'image': get_product_image_attr(domain_xpath, product_container, 'image', domain, not_found_value),
            'price': get_product_tag_attr(domain_xpath, product_container, 'price', 'text', domain, not_found_value),
            'domain': domain,
            'link': get_product_tag_attr(domain_xpath, product_container, 'link', 'href', domain, not_found_value)
        }

        products_found.append(current_product)

    if len(products_found) > 0:
        print(
            f"{config.SCRAPER_INDICATOR} {len(products_found)} more products found at")
        print(f"{config.SCRAPER_INDICATOR} {website}")

    return products_found
