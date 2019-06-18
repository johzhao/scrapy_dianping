import logging

import requests

import dianping.css_unpack.css_unpacker

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CSSManager:

    def __init__(self):
        self.unpackers = {}
        self.svgs = {}

    def get_css_unpacker(self, url):
        if url not in self.unpackers:
            css_url = 'http:{}'.format(url)
            response = requests.get(css_url)

            unpacker = dianping.css_unpack.css_unpacker.CSSUnpacker(self)
            unpacker.set_content(response.content.decode('utf-8'))

            self.unpackers[url] = unpacker

        return self.unpackers[url]

    def get_svg(self, url):
        if url not in self.svgs:
            svg_url = 'http:{}'.format(url)
            response = requests.get(svg_url)
            self.svgs[url] = response.content.decode('utf-8')

        return self.svgs[url]


def test():
    m = CSSManager()
    url = '//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/47637d8eb34f013f3b3c2c997246a587.css'
    p = m.get_css_unpacker(url)


if __name__ == '__main__':
    test()
