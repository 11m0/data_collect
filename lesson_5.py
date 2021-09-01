from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['products']
db_products = db.db_products

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')
time.sleep(2)

news_block = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..")
actions = ActionChains(driver)
actions.move_to_element(news_block).perform()
next_button = news_block.find_element_by_xpath(".//a[contains(@class, 'next-btn')]")

while next_button.get_attribute('class') ==\
        'next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right':
    next_button.click()
    time.sleep(1)

products = news_block.find_elements_by_xpath(".//li[contains(@class, 'gallery-list-item')]")
products_list = []
for product in products:
    product_info = {}

    product_name = product.find_element_by_xpath(".//a[contains(@class, 'fl-product-tile-title')]")
    product_price = product.find_element_by_xpath(".//span[contains(@class, 'fl-product-tile-price')]")

    product_info['name'] = ' '.join(product_name.get_attribute('text').replace('\n', '').split())
    product_info['price'] = product_price.text

    products_list.append(product_info)

db_products.insert_many(products_list)
for item in db_products.find({}):
    pprint(item)
