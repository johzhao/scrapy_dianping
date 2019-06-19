from scrapy.http.response.html import HtmlResponse

from dianping.css_unpack.css_manager import CSSManager
from dianping.items import DianpingShopItem


def test_parse_shop_detail():
    with open('./examples/output_03.html', 'rb') as html_file:
        body = html_file.read()
    url = 'http://www.dianping.com/shop/97590984'
    response = HtmlResponse(url=url, body=body)

    item = DianpingShopItem()

    name = response.xpath('//div[@id="basic-info"]/h1/text()')
    if name:
        item['name'] = name.get()

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
        elements = address.xpath('d/@class | e/@class | text()').getall()
        results = []
        for element in elements:
            ret = css_unpacker.unpack(element)
            if ret:
                results.append(ret)
            else:
                results.append(element.strip())
        address = ''.join(results)
        item['address'] = address

    tel = response.xpath('//p[contains(@class, "tel")]')
    if tel:
        elements = tel.xpath('d/@class | e/@class | text()').getall()
        results = []
        for element in elements:
            ret = css_unpacker.unpack(element)
            if ret:
                results.append(ret)
            else:
                results.append(element.strip())
        tel = ''.join(results)
        item['phone_number'] = tel

    pass
