# Import needed libraries
import json
import csv
import time
import pyfiglet

from bs4 import BeautifulSoup
from collections.abc import Iterable
from selenium import webdriver
from termcolor import colored


# Print PyProduct banner
ascii_banner = pyfiglet.figlet_format("PyProduct v.1.1")
print(colored(ascii_banner, 'blue'))
print("By Elgin Beloy\n")

# Text to show before Spider related outputs
SPIDER_INDICATOR = colored("[Spider] ", 'blue')

# Wait time for Selenium before getting page source. Helpful for AJAX based
# code fetching.
SPA_LOAD_WAIT_TIME = 1

# HTML elements to search when looking for product data.
TAGS_TO_SEARCH = ['a', 'p', 'h1', 'h2', 'h3', 'h4', 'span', 'div']

# Options (attribute values) for product name, description, image, and price.
NAME_TAG_OPTIONS = {"product-slide-title", "product-display-name", "brand", "product__name"}
DESCRIPTION_TAG_OPTIONS = {"product-slide-subtitle", "product-subtitle", "name", "product__color-info"}
PRICE_TAG_OPTIONS = {"local", "js-plpPrice"}
IMAGE_TAG_OPTIONS = {'grid-item-image', 'image-frame', 'product__image'}

# TODO: Options (tag content values) for product name, description, image, and price.
PRICE_CONTENT_OPTIONS = {"$"}

# TODO: availability
AVAILABILITY_OPTIONS = []

# Amount of products to show on output for spider search completion.
PRODUCTS_TO_SHOW = 5

# Output file to write to with results
OUTPUT_FILE = "./output/output.tsv"

BRAND_URLS = [
    'https://store.nike.com/us/en_us/pw/mens-running-shoes/7puZ8yzZoi3',
    'https://store.nike.com/us/en_us/pw/mens-tracksuits/7puZs9h',
    'https://store.nike.com/us/en_us/pw/mens-tops-t-shirts/7puZobp',
    'https://www.jennikayne.com/category/shoes/flats'
]

products = []

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def add_or_append_product(product_attr, contents, brand_url):
    exsisting_product_appended = False
    for product in products:
        if product.get(product_attr, None) == None and product['brand_url'] == brand_url:
            product[product_attr] = contents
            exsisting_product_appended = True
            break

    if not exsisting_product_appended:
        products.append({ product_attr: contents, 'brand_url': brand_url })

print(f"{SPIDER_INDICATOR} Starting spider scraper...")
for brand_url in BRAND_URLS:

    print(f"{SPIDER_INDICATOR} Getting {brand_url}...")

    # Start selenium session with Chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080');
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    # Get URL and wait for product page to load (JavaScript & SPAs)
    driver.get(brand_url)
    time.sleep(SPA_LOAD_WAIT_TIME)

    # Get page source after load and format with BeautifulSoup
    loadedPageSource = driver.page_source
    full_page_soup = BeautifulSoup(loadedPageSource, 'html.parser')

    # Get list of tags to search
    tags_to_search = full_page_soup.find_all(TAGS_TO_SEARCH)

    # Search each tag as potential name, description, image_url, or price
    for (tag_index, tag) in enumerate(tags_to_search):

        tag_values = list(tag.attrs.values())
        tag_values_flat = list(flatten(tag_values))

        tag_contents =  ' '.join(tag.text.split())

        if NAME_TAG_OPTIONS.intersection(tag_values_flat):
            add_or_append_product('name', tag_contents, brand_url)
            continue

        if DESCRIPTION_TAG_OPTIONS.intersection(tag_values_flat):
            add_or_append_product('description', tag_contents, brand_url)
            continue

        if PRICE_TAG_OPTIONS.intersection(tag_values_flat):
            add_or_append_product('price', tag_contents, brand_url)
            continue

        if IMAGE_TAG_OPTIONS.intersection(tag_values_flat):
            # Get nearest image child in container and use src as image_url
            add_or_append_product('image_url', tag.find('img').attrs['src'], brand_url)
            continue

    print(f"{SPIDER_INDICATOR} Complete!")

# Show user products scraped
print(f"{SPIDER_INDICATOR} Products scraped:")
for product in products[:PRODUCTS_TO_SHOW]:
    print('Name: ' + str(product.get('name', '')))
    print('Description: ' + str(product.get('description', '')))
    print('Image URL: ' + str(product.get('image_url', '')))
    print('Price: ' + str(product.get('price', '')))
    print('')

print(f'... { max(0, len(products) - PRODUCTS_TO_SHOW) } more results ...\n')

print(f"{SPIDER_INDICATOR} Writing output to {OUTPUT_FILE}...")

keys = products[0].keys()
with open(OUTPUT_FILE, 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
    dict_writer.writeheader()
    dict_writer.writerows(products)

print(f"{SPIDER_INDICATOR} Complete!")
