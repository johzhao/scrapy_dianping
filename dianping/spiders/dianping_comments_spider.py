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

        next_page = response.xpath('//div[@class="reviews-pages"]/a[last()]')
        if next_page:
            if next_page[0].attrib['title'] == '下一页':
                next_page = next_page[0].attrib['href']
                url = response.urljoin(next_page)
                # yield scrapy.Request(url, callback=self.parse)

    def _update_cookies(self):
        self.cookies = {}
        cookie_str = ('s_ViewType=10; _lxsdk_cuid=16b847dae579d-09ca42943d3ef7-37667e02-fa000-16b847dae58c8; _lxsdk=16b847dae579d-09ca42943d3ef7-37667e02-fa000-16b847dae58c8; _hc.v=9be0b285-49ac-0f18-6bf4-3a7df746cfc3.1561295958; dper=1896dc3a5ddd04644d1b3e24af7f604b6ff4d79f2d558663b3cad7449376a2d4c90de45fa583fd95acd93a4ea465f4a580623a936115c58680cf2ba0196ecf4a344827412dc73851babfb4d2dbcd2ab6a41513040573074651abdcca0b7bad8b; ll=7fd06e815b796be3df069dec7836c3df; ua=%E8%B5%B5%E9%B9%8F_7770; ctu=81691623eb4c224070e34f8f70cc7f5daac2cab2f305e2ec95e2f4c071d425dd; cy=10; cye=tianjin; _lxsdk_s=16b84d43a29-e9c-a79-d38%7C%7C369')
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
