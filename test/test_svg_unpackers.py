import logging

from dianping.svg_unpacker.svg_abi_unpacker import SVGAbiUnpacker
from dianping.svg_unpacker.svg_itd_unpacker import SVGItdUnpacker
from dianping.svg_unpacker.svg_lkr_unpacker import SVGLkrUnpacker

logging.basicConfig(level=logging.DEBUG)


def test_svg_abi_unpacker():
    with open('examples/output_abi.svg', 'r') as svg_file:
        data = svg_file.read()
    abi_unpacker = SVGAbiUnpacker('abi', data)

    assert abi_unpacker.get_data(0, 0) == '莞'
    assert abi_unpacker.get_data(84, 286) == '三'
    assert abi_unpacker.get_data(126, 11) == '路'
    assert abi_unpacker.get_data(112, 247) == '号'
    assert abi_unpacker.get_data(336, 174) == '大'
    assert abi_unpacker.get_data(70, 11) == '厦'
    assert abi_unpacker.get_data(210, 52) == '层'


def test_svg_itd_unpacker():
    with open('examples/output_itd.svg', 'r') as svg_file:
        data = svg_file.read()
    itd_unpacker = SVGItdUnpacker('itd', data)

    assert itd_unpacker.get_data(0, 0) == '3'
    assert itd_unpacker.get_data(232, 126) == '4'
    assert itd_unpacker.get_data(316, 126) == '2'
    assert itd_unpacker.get_data(302, 126) == '8'
    assert itd_unpacker.get_data(148, 126) == '5'
    assert itd_unpacker.get_data(330, 126) == '7'
    assert itd_unpacker.get_data(218, 126) == '9'
    assert itd_unpacker.get_data(288, 126) == '3'


def test_svg_lkr_unpacker():
    with open('examples/output_lkr.svg', 'r') as svg_file:
        data = svg_file.read()
    lkr_unpacker = SVGLkrUnpacker('lkr', data)

    assert lkr_unpacker.get_data(182, 723) == '朋'
    assert lkr_unpacker.get_data(196, 1877) == '友'
    assert lkr_unpacker.get_data(490, 762) == '姐'
    assert lkr_unpacker.get_data(308, 1259) == '开'
    assert lkr_unpacker.get_data(350, 1709) == '业'
    assert lkr_unpacker.get_data(210, 565) == '就'
    assert lkr_unpacker.get_data(14, 52) == '了'
    assert lkr_unpacker.get_data(224, 1970) == '五'
    assert lkr_unpacker.get_data(224, 1709) == '楼'
    assert lkr_unpacker.get_data(210, 565) == '就'
    assert lkr_unpacker.get_data(140, 1590) == '八'
    assert lkr_unpacker.get_data(0, 1631) == '果'
