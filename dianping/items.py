# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingShopItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    comments = scrapy.Field()
    cost_avg = scrapy.Field()
    product_rating = scrapy.Field()
    enviroment_rating = scrapy.Field()
    service_rating = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    url = scrapy.Field()


class DianpingReviewItem(scrapy.Item):
    shop_id = scrapy.Field()
    username = scrapy.Field()
    shop_name = scrapy.Field()
    rating = scrapy.Field()
    review = scrapy.Field()
    timestamp = scrapy.Field()
    pass
