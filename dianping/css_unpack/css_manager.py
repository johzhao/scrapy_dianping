import json
import logging
import re

import requests
from fontTools.ttLib import TTFont

from dianping.css_unpack.css_unpacker import CSSUnpacker
from dianping.svg_unpacker.svg_abi_unpacker import SVGAbiUnpacker
from dianping.svg_unpacker.svg_itd_unpacker import SVGItdUnpacker
from dianping.svg_unpacker.svg_lkr_unpacker import SVGLkrUnpacker
from dianping.font_unpacker.font_unpacker import FontUnpacker

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CSSManager:

    def __init__(self):
        self.unpackers = {}
        self.svgs = {}
        self.fonts = {}
        self.base_font = None
        self.base_font_mapping = {}
        self._load_base_font()

        self.abi_pattern = re.compile(r'<textPath xlink:href=')
        self.itd_pattern = re.compile(r'<text x="\d+ \d+ ')
        self.lkr_pattern = re.compile(r'<text x="\d+" y="\d+">')

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
            unpacker = self.get_unpacker(content)
            if unpacker:
                svg_unpacker = unpacker(type_, content)
                self.svgs[url] = svg_unpacker

        return self.svgs.get(url, None)

    def get_font_unpacker(self, url):
        if url not in self.unpackers:
            woff_url = f'http:{url}'
            response = requests.get(woff_url)
            unpacker = FontUnpacker(self.base_font, self.base_font_mapping, response.content)
            self.unpackers[url] = unpacker

        return self.unpackers[url]

    def _load_base_font(self):
        font_file_path = './examples/basefont.woff'
        self.base_font = TTFont(font_file_path)
        font_mapping_file_path = './examples/basefont.json'
        with open(font_mapping_file_path, 'r') as mapping_file:
            self.base_font_mapping = json.load(mapping_file)

    def get_unpacker(self, content: str):
        if self.abi_pattern.findall(content):
            return SVGAbiUnpacker
        elif self.itd_pattern.findall(content):
            return SVGItdUnpacker
        elif self.lkr_pattern.findall(content):
            return SVGLkrUnpacker
        else:
            return None
