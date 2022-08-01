# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TbfetcherItem(scrapy.Item):
    file_urls = scrapy.Field()
    desc = scrapy.Field()
    title = scrapy.Field()

