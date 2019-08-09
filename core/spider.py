import time
import re
import core.config as config

from bs4 import BeautifulSoup
from collections.abc import Iterable
from selenium import webdriver

def get_base_website_name_from_url(url):
    # Get the base website name from a website's URL
    base_website_name = re.sub('http[A-Z]?://', '', url)
    base_website_name = base_website_name.split('/')[0]

    return base_website_name


def crawl_website(driver, base_url, level_to_crawl=1):
    print(f"{config.SPIDER_INDICATOR} Starting spider...")
    print(f"{config.SPIDER_INDICATOR} Crawling {base_url}...")

    # Get URL and wait for page to load (JavaScript & SPAs)
    driver.get(base_url)
    time.sleep(config.SPA_LOAD_WAIT_TIME)

    # Base website name from base_url
    base_website_name = get_base_website_name_from_url(base_url)

    # Get all links to potential product pages
    urls_found = {
        elm.get_attribute('href') for elm in 
        driver.find_elements_by_xpath("//a[@href]") 
        if base_website_name in elm.get_attribute('href')
    }

    print(f"{config.SPIDER_INDICATOR} Complete!")
    print(f"{config.SPIDER_INDICATOR} {len(urls_found)} URLS found.")
    print('')

    return urls_found
