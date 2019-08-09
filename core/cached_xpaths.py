# Default cached xpaths

cached_xpaths = {
    'nike': {
        'container': '//div[contains(@class, "product-grid__card")]',
        'name': './/div[contains(@class, "product-card__titles")]/div[contains(@class, "product-card__title")]',
        'description': './/div[contains(@class, "product-card__subtitle")]',
        'image': './/div[contains(@class, "product-card__hero-image")]/picture/img',
        'price': './/div[contains(@class, "product-card__price")]',
    },

    'jennikayne': {
        'container': '//div[contains(@class, "product")]',
        'name': './/div[contains(@class, "product__name")]',
        'description': './/div[contains(@class, "product__color-info")]',
        'image': './/div[contains(@class, "product__image")]',
        'price': './/div[contains(@class, "product__price")]',
    },

    'adidas': {
        'container': '//div[contains(@class, "gl-product-card-container")]',
        'name': './/div[contains(@class, "gl-product-card__name")]',
        'description': './/div[contains(@class, "gl-product-card__category")]',
        'image': './/img[contains(@class, "gl-product-card__image")]',
        'price': './/div[contains(@class, "gl-price")]',
    }
}
