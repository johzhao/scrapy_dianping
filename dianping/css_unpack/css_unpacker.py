import logging
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CSSUnpacker:

    def __init__(self, manager):
        self.manager = manager
        self.content = ''
        self.svg_pattern = re.compile(r'\[class\^="(.*?)"\]{.*?background-image: url(.*?);')
        self.svgs = {}

    def set_content(self, content: str):
        self.content = content
        matchs = self.svg_pattern.findall(content)
        for item in matchs:
            key = item[0]
            svg_url = item[1][1:-1]
            logger.debug('Parsed svg with key {}, url: {}'.format(key, svg_url))
            svg = self.manager.get_svg(key, svg_url)
            if svg:
                self.svgs[key] = svg

    def unpack(self, key: str) -> str:
        x, y = self._get_pixel(key)
        if x < 0 or y < 0:
            return ''

        for svg_type, svg in self.svgs.items():
            if key.find(svg_type) == 0:
                return svg.get_data(x, y)
        else:
            msg = f'Failed to find value for {key} in css unpacker.'
            logger.error(msg)
            raise ValueError(msg)
            # return ''

    def _get_pixel(self, key: str) -> (int, int):
        pattern = re.compile('{}{{background:(.*?)px (.*?)px;}}'.format(key))
        matchs = pattern.findall(self.content)
        if matchs:
            result = matchs[0]
            x = -int(float(result[0]))
            y = -int(float(result[1]))
            logger.debug('Key {} found pixel {}, {}'.format(key, x, y))
            return x, y
        msg = f'Failed to find pixel for {key} in css unpacker'
        raise ValueError(msg)
        # return -1, -1
