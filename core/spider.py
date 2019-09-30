import time
import json
import tldextract
import core.config as config
import re

from bs4 import BeautifulSoup
from collections.abc import Iterable
from selenium import webdriver


def get_product_url_pattern(base_url):
    with open('core/cached_xpaths.json') as xpaths_file:
        regex_str = json.loads(xpaths_file.read())[base_url]['product_url_regex']
        regex_pattern = re.compile(regex_str)
        return regex_pattern


def is_same_domain(url_one, url_two):
    domain_one = tldextract.extract(url_one).domain
    domain_two = tldextract.extract(url_two).domain

    return domain_one == domain_two


def crawl_website(driver, base_url, level_to_crawl=1):
    print(f"{config.SPIDER_INDICATOR} Starting spider...")
    print(f"{config.SPIDER_INDICATOR} Crawling {base_url}...")

    # Get URL and wait for page to load (JavaScript & SPAs)
    driver.get(base_url)

    # TODO: Use default xpath or autogenerate when not found
    try:
        # regex pattern to exclude product urls
        domain = tldextract.extract(base_url).domain
        product_url_regex = get_product_url_pattern(domain)
    except:
        print(f"{config.SCRAPER_INDICATOR} !! xpath error:")
        print(f"Unable to get cached xpath for {base_url}!")
        exit()

    urls_found = {}
    while len(urls_found) == 0:
        # Get all links to potential product pages with same domain
        # TODO: Make this go deeper than initial page. 
        urls_found = {
            elm.get_attribute('href') for elm in
            driver.find_elements_by_xpath("//a[@href]") 
            if elm.get_attribute('href') and 
            is_same_domain(base_url, elm.get_attribute('href'))
            and not bool(product_url_regex.search(elm.get_attribute('href')))
        }

        time.sleep(config.SPA_LOAD_WAIT_TIME)

    print(f"{config.SPIDER_INDICATOR} Complete!")
    print(f"{config.SPIDER_INDICATOR} {len(urls_found)} URLS found.")
    print('')

    return list(urls_found)
