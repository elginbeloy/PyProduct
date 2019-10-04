<p align="center"><img src="assets/logo.svg" width="400" title="PyProduct Logo"></p>

<p align="center">
    <a href="https://github.com/elginbeloy/PyProduct/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/elginbeloy/PyProduct">
    </a>
</p>


PyProduct is a Python + Selenium + BeautifulSoup based web catalog scraper, programmatic OMS, and all-around e-commerce interaction bot solution.

# What is PyProduct

In short, PyProduct aims to be the one-stop shop for e-commerce interaction, from catalog scraping, to programmatic OMS and inventory tracking. PyProduct is built with Python, Selenium, and BeautifulSoup. PyProduct allows for quick and efficient data capture from online e-commerce catalogs like Nike, Adidas, and others using headless browser bot interactions.

The goals of PyProduct are as follows:
- Integration free, clone-and-go setup
- Efficient and reliable online e-commerce catalog data capture
- Secure and fast oms order placement
- Reliable inventory and shipping option tracking

# Getting Started

To get started with PyProduct, simply clone, install dependencies, get a driver, and go:

1. Clone the repo and cd into the directory

```
git clone https://github.com/elginbeloy/PyProduct
cd PyProduct
```

2. Install requirements.txt into a virtual environment of your choice

```
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

3. Download a chrome driver [here](https://chromedriver.chromium.org/downloads), and place it in the PyProduct directory as `chromedriver`. *NOTE:* Ensure you download the correct driver for your version of Chrome. 

4. Run PyProduct with help to see options 

```
python pyproduct.py --help
```

> NOTE: Programmatic OMS functionality will not work without a .env in root that contains the necessary purchase environment variables.

# How PyProduct Works

PyProduct has three main components
1. Scraping products from e-commerce websites (using `Spider`)
2. Tracking product availability (in progress) 
3. Purchasing products automatically (using `OMBot`)

The functionality of each of these parts of PyProduct (both developed and WIP) is outlined below:

> NOTE: Some websites (namely adidas) have a policy against bots and implement IP blocking which limits the amount of requests that can be made from a single IP before being blacklisted for a time frame. This can bypassed with any sort of bypass routing like VPN or Onion-routing - however this slows down scrapping significantly. 

## Spider (Scrapping)

The scraping part of PyProduct is done with a spider that crawls catalog URLs from a base domain URL (E.g https://shop.nike.com). The spider avoids scraping specific product URLs (looking only for catalogs, not specific products) using a regex check of the URL. This is to save the scraper the time cost of scraping a single product page - focusing only on catalog URLs.

These scrapped URLs are then passed to a bot that scrolls the page (using a smooth scroll JS for lazy loaded SPAs) then finds each product by container xpaths. Each attribute of the product is then found within this container using xpaths that are cached. For an example of this see `cached_xpaths.json`.

Automatic XPath generation using NNs is a WIP - but will be vitally helpful for auto adding websites (without having to manually add and verify xpaths) and fail-safe checking. 

Fail-safe checks are also a WIP. 

## OMBot (OMS Interaction)

OMBot aims to encapsulate the OMS checkout process into a single bot that can go through checkout on a variety of sites using cached xpaths (similar to the spider). Again, auto xpath generation is vital here but still a WIP.

# Core ToDo's

- [ ] Add x-out of popup to xpaths in case of popup 
- [ ] Don't do scrolling or anything if product containers are not found
- [ ] Make deep option for scraping URLs past initial page

- [ ] Add MSRP to scraped data
- [ ] Support multiple images in scraped data
- [ ] Add size and color availability to scraped data
- [ ] Add shipping options to scraped data

- [ ] Standardize and expand programmatic OMS

- [ ] Add testing, code coverage, and badges for each to README.md

- [ ] Add automatic cached xpath and url generation
- [ ] Make cached xpath test to ensure UI not updated (if so regenerate or alert)
- [ ] Make NN based xpath generation using NLP or CNN
- [ ] Create system for scraping products on an interval and saving to PostgreSQL

# Contributing

Don't for now 🤷 Gotta get it to a good starting place first.
