# Import needed libraries
import csv
import pyfiglet
import argparse
import core.config as config

from selenium import webdriver
from termcolor import colored
from core.spider import crawl_website
from core.scraper import scrape_products


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--website', type=str, 
    default=config.DEFAULT_WEBSITE_URLS[0])
parser.add_argument('-o', '--output', type=str,
    default=config.DEFAULT_OUTPUT_FILE)
parser.add_argument('-v', '--verbose', type=int, default=1)
args = parser.parse_args()


if __name__ == '__main__':
    # Print PyProduct banner
    ascii_banner = pyfiglet.figlet_format("PyProduct v.1.2")
    print(colored(ascii_banner, 'blue'))
    print("By Elgin Beloy\n")


    # Start selenium session with Chrome driver
    chrome_options = webdriver.ChromeOptions()
    # Comment this out to watch the bot go :D
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)


    urls_to_scrape = crawl_website(driver, args.website)

    # TODO: Make this a unique set of dicts based on values.
    total_products_found = []
    for url in urls_to_scrape:
        batch_products_found = scrape_products(driver, url)
        total_products_found.extend(batch_products_found)
        print(f"{config.PYPRODUCT_INDICATOR} Update: {len(total_products_found)} total products scraped.")
        print('')

        # FOR LIMITING PURPOSES
        # if len(total_products_found) >= 500:
        #    break


    # Show user products scraped
    print(f"{config.PYPRODUCT_INDICATOR} Products scraped:")
    print('')
    for product in total_products_found[:config.PRODUCTS_TO_SHOW]:
        print('Name: ' + str(product.get('name', '')))
        print('Description: ' + str(product.get('description', '')))
        print('Image URL: ' + str(product.get('image_url', '')))
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
