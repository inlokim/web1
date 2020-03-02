# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Web1Item(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field()
    title = scrapy.Field()
    korean_title = scrapy.Field()
    english_title = scrapy.Field()
    japanese_title = scrapy.Field()
    chinese_title = scrapy.Field()
    
    content = scrapy.Field()
    korean_content = scrapy.Field()
    english_content = scrapy.Field()
    japanese_content = scrapy.Field()
    chinese_content = scrapy.Field()
    
    url = scrapy.Field()
    category = scrapy.Field()
    date = scrapy.Field()
    img = scrapy.Field()