import datetime
import time
import re

import scrapy
import scrapy.exceptions

from dianping.css_unpack.css_manager import CSSManager
from dianping.items import DianpingReviewItem


class DianpingCommentsSpider(scrapy.Spider):

    name = 'dianping_comments_spider'

    allowed_domains = [
        'www.dianping.com',
        'verify.meituan.com',
    ]

    start_urls = [
    ]
    css_manager = CSSManager()
    shop_id_pattern = re.compile(r'https://www\.dianping\.com/shop/(.+?)/review_all.*')
    unpack_pattern = re.compile(r'<svgmtsi class="(.+?)"></.+?>')
    review_date_limit = datetime.datetime(2019, 1, 1, 0)

    def start_requests(self):
        self._update_cookies()

        with open('./shop_ids.txt', 'r') as shop_id_file:
            for line in shop_id_file:
                if line.startswith('#'):
                    continue
                shop_id = line.strip()
                url = f'https://www.dianping.com/shop/{shop_id}/review_all?queryType=sortType&&queryVal=latest'
                yield scrapy.Request(url, callback=self.parse, cookies=self.cookies)
                break

    def parse(self, response):
        unpacker = self._parse_css(response)

        shop_name = response.xpath('//div[@class="review-shop-wrap"]//h1/text()')
        if not shop_name:
            self.logger.error(f'Failed to find shop name for url {response.url}')
            return
        shop_name = shop_name.get()

        shop_id = self.shop_id_pattern.match(response.url)
        if shop_id:
            shop_id = shop_id.group(1)
        else:
            msg = f'Failed to find shop id from url {response.url}'
            self.logger.error(msg)
            raise scrapy.exceptions.CloseSpider(msg)

        no_review = True

        reviews = response.xpath('//div[@class="reviews-items"]/ul/li')
        for review in reviews:
            timestamp = review.xpath('div[@class="main-review"]/div[contains(@class, "misc-info")]/span[1]/text()')
            if timestamp:
                timestamp = timestamp.get().strip()
                if timestamp.find('更新于') > 0:
                    timestamp = timestamp.split('更新于')[-1].strip()
                timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
                if timestamp < self.review_date_limit:
                    continue

            no_review = False
            item = DianpingReviewItem()
            item['shop_id'] = shop_id
            item['timestamp'] = time.mktime(timestamp.timetuple())

            username = review.xpath('div[@class="main-review"]/div[@class="dper-info"]/a[@class="name"]/text()')
            if username:
                item['username'] = username.get().strip()

            item['shop_name'] = shop_name

            rating = review.xpath('div[@class="main-review"]/div[@class="review-rank"]/span[1]/@class')
            if rating:
                rating = rating.get().split(' ')[1]
                item['rating'] = rating

            review_words = review.xpath('div[@class="main-review"]/div[@class="review-words"]')
            if not review_words:
                review_words = review.xpath('div[@class="main-review"]/div[@class="review-truncated-words"]')

            if review_words:
                review_words = self._unpack_element(review_words, unpacker)
                item['review'] = review_words

            yield item

        if not no_review:
            next_page = response.xpath('//div[@class="reviews-pages"]/a[last()]')
            if next_page:
                if next_page[0].attrib['title'] == '下一页':
                    next_page = next_page[0].attrib['href']
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, callback=self.parse)

    def _update_cookies(self):
        self.cookies = {}
        cookie_str = ('cy=10; cye=tianjin; _lxsdk_cuid=16b84f7a539c8-0aa964cb16d935-37667e02-fa000-16b84f7a539c8; _lxsdk=16b84f7a539c8-0aa964cb16d935-37667e02-fa000-16b84f7a539c8; _hc.v=f59f3fee-88a6-f6c8-887e-c77578b98579.1561303951; dper=1896dc3a5ddd04644d1b3e24af7f604b1e94ac056f5c4cb5e36262ad2fbc7df4cbb6735ce31b585992da30d8a0027c6adb5bc5b0040e385aa40f88702b687c5c1bfa2e61ebee39baf6f1b4e07054c5a9eae6d108c8c5822cbe7059c1df1be9a3; ll=7fd06e815b796be3df069dec7836c3df; ua=%E8%B5%B5%E9%B9%8F_7770; ctu=81691623eb4c224070e34f8f70cc7f5d809caa692589e51158f593821d5ebabf; _lxsdk_s=16b84f7a350-bf0-60a-c15%7C%7C372')
        fields = cookie_str.split(';')
        for field in fields:
            splitted = field.split('=')
            self.cookies[splitted[0].strip()] = splitted[1].strip()

    def _parse_css(self, response):
        css = response.xpath('//link/@href')
        if css:
            for item in css.getall():
                if item.startswith('//s3plus.meituan.net/'):
                    return self.css_manager.get_css_unpacker(item)
        return None

    def _unpack_element(self, element, css_unpacker) -> str:
        elements = element.xpath('svgmtsi | text()')
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
