import os
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
    unpack_pattern = re.compile(r'<svgmtsi class="(.+?)"></.+?>')
    value_pattern = re.compile(r'([0-9.]+)')
    value_pattern2 = re.compile(r'<[d|e] class=".+?">(.+?)</.+?>')

    cookies = {}

    def _update_cookies(self):
        self.cookies = {}

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
        unpacker = self._parse_css(response)

        has_shop_request = False
        shops = response.xpath('//div[@class="content"]//div[contains(@class, "shop-list")]/ul/li')
        for shop in shops:
            comments = shop.xpath('div//span[@class="sear-highlight"]')
            if comments:
                comments = self._unpack_element(comments, unpacker)
                comments = int(comments)
                # 只爬取用户评论数大于100的店铺
                if comments > 100:
                    has_shop_request = True
                    shop_url = shop.xpath('div/div[@class="tit"]/a[1]/@href')
                    if shop_url:
                        yield scrapy.Request(shop_url.get(), callback=self.parse_shop_v2, cookies=self.cookies)
            # break

        if has_shop_request:
            pages = response.xpath('//div[@class="page"]/a')
            if pages:
                next_page = pages[-1]
                next_page_url = next_page.attrib['href']
                self.logger.info(next_page_url)
                yield scrapy.Request(next_page_url, callback=self.parse_list)

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
        item['_id'] = os.path.basename(response.url)
        item['url'] = response.url

        name = response.xpath('//div[@id="basic-info"]/h1/text()')
        if name:
            item['name'] = name.get().strip()

        address = response.xpath('//div[@id="basic-info"]/div[contains(@class, "address")]/span[2]')
        if address:
            item['address'] = self._unpack_font_element(address, unpacker)

        rating = response.xpath('//div[@id="basic-info"]/div[@class="brief-info"]/span[1]/@title')
        if rating:
            item['rating'] = rating.get()

        tel = response.xpath('//p[contains(@class, "tel")]')
        if tel:
            tel = self._unpack_font_element(tel, unpacker)
            item['phone_number'] = tel.split(';')

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
        elements = element.xpath('b/svgmtsi | b/text()')
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
                    for c in i:
                        if c == ' ':
                            pass
                        elif ord(c) == 160:
                            result.append(';')
                        else:
                            result.append(c)
            return ''.join(result)

        self.logger.info(f'Failed to unpack for {element}')
        return ''
