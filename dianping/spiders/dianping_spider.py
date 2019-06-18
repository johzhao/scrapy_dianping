# -*- coding: utf-8 -*-
import scrapy


class DianpingSpiderSpider(scrapy.Spider):
    name = 'dianping_spider'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/']

    def parse(self, response):
        pass
