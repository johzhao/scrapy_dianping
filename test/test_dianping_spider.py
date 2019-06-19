import logging

from scrapy.http.response.html import HtmlResponse

from dianping.css_unpack.css_manager import CSSManager
from dianping.items import DianpingShopItem

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_parse_shop_detail():
    with open('./examples/output_03.html', 'rb') as html_file:
        body = html_file.read()
    url = 'http://www.dianping.com/shop/97590984'
    response = HtmlResponse(url=url, body=body)

    item = DianpingShopItem()

    name = response.xpath('//div[@id="basic-info"]/h1/text()')
    if name:
        item['name'] = name.get().strip()

    rating = response.xpath('//div[@id="basic-info"]/div[@class="brief-info"]/span[1]/@title')
    if rating:
        item['rating'] = rating.get()

    css_manager = CSSManager()
    css = response.xpath('//link/@href')
    css_url = ''
    if css:
        for element in css.getall():
            if element.startswith('//s3plus.meituan.net/'):
                css_url = element
                css_manager.get_css_unpacker(css_url)
                break
    css_unpacker = css_manager.get_css_unpacker(css_url)

    address = response.xpath('//span[@id="address"]')
    if address:
        item['address'] = _unpack_element(address, css_unpacker)

    tel = response.xpath('//p[contains(@class, "tel")]')
    if tel:
        item['phone_number'] = _unpack_element(tel, css_unpacker)

    review_count = response.xpath('//span[@id="reviewCount"]')
    if review_count:
        item['comments'] = _unpack_element(review_count, css_unpacker)

    avg_price = response.xpath('//span[@id="avgPriceTitle"]')
    if avg_price:
        item['cost_avg'] = _unpack_element(avg_price, css_unpacker)

    product_rating = response.xpath('//span[@id="comment_score"]/span[1]')
    if product_rating:
        item['product_rating'] = _unpack_element(product_rating, css_unpacker)

    enviroment_rating = response.xpath('//span[@id="comment_score"]/span[2]')
    if enviroment_rating:
        item['enviroment_rating'] = _unpack_element(enviroment_rating, css_unpacker)

    service_rating = response.xpath('//span[@id="comment_score"]/span[3]')
    if service_rating:
        item['service_rating'] = _unpack_element(service_rating, css_unpacker)

    logger.debug(item.values())


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
