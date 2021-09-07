# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def get_price(value):
    try:
        return int(value.replace(' ', ''))
    except Exception:
        return value


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    descr_keys = scrapy.Field()
    descr_values = scrapy.Field(input_processor=MapCompose(lambda value: value .replace('\n', '') .lstrip() .rstrip()))
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(lambda value: value .replace('_82', '_1200')))
    url = scrapy.Field()
    descr = scrapy.Field()
