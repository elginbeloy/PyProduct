import time
import tldextract
import core.config as config

from bs4 import BeautifulSoup
from collections.abc import Iterable
from selenium import webdriver

def is_same_domain(url_one, url_two):
    domain_one = tldextract.extract(url_one).domain
    domain_two = tldextract.extract(url_two).domain

    return domain_one == domain_two

def crawl_website(driver, base_url, level_to_crawl=1):
    print(f"{config.SPIDER_INDICATOR} Starting spider...")
    print(f"{config.SPIDER_INDICATOR} Crawling {base_url}...")

    # Get URL and wait for page to load (JavaScript & SPAs)
    driver.get(base_url)
    time.sleep(config.SPA_LOAD_WAIT_TIME)

    # Get all links to potential product pages with same domain
    urls_found = {
        elm.get_attribute('href') for elm in
        driver.find_elements_by_xpath("//a[@href]") 
        if elm.get_attribute('href') and 
        is_same_domain(base_url, elm.get_attribute('href'))
    }

    print(f"{config.SPIDER_INDICATOR} Complete!")
    print(f"{config.SPIDER_INDICATOR} {len(urls_found)} URLS found.")
    print('')

    return urls_found
