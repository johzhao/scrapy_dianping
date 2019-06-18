# -*- coding: utf-8 -*-
import scrapy
from dianping.items import DianpingShopItem


class DianpingSpiderSpider(scrapy.Spider):
    name = 'dianping_spider'
    allowed_domains = [
        'www.dianping.com',
        'verify.meituan.com',
    ]
    start_urls = [
        'http://www.dianping.com/search/keyword/2/0_%E4%B9%A6%E5%BA%97%E9%9F%B3%E5%83%8F/o11'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_list)

    def parse(self, response):
        pass

    def parse_verify(self, response):
        image = response.xpath('//img[@id="yodaImgCode"]/@src').get()
        if image:
            self.logger.info(image)
        pass

    def parse_list(self, response):
        a = response.xpath('//title/text()')
        b = a.get()
        if response.xpath('//title/text()').get() == '验证中心':
            yield from self.parse_verify(response)
        else:
            shops = response.xpath('//ul/li//div[@class="tit"]/a[1]/@href').getall()
            if shops:
                for shop in shops:
                    self.logger.info(shop)
                    # yield scrapy.Request(shop, callback=self.parse_shop)

            pages = response.xpath('//div[@class="page"]/a')
            if pages:
                next_page = pages[-1]
                next_page_url = next_page.attrib['href']
                self.logger.info(next_page_url)
                # yield scrapy.Request(next_page_url, callback=self.parse_list)

    def parse_shop(self, response):
        item = DianpingShopItem()

        name = response.xpath('//div[@id="basic-info"]/h1/text()')
        if name:
            item['name'] = name.get()

        rating = response.xpath('//div[@id="basic-info"]/div[@class="brief-info"]/span[1]/@title')
        if rating:
            item['rating'] = rating.get()

        yield item
