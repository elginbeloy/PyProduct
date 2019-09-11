import os
import time
import tldextract
import core.config as config
import core.bot_scripts as bot_scripts
import selenium

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Load dotenv variables
from dotenv import load_dotenv
load_dotenv()

# signup info
email_for_signup = 'elginbeloy123@gmail.com'

# shipping info
shipping_email = os.getenv("shipping_email")
shipping_first_name = os.getenv('shipping_first_name')
shipping_last_name = os.getenv('shipping_last_name')
shipping_address = os.getenv('shipping_address')
shipping_address_two = os.getenv('shipping_address_two')
shipping_city = os.getenv('shipping_city')
shipping_state = os.getenv('shipping_state')
shipping_zipcode = os.getenv('shipping_zipcode')
shipping_phone = os.getenv('shipping_phone')

# billing info
billing_first_name = os.getenv('billing_first_name')
billing_last_name = os.getenv('billing_last_name')
billing_address = os.getenv('billing_address')
billing_city = os.getenv('billing_city')
billing_state = os.getenv('billing_state')
billing_zipcode = os.getenv('billing_zipcode')
billing_phone = os.getenv('billing_phone')

# card info
card_num = os.getenv('card_num')
card_name = os.getenv('card_name')
card_expiry = os.getenv('card_expiry')
card_verification = os.getenv('card_verification')


print(f"{config.SPIDER_INDICATOR} Starting OMSBot (ElgBot)...")

# Ex. https://www.adidas.com/us/stealth-spider-man-%7C-d.o.n.-issue-1-shoes/EF2805.html
product_url = input('Product names: ')

# Start selenium session with Chrome driver
chrome_options = webdriver.ChromeOptions()
# Comment this out to watch the bots go :D
# chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)

print(f'{config.SPIDER_INDICATOR} Getting {product_url}')
driver.get(product_url)
time.sleep(8)

add_to_bag_button = driver.find_element_by_xpath(
    '//button[contains(@class, "btn-bag")]')
add_to_bag_button.click()

time.sleep(4)

size_button = driver.find_element_by_xpath(
    '//button[@title="10.5"]')
size_button.click()

time.sleep(4)

checkout_button = driver.find_element_by_xpath(
    '//button/span[text()="Checkout"]')
checkout_button.click()

time.sleep(4)

fname_input = driver.find_element_by_name('firstName')
fname_input.send_keys(shipping_first_name)

time.sleep(1)

lname_input = driver.find_element_by_name('lastName')
lname_input.send_keys(shipping_last_name)

time.sleep(1)

address_input = driver.find_element_by_name('address1')
address_input.send_keys(shipping_address)

time.sleep(1)

additionaladdy = driver.find_element_by_xpath(
    '//a[text()="Add additional address info"]')
additionaladdy.click()

time.sleep(1)

address_input_two = driver.find_element_by_name('address2')
address_input_two.send_keys(shipping_address_two)

time.sleep(1)

city_input = driver.find_element_by_name('city')
city_input.send_keys(shipping_city)

time.sleep(1)

zip_input = driver.find_element_by_name('zipcode')
zip_input.send_keys(shipping_zipcode)

time.sleep(1)

select = Select(driver.find_element_by_name('stateCode'))
select.select_by_visible_text('California')

time.sleep(1)

email_input = driver.find_element_by_name('emailAddress')
email_input.send_keys(shipping_email)

time.sleep(1)

phone_input = driver.find_element_by_name('phoneNumber')
phone_input.send_keys(shipping_phone)

time.sleep(1)

sameBillingAddress = driver.find_element_by_name('sameBillingAddress')
sameBillingAddress.click()

time.sleep(3)

#### Billing Info ####

fname_input = driver.find_elements_by_name('firstName')[1]
fname_input.send_keys(billing_first_name)

time.sleep(1)

lname_input = driver.find_elements_by_name('lastName')[1]
lname_input.send_keys(billing_last_name)

time.sleep(1)

address_input = driver.find_elements_by_name('address1')[1]
address_input.send_keys(billing_address)

time.sleep(1)

city_input = driver.find_elements_by_name('city')[1]
city_input.send_keys(billing_city)

time.sleep(1)

zip_input = driver.find_elements_by_name('zipcode')[1]
zip_input.send_keys(billing_zipcode)

time.sleep(1)

select = Select(driver.find_elements_by_name('stateCode')[1])
select.select_by_visible_text(billing_state)

time.sleep(1)

phone_input = driver.find_elements_by_name('phoneNumber')[1]
phone_input.send_keys(billing_phone)

time.sleep(3)

######################


checkout_button = driver.find_element_by_xpath(
    '//button/span[text()="Review and Pay"]')
checkout_button.click()

time.sleep(16)

# Switch in and out of checkout iframe

driver.switch_to.frame(driver.find_element_by_name('card.number'))
time.sleep(2)

card_num_input = driver.find_element_by_xpath(
    '//input[@name="card.number"]')
card_num_input.send_keys(card_num)

driver.switch_to.default_content()
time.sleep(2)
driver.switch_to.frame(driver.find_element_by_name('card.cvv'))
time.sleep(2)

card_cvv_input = driver.find_element_by_xpath(
    '//input[@name="card.cvv"]')
card_cvv_input.send_keys(card_verification)

driver.switch_to.default_content()
time.sleep(6)

expiry_input = driver.find_element_by_css_selector(
    '.wpwl-control-expiry')
expiry_input.send_keys(card_expiry)

time.sleep(1)

card_name_input = driver.find_element_by_name('card.holder')
card_name_input.clear()
time.sleep(2)
card_name_input.send_keys(card_name)

time.sleep(1)

checkout_button = driver.find_element_by_xpath(
    '//button/span[text()="Place Order"]')
checkout_button.click()

time.sleep(24)

frame = driver.find_element_by_xpath(
    '//div[contains(@class, "wpwl-container-card")]/iframe')
driver.switch_to.frame(frame)
time.sleep(2)

driver.switch_to.frame(driver.find_element_by_id('authWindow'))
time.sleep(2)

continue_button = driver.find_element_by_id('ContinueButton')
continue_button.click()

code = input('code: ')
code_input = driver.find_element_by_id('Credential_Value')
code_input.send_keys(code)

validate_button = driver.find_element_by_id('ValidateButton')
validate_button.click()

print(f'{config.SPIDER_INDICATOR} Using discount codes!')
print(f'{config.SPIDER_INDICATOR} Complete.')

