# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PyconItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    hour = scrapy.Field()
    type = scrapy.Field()
    level = scrapy.Field()
    lang = scrapy.Field()
    room = scrapy.Field()
    speakers = scrapy.Field()
