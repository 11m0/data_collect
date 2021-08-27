from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
db_news = db.db_news

url = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
items = dom.xpath("//div[@class='span4']/div[@class='item']/a")

news_list = []

for item in items:
    item_info = {}
    source = 'lenta.ru'
    name = item.xpath("./text()")[0].replace('\xa0', ' ')
    date = item.xpath("./time/@datetime")[0]
    link = item.xpath("./@href")[0]
    if not link.startswith('https'):
        link = url + link

    item_info['source'] = source
    item_info['name'] = name
    item_info['link'] = link
    item_info['date'] = date

    news_list.append(item_info)

db_news.insert_many(news_list)

for item in db_news.find({}):
    pprint(item)
