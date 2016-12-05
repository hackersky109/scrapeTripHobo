# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PathItem(scrapy.Item):
    title = scrapy.Field()
    total_days = scrapy.Field()
    views = scrapy.Field()
    startTime = scrapy.Field()
    endTime = scrapy.Field()
    start_city = scrapy.Field()
    transit_city = scrapy.Field()

class TriphoboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
