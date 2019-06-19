import scrapy

from dianping.css_unpack.css_manager import CSSManager
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
    css_manager = CSSManager()

    def start_requests(self):
        cookie_str = ('_lxsdk_s=16b6e52e057-7fc-bbe-8cd%7C%7C31; s_ViewType=10; _lxsdk_cuid=16b6e52ec459-094519'
                      '5ac099aa-71236752-1fa400-16b6e52ec46c8; _lxsdk=16b6e52ec459-0945195ac099aa-71236752-1fa40'
                      '0-16b6e52ec46c8; _hc.v=b74b93cf-c729-722d-dfc8-6854101a70f9.1560924057')
        cookies = {}
        fields = cookie_str.split(';')
        for field in fields:
            splitted = field.split('=')
            cookies[splitted[0].strip()] = splitted[1].strip()

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_list, cookies=cookies)

    def parse(self, response):
        pass

    def parse_verify(self, response):
        image = response.xpath('//img[@id="yodaImgCode"]/@src').get()
        if image:
            self.logger.info(image)
        pass

    def parse_list(self, response):
        self._parse_css(response)

        a = response.xpath('//title/text()')
        b = a.get()
        if response.xpath('//title/text()').get() == '验证中心':
            yield from self.parse_verify(response)
        else:
            shops = response.xpath('//ul/li//div[@class="tit"]/a[1]/@href').getall()
            if shops:
                for shop in shops:
                    self.logger.info(shop)
                    yield scrapy.Request(shop, callback=self.parse_shop)
                    break

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

    def _parse_css(self, response):
        css = response.xpath('//link/@href')
        if css:
            for item in css.getall():
                if item.startswith('//s3plus.meituan.net/'):
                    self.css_manager.get_css_unpacker(item)
                    break
