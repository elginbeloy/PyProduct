# Import needed libraries
import core.config as config

from joblib import Parallel, delayed
from selenium import webdriver
from core.spider import crawl_website
from core.scraper import scrape_products

def get_default_driver():
    # Start selenium session with Chrome driver
    chrome_options = webdriver.ChromeOptions()
    # Comment this out to watch the bots go :D
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument(
        f'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    return driver


def create_browser_scrape_job(url, not_found_value, max_product_limit):
    return scrape_products(get_default_driver(), url, not_found_value)


def scrape_websites(websites, verbose, not_found_value, max_product_limit):
    # TODO: Make this a unique set of dicts based on values.
    total_products_found = {}

    for website in websites:
        # Get all potential URLs from website
        # TODO: make this more efficient at indexing
        urls_to_scrape = crawl_website(get_default_driver(), website)

        product_batches = Parallel(n_jobs=-1, verbose=verbose)(delayed(create_browser_scrape_job)(
            url,
            not_found_value,
            max_product_limit
        ) for url in urls_to_scrape) # TODO: do all after better indexing is achieved 

        for product_list in product_batches:
            for product in product_list:
                total_products_found[product['name']] = product

    return total_products_found
