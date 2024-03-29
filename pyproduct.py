# Import needed libraries
import csv
import pyfiglet
import argparse
import core.config as config

from joblib import Parallel, delayed
from termcolor import colored
from core.browser_pool import scrape_websites
from core.ombot import checkout_from_url 


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
parser.add_argument('-c', '--checkout', type=str, default=None,
    help='URL to test checkout on adidas.com using OMBot.')

args = parser.parse_args()

if __name__ == '__main__':
    # Print PyProduct banner
    ascii_banner = pyfiglet.figlet_format("PyProduct v.1.3")
    print(colored(ascii_banner, 'blue'))
    print("By Elgin Beloy\n")

    if args.checkout:
        checkout_from_url(
            'adidas',
            {'size': 'M 12.5 / W 13.5'},
            args.checkout)
        
        exit()


    total_products_found = scrape_websites(
        args.websites, args.verbose, args.not_found_value, args.not_found_value)

    products_found_values = list(total_products_found.values())

    # Show user some of the products scraped
    print(f"{config.PYPRODUCT_INDICATOR} Products scraped:")
    print()
    for product in products_found_values[:config.PRODUCTS_TO_SHOW]:
        print('Name: ' + str(product.get('name', '')))
        print('Description: ' + str(product.get('description', '')))
        print('Image URL: ' + str(product.get('image', '')))
        print('Price: ' + str(product.get('price', '')))
        print()

    products_not_shown = len(products_found_values) - config.PRODUCTS_TO_SHOW
    products_not_shown = max(0, products_not_shown)
    print(f'... { products_not_shown } more results ...\n')

    print(f"{config.PYPRODUCT_INDICATOR} Writing output to {args.output}...")

    # Write output to TSV output file based on first dicts keys
    keys = products_found_values[0].keys()
    with open(args.output, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(products_found_values)

    print(f"{config.PYPRODUCT_INDICATOR} Complete!")
