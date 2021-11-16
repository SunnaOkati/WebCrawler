# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AldicrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    Product_title = scrapy.Field()
    Product_image = scrapy.Field()
    PackSize = scrapy.Field()
    Price = scrapy.Field()
    Price_per_unit = scrapy.Field()

