# Import needed libraries
import csv
import pyfiglet
import argparse
import core.config as config

from core.spider import scrape_products
from termcolor import colored


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

    print(f"{config.SPIDER_INDICATOR} Starting spider scraper...")
    products_found = scrape_products(args.website)

    # Show user products scraped
    print(f"{config.SPIDER_INDICATOR} Products scraped:")
    print('')
    for product in products_found[:config.PRODUCTS_TO_SHOW]:
        print('Name: ' + str(product.get('name', '')))
        print('Description: ' + str(product.get('description', '')))
        print('Image URL: ' + str(product.get('image_url', '')))
        print('Price: ' + str(product.get('price', '')))
        print('')

    print(
        f'... { max(0, len(products_found) - config.PRODUCTS_TO_SHOW) } more results ...\n')

    print(f"{config.SPIDER_INDICATOR} Writing output to {args.output}...")

    keys = products_found[0].keys()
    with open(args.output, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(products_found)

    print(f"{config.SPIDER_INDICATOR} Complete!")
