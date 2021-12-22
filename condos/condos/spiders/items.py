# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CondosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    floorplan_bd = scrapy.Field()
    floorplan_ba = scrapy.Field()
    floorplan_pk = scrapy.Field()
    sqm = scrapy.Field()
    main_fee = scrapy.Field()
    tax = scrapy.Field()
    location = scrapy.Field()
    #exposure = scrapy.Field()
    #outdoor = scrapy.Field()
    #locker = scrapy.Field()
