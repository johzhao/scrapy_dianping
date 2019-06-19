import logging

import requests

from dianping.css_unpack.css_unpacker import CSSUnpacker
from dianping.svg_unpacker.svg_abi_unpacker import SVGAbiUnpacker
from dianping.svg_unpacker.svg_itd_unpacker import SVGItdUnpacker
from dianping.svg_unpacker.svg_lkr_unpacker import SVGLkrUnpacker


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CSSManager:

    def __init__(self):
        self.unpackers = {}
        self.svgs = {}

    def get_css_unpacker(self, url) -> CSSUnpacker:
        if url not in self.unpackers:
            css_url = f'http:{url}'
            response = requests.get(css_url)

            unpacker = CSSUnpacker(self)
            unpacker.set_content(response.content.decode('utf-8'))

            self.unpackers[url] = unpacker

        return self.unpackers[url]

    def get_svg(self, type_: str, url: str):
        if url not in self.svgs:
            svg_url = f'http:{url}'
            response = requests.get(svg_url)
            content = response.content.decode('utf-8')
            unpacker = self.get_unpacker(type_)
            if unpacker:
                svg_unpacker = unpacker(type_, content)
                self.svgs[url] = svg_unpacker

        return self.svgs.get(url, None)

    @staticmethod
    def get_unpacker(type_: str):
        if type_ == 'abi':
            return SVGAbiUnpacker
        elif type_ == 'itd':
            return SVGItdUnpacker
        elif type_ == 'lkr':
            return SVGLkrUnpacker
        else:
            msg = f'Unsupported svg type: {type_}.'
            logger.error(msg)
            # raise ValueError(msg)
            return None
