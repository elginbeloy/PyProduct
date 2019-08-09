# Import needed libraries
import csv
import pyfiglet
import argparse
import core.config as config

from selenium import webdriver
from termcolor import colored
from core.spider import crawl_website
from core.scraper import scrape_products


parser = argparse.ArgumentParser(
    prog='PyProduct',
    description='Python + Selenium + BeautifulSoup based web catalog scraper.')
parser.add_argument('-w', '--websites', type=str, nargs='+',
    default=config.DEFAULT_WEBSITE_URLS,
    help='Websites for PyProduct to scrape.')
parser.add_argument('-o', '--output', type=str,
    default=config.DEFAULT_OUTPUT_FILE,
    help='The output TSV file to write to once complete.')
parser.add_argument('--max-product-limit', type=int,
    default=config.DEFAULT_MAX_PRODUCT_LIMIT,
    help='The maximum amount of products to scrape before saving and quiting.')
parser.add_argument('--not-found-value', type=str, 
    default=config.DEFAULT_NOT_FOUND_VALUE,
    help='The default value for when a product attribute is not found.')
parser.add_argument('-v', '--verbose', type=int, default=1,
    help='The verbosity level for the CLI output log.')

args = parser.parse_args()

if __name__ == '__main__':
    # Print PyProduct banner
    ascii_banner = pyfiglet.figlet_format("PyProduct v.1.2")
    print(colored(ascii_banner, 'blue'))
    print("By Elgin Beloy\n")


    # Start selenium session with Chrome driver
    chrome_options = webdriver.ChromeOptions()
    # Comment this out to watch the bot go :D
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    # TODO: Make this a unique set of dicts based on values.
    total_products_found = []

    for website in args.websites:
        urls_to_scrape = crawl_website(driver, website)

        for url in urls_to_scrape:
            batch_products_found = scrape_products(
                driver, url, args.not_found_value)  
            total_products_found.extend(batch_products_found)
            print(f"{config.PYPRODUCT_INDICATOR} Update: {len(total_products_found)} total products scraped.")
            print('')

            # Break once met max products
            if len(total_products_found) >= args.max_product_limit:
                break
        
        # Break once met max products
        if len(total_products_found) >= args.max_product_limit:
            break


    # Show user products scraped
    print(f"{config.PYPRODUCT_INDICATOR} Products scraped:")
    print('')
    for product in total_products_found[:config.PRODUCTS_TO_SHOW]:
        print('Name: ' + str(product.get('name', '')))
        print('Description: ' + str(product.get('description', '')))
        print('Image URL: ' + str(product.get('image', '')))
        print('Price: ' + str(product.get('price', '')))
        print('')

    print(f'... { max(0, len(total_products_found) - config.PRODUCTS_TO_SHOW) } more results ...\n')

    print(f"{config.PYPRODUCT_INDICATOR} Writing output to {args.output}...")

    keys = total_products_found[0].keys()
    with open(args.output, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(total_products_found)

    print(f"{config.PYPRODUCT_INDICATOR} Complete!")
