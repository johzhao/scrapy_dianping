import logging

import pytest
from scrapy.http.response.html import HtmlResponse

from dianping.spiders.dianping_spider import DianpingSpiderSpider
from dianping.spiders.dianping_comments_spider import DianpingCommentsSpider

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@pytest.mark.skip
def test_parse_shop_list():
    body = _load_html_file('./examples/output_01.html')
    url = 'http://www.dianping.com/shop/97590984'
    response = HtmlResponse(url=url, body=body)

    spider = DianpingSpiderSpider()

    for item in spider.parse_list(response):
        logger.debug(item)


@pytest.mark.skip
def test_parse_shop_detail():
    body = _load_html_file('./examples/output_02.html')
    url = 'http://www.dianping.com/shop/97590984'
    response = HtmlResponse(url=url, body=body)

    spider = DianpingSpiderSpider()

    for item in spider.parse_shop(response):
        logger.debug(item)


@pytest.mark.skip
def test_parse_shop_detail_v2():
    body = _load_html_file('./examples/output_04.html')
    url = 'http://www.dianping.com/shop/97590984'
    response = HtmlResponse(url=url, body=body)

    spider = DianpingSpiderSpider()

    spider.parse_shop_v2(response)
    for item in spider.parse_shop_v2(response):
        logger.debug(item)


def test_parse_comments_01():
    body = _load_html_file('./examples/comments_01.html')
    url = 'https://www.dianping.com/shop/17983537/review_all?queryType=sortType&&queryVal=latest'
    response = HtmlResponse(url=url, body=body)

    spider = DianpingCommentsSpider()

    for review in spider.parse(response):
        logger.info(review)


def _load_html_file(filepath: str):
    with open(filepath, 'rb') as html_file:
        body = html_file.read()
    return body
