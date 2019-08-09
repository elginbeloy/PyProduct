# Import needed libraries
import core.config as config

from joblib import Parallel, delayed
from selenium import webdriver
from core.spider import crawl_website
from core.scraper import scrape_products


def scrape_websites(websites, verbose, not_found_value, max_product_limit):
    # Start selenium session with Chrome driver
    chrome_options = webdriver.ChromeOptions()
    # Comment this out to watch the bots go :D
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    # TODO: Make this a unique set of dicts based on values.
    total_products_found = []

    for website in websites:
        urls_to_scrape = crawl_website(driver, website)

        product_batches = Parallel(n_jobs=-1, verbose=verbose)(delayed(create_browser_scrape_job)(
            url,
            not_found_value,
            max_product_limit
        ) for url in urls_to_scrape[0:10])

        products_from_website = [
            product for product_list in product_batches for product in product_list]

        total_products_found.extend(products_from_website)


    return total_products_found


def create_browser_scrape_job(url, not_found_value, max_product_limit):
    # Start selenium session with Chrome driver
    chrome_options = webdriver.ChromeOptions()
    # Comment this out to watch the bots go :D
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    # TODO: Make this a unique set of dicts based on values.
    return scrape_products(driver, url, not_found_value)  

'''
print(f"{config.PYPRODUCT_INDICATOR} Update: {len(total_products_found)} total products scraped.")
        print('')
'''
