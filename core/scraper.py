import time
import core.config as config

from bs4 import BeautifulSoup
from collections.abc import Iterable

def flatten_list(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten_list(el)
        else:
            yield el


def add_or_append_product(product_attr, products, contents, brand_url):
    existing_product_appended = False
    for product in products:
        if product.get(product_attr, None) == None and product['brand_url'] == brand_url:
            product[product_attr] = contents
            existing_product_appended = True
            break

    if not existing_product_appended:
        products.append({product_attr: contents, 'brand_url': brand_url})


def scrape_products(driver, website):
    print(f"{config.SCRAPER_INDICATOR} Starting scraper...")
    print(f"{config.SCRAPER_INDICATOR} Scraping {website}...")

    products_found = []

    # Get URL and wait for page to load (JavaScript & SPAs)
    driver.get(website)
    time.sleep(config.SPA_LOAD_WAIT_TIME)

    # Get page source after load and format with BeautifulSoup
    loadedPageSource = driver.page_source
    full_page_soup = BeautifulSoup(loadedPageSource, 'html.parser')

    # Get list of tags to search
    tags_to_search = full_page_soup.find_all(config.TAGS_TO_SEARCH)

    # Search each tag as potential name, description, image_url, or price
    for tag in tags_to_search:

        tag_values = list(tag.attrs.values())
        tag_values_flat = list(flatten_list(tag_values))

        tag_contents =  ' '.join(tag.text.split())

        if config.NAME_TAG_OPTIONS.intersection(tag_values_flat):
            add_or_append_product('name', products_found,
                tag_contents, website)
            continue

        if config.DESCRIPTION_TAG_OPTIONS.intersection(tag_values_flat):
            add_or_append_product('description', products_found,
                tag_contents, website)
            continue

        if config.PRICE_TAG_OPTIONS.intersection(tag_values_flat):
            add_or_append_product('price', products_found,
                tag_contents, website)
            continue

        if config.IMAGE_TAG_OPTIONS.intersection(tag_values_flat):
            # Get nearest image child in container and use src as image_url
            add_or_append_product('image_url', products_found, tag.find(
                'img').attrs['src'], website)
            continue

    print(f"{config.SCRAPER_INDICATOR} Complete!")
    print(f"{config.SCRAPER_INDICATOR} {len(products_found)} products found.")
    print('')

    return products_found
