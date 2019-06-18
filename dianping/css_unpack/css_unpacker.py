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

    def set_content(self, content):
        self.content = content
        matchs = self.svg_pattern.findall(content)
        for item in matchs:
            key = item[0]
            svg_url = item[1][1:-1]
            logger.debug('Parsed svg with key {}, url: {}'.format(key, svg_url))
            # svg = self.manager.get_svg(svg_url)
            # self.svgs[key] = svg

    def unpack(self, key: str) -> str:
        pass

    def _get_pixel(self, key: str) -> (int, int):
        pattern = re.compile('{}{{background:(.*?)px (.*?)px;}}'.format(key))
        matchs = pattern.findall(self.content)
        if matchs:
            result = matchs[0]
            x = -int(float(result[0]))
            y = -int(float(result[1]))
            logger.debug('Key {} found pixel {}, {}'.format(key, x, y))
            return x, y


def test():
    logging.basicConfig(level=logging.DEBUG)
    from dianping.css_unpack.css_manager import CSSManager
    manager = CSSManager()
    with open('./output.css', 'r') as css_file:
        data = css_file.read()
    unpacker = CSSUnpacker(manager)
    unpacker.set_content(data)

    x, y = unpacker._get_pixel('.itdf8d')
    logger.debug('Found pixel {}, {}'.format(x, y))

    pass


if __name__ == '__main__':
    test()
