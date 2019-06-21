import logging

import pytest
from scrapy.http.response.html import HtmlResponse

from dianping.spiders.dianping_spider import DianpingSpiderSpider

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@pytest.mark.skip
def test_parse_shop_detail():
    with open('./examples/output_02.html', 'rb') as html_file:
        body = html_file.read()
    url = 'http://www.dianping.com/shop/97590984'
    response = HtmlResponse(url=url, body=body)

    spider = DianpingSpiderSpider()

    for item in spider.parse_shop(response):
        logger.debug(item)


def test_parse_shop_detail_v2():
    with open('./examples/output_02.html', 'rb') as html_file:
        body = html_file.read()
    url = 'http://www.dianping.com/shop/97590984'
    response = HtmlResponse(url=url, body=body)

    spider = DianpingSpiderSpider()

    spider.parse_shop_v2(response)
    # for item in spider.parse_shop_v2(response):
    #     logger.debug(item)


def _unpack_element(element, css_unpacker) -> str:
    import re

    elements = element.xpath('d | e | text()')
    data = []
    if elements:
        elements = elements.getall()

        pattern = re.compile(r'<[d|e] class="(.+?)"></.+?>')
        for element in elements:
            ret = pattern.match(element)
            if ret:
                val = css_unpacker.unpack(ret.group(1))
                data.append(val)
            else:
                data.append(element.strip())

    return ''.join(data)
