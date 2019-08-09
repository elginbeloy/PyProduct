from termcolor import colored

# Text to show before spider related outputs
PYPRODUCT_INDICATOR = colored('[PyProduct] ', 'red')

# Text to show before scraper related outputs
SCRAPER_INDICATOR = colored('[Scraper] ', 'blue')

# Text to show before spider related outputs
SPIDER_INDICATOR = colored('[Spider] ', 'green')

# Text to show before spider related outputs
PAGE_BOT_INDICATOR = colored('[PageBot] ', 'yellow')

# Wait time for Selenium before getting page source. Helpful for AJAX based
# code fetching.
SPA_LOAD_WAIT_TIME = 2

# Max amount of scrolls bot will do before being done.
# NOTE: Need to limit for infinite scrolling catalogs
SCROLL_LIMIT = 10

# HTML elements to search when looking for product data.
TAGS_TO_SEARCH = ['a', 'p', 'h1', 'h2', 'h3', 'h4', 'span', 'div']

# Options (attribute values) for product name, description, image, and price.
NAME_TAG_OPTIONS = {
    'product-card__title', 
    'product-slide-title',
    'product-display-name', 
    'product__name',
    'name'
}

DESCRIPTION_TAG_OPTIONS = {
    'product-card__subtitle',
    'product-slide-subtitle', 
    'product-subtitle', 
    'desc',
    'subtitle',
    'product__color-info'
}

PRICE_TAG_OPTIONS = {
    'product-card__price',
    'product-price',
    'local', 
    'js-plpPrice'
}

IMAGE_TAG_OPTIONS = {
    'product-card__hero-image',
    'grid-item-image', 
    'image-frame', 
    'product__image'
}

# TODO: Options (tag content values) for product name, description, image, and price.
PRICE_CONTENT_OPTIONS = {'$'}

# TODO: availability
AVAILABILITY_OPTIONS = []

# Amount of products to show on output of search completion.
PRODUCTS_TO_SHOW = 5

# Output file to write to with results
DEFAULT_OUTPUT_FILE = './output.tsv'

# Default website URLs if none are specified
DEFAULT_WEBSITE_URLS = [
    'https://store.nike.com',
    'https://www.jennikayne.com'
]
