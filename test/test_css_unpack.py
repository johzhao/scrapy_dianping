import logging

from dianping.css_unpack.css_manager import CSSManager
from dianping.css_unpack.css_unpacker import CSSUnpacker

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_css_manager():
    # m = CSSManager()
    # url = '//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/47637d8eb34f013f3b3c2c997246a587.css'
    # p = m.get_css_unpacker(url)
    pass


def test_css_unpacker():
    # manager = CSSManager()
    # with open('./examples/output_01.css', 'r') as css_file:
    #     data = css_file.read()
    # unpacker = CSSUnpacker(manager)
    # unpacker.set_content(data)
    #
    # x, y = unpacker._get_pixel('.itdf8d')
    # logger.debug('Found pixel {}, {}'.format(x, y))
    pass
