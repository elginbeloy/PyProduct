from termcolor import colored

# Text to show before Spider related outputs
SPIDER_INDICATOR = colored('[Spider] ', 'blue')

# Wait time for Selenium before getting page source. Helpful for AJAX based
# code fetching.
SPA_LOAD_WAIT_TIME = 2

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

# Amount of products to show on output for spider search completion.
PRODUCTS_TO_SHOW = 5

# Output file to write to with results
DEFAULT_OUTPUT_FILE = './output.tsv'

# Default website URLs if none are specified
DEFAULT_WEBSITE_URLS = [
    'https://store.nike.com/us/en_us/pw/mens-running-shoes/7puZ8yzZoi3',
    'https://store.nike.com/us/en_us/pw/mens-tracksuits/7puZs9h',
    'https://store.nike.com/us/en_us/pw/mens-tops-t-shirts/7puZobp',
    'https://www.jennikayne.com/category/shoes/flats'
]
