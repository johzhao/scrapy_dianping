import logging

from dianping.css_unpack.css_manager import CSSManager
from dianping.css_unpack.css_unpacker import CSSUnpacker

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def test_css_manager():
    m = CSSManager()
    url = '//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/47637d8eb34f013f3b3c2c997246a587.css'
    p = m.get_css_unpacker(url)
    assert p is not None


def test_css_unpacker():
    manager = CSSManager()
    with open('./examples/output_01.css', 'r') as css_file:
        data = css_file.read()
    unpacker = CSSUnpacker(manager)
    unpacker.set_content(data)

    assert unpacker.unpack('itdhx9') == '4'
    assert unpacker.unpack('itdxjr') == '2'
    assert unpacker.unpack('itdg4j') == '8'
    assert unpacker.unpack('itdkqf') == '5'
    assert unpacker.unpack('itdzh8') == '7'
    assert unpacker.unpack('itdk1g') == '9'
    assert unpacker.unpack('abiak2') == '三'
    assert unpacker.unpack('abico0') == '路'
    assert unpacker.unpack('itdq71') == '3'
    assert unpacker.unpack('abintv') == '号'
    assert unpacker.unpack('abi3oc') == '大'
    assert unpacker.unpack('abikho') == '厦'
    assert unpacker.unpack('abisdz') == '层'
