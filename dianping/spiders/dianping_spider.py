import re

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
        'http://www.dianping.com/search/keyword/2/0_%E4%B9%A6%E5%BA%97%E9%9F%B3%E5%83%8F/o11',
        # 'http://www.dianping.com/shop/97590984',
    ]
    css_manager = CSSManager()
    unpack_pattern = re.compile(r'<[d|e] class="(.+?)"></.+?>')
    value_pattern = re.compile(r'([0-9.]+)')
    value_pattern2 = re.compile(r'<d class=".+?">(.+?)</d>')

    cookies = {}

    def _update_cookies(self):
        self.cookies = {}
        # cookie_str = (
        #     'cy=2; cye=beijing; _lxsdk_cuid=16b7001ef55c8-0ebb2ba9981f82-123e6e57-fa000-16b7001ef55c8; _lxsdk=16b7001ef55c8-0ebb2ba9981f82-123e6e57-fa000-16b7001ef55c8; _hc.v=c1c1dc00-f62c-437e-0e17-994d2d1fc567.1560952304; s_ViewType=10; _lxsdk_s=16b703e9c5a-fad-6f9-7e0%7C%7C19')
        # fields = cookie_str.split(';')
        # for field in fields:
        #     splitted = field.split('=')
        #     self.cookies[splitted[0].strip()] = splitted[1].strip()

    def start_requests(self):
        self._update_cookies()

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_list, cookies=self.cookies)

    def parse(self, response):
        pass

    def parse_verify(self, response):
        image = response.xpath('//img[@id="yodaImgCode"]/@src').get()
        if image:
            self.logger.info(image)
        pass

    def parse_list(self, response):
        self._parse_css(response)

        # a = response.xpath('//title/text()')
        # b = a.get()
        if response.xpath('//title/text()').get() == '验证中心':
            yield from self.parse_verify(response)
        else:
            shops = response.xpath('//ul/li//div[@class="tit"]/a[1]/@href').getall()
            if shops:
                for shop in shops:
                    self.logger.info(shop)
                    yield scrapy.Request(shop, callback=self.parse_shop_v2, cookies=self.cookies)
                    # break

            pages = response.xpath('//div[@class="page"]/a')
            if pages:
                next_page = pages[-1]
                next_page_url = next_page.attrib['href']
                self.logger.info(next_page_url)
                # yield scrapy.Request(next_page_url, callback=self.parse_list)

    def parse_shop(self, response):
        css_unpacker = self._parse_css(response)

        item = DianpingShopItem()
        item['url'] = response.url

        name = response.xpath('//div[@id="basic-info"]/h1/text()')
        if name:
            item['name'] = name.get().strip()

        rating = response.xpath('//div[@id="basic-info"]/div[@class="brief-info"]/span[1]/@title')
        if rating:
            item['rating'] = rating.get()

        if css_unpacker:
            address = response.xpath('//span[@id="address"]')
            if address:
                item['address'] = self._unpack_element(address, css_unpacker)

            tel = response.xpath('//p[contains(@class, "tel")]')
            if tel:
                item['phone_number'] = self._unpack_element(tel, css_unpacker)

            review_count = response.xpath('//span[@id="reviewCount"]')
            if review_count:
                review_count = self._unpack_element(review_count, css_unpacker)
                match = self.value_pattern.findall(review_count)
                if match:
                    item['comments'] = int(match[0])

            avg_price = response.xpath('//span[@id="avgPriceTitle"]')
            if avg_price:
                avg_price = self._unpack_element(avg_price, css_unpacker)
                match = self.value_pattern.findall(avg_price)
                if match:
                    item['cost_avg'] = int(match[0])

            product_rating = response.xpath('//span[@id="comment_score"]/span[1]')
            if product_rating:
                product_rating = self._unpack_element(product_rating, css_unpacker)
                match = self.value_pattern.findall(product_rating)
                if match:
                    item['product_rating'] = float(match[0])

            enviroment_rating = response.xpath('//span[@id="comment_score"]/span[2]')
            if enviroment_rating:
                enviroment_rating = self._unpack_element(enviroment_rating, css_unpacker)
                match = self.value_pattern.findall(enviroment_rating)
                if match:
                    item['enviroment_rating'] = float(match[0])

            service_rating = response.xpath('//span[@id="comment_score"]/span[3]')
            if service_rating:
                service_rating = self._unpack_element(service_rating, css_unpacker)
                match = self.value_pattern.findall(service_rating)
                if match:
                    item['service_rating'] = float(match[0])

        yield item

    def parse_shop_v2(self, response):
        unpacker = self._parse_css(response)

        item = DianpingShopItem()
        item['url'] = response.url

        name = response.xpath('//div[@id="basic-info"]/h1/text()')
        if name:
            item['name'] = name.get().strip()

        # TODO: Parse the address

        rating = response.xpath('//div[@id="basic-info"]/div[@class="brief-info"]/span[1]/@title')
        if rating:
            item['rating'] = rating.get()

        tel = response.xpath('//p[contains(@class, "tel")]')
        if tel:
            item['phone_number'] = self._unpack_font_element(tel, unpacker)

        review_count = response.xpath('//span[@id="reviewCount"]')
        if review_count:
            review_count = self._unpack_font_element(review_count, unpacker)
            match = self.value_pattern.findall(review_count)
            if match:
                item['comments'] = int(match[0])

        avg_price_title = response.xpath('//span[@id="avgPriceTitle"]')
        if avg_price_title:
            avg_price_title = self._unpack_font_element(avg_price_title, unpacker)
            match = self.value_pattern.findall(avg_price_title)
            if match:
                item['cost_avg'] = int(match[0])

        rating1 = response.xpath('//span[@id="comment_score"]/span[1]')
        if rating1:
            rating1 = self._unpack_font_element(rating1, unpacker)
            match = self.value_pattern.findall(rating1)
            if match:
                item['product_rating'] = float(match[0])

        rating2 = response.xpath('//span[@id="comment_score"]/span[2]')
        if rating2:
            rating2 = self._unpack_font_element(rating2, unpacker)
            match = self.value_pattern.findall(rating2)
            if match:
                item['enviroment_rating'] = float(match[0])

        rating3 = response.xpath('//span[@id="comment_score"]/span[1]')
        if rating3:
            rating3 = self._unpack_font_element(rating3, unpacker)
            match = self.value_pattern.findall(rating3)
            if match:
                item['service_rating'] = float(match[0])

        yield item

    def _parse_css(self, response):
        css = response.xpath('//link/@href')
        if css:
            for item in css.getall():
                if item.startswith('//s3plus.meituan.net/'):
                    return self.css_manager.get_css_unpacker(item)
        return None

    def _unpack_element(self, element, css_unpacker) -> str:
        elements = element.xpath('d | e | text()')
        data = []
        if elements:
            elements = elements.getall()

            for element in elements:
                ret = self.unpack_pattern.match(element)
                if ret:
                    val = css_unpacker.unpack(ret.group(1))
                    data.append(val)
                else:
                    data.append(element.strip())

        return ''.join(data)

    def _unpack_font_element(self, element, css_unpacker) -> str:
        element = element.xpath('d | e | text()')
        if element:
            element = element.getall()
            result = []
            for i in element:
                ret = self.value_pattern2.match(i)
                if ret:
                    key = ret.group(1)
                    result.append(css_unpacker.unpack_font_str(key))
                else:
                    result.append(i.strip())
            return ''.join(result)

        self.logger.info(f'Failed to unpack for {element}')
        return ''
