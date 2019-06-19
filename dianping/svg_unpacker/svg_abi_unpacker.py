import logging
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SVGAbiUnpacker:

    def __init__(self, type_: str, content: str):
        self.type_ = type_
        self.font_size = -1
        self.path = []
        self._content_updated(content)

    def get_data(self, x: int, y: int) -> str:
        for item in self.path:
            if item['value'] >= y:
                offset = x // self.font_size
                return item['text'][offset]

        msg = f'Failed to find text at x: {x}, y: {y}'
        raise ValueError(msg)

    def _content_updated(self, content):
        pattern = re.compile(r'font-size:(\d+?)px', re.MULTILINE)
        match = pattern.findall(content)
        if match:
            self.font_size = int(match[0])
            logger.info(f'{self.type_} svg unpacker got font size {self.font_size}')
        else:
            msg = f'Failed to find font size for {self.type_} svg.'
            raise ValueError(msg)

        data1 = []

        pattern = re.compile(r'<path id="(\d+?)" d="M\d+? (\d+?) H\d+?"/>')
        match = pattern.findall(content)
        if match:
            for item in match:
                data1.append({
                    'id': int(item[0]),
                    'range': int(item[1]),
                })
        else:
            msg = f'Failed to find path for {self.type_} svg.'
            raise ValueError(msg)

        data2 = []

        pattern = re.compile(r'<textPath xlink:href="#(\d+?)" textLength="(\d+?)">(.+?)</textPath>')
        match = pattern.findall(content)
        if match:
            for item in match:
                data2.append({
                    'id': int(item[0]),
                    'range': int(item[1]),
                    'text': item[2]
                })
        else:
            msg = f'Failed to find text path for {self.type_} svg.'
            raise ValueError(msg)

        for item in zip(data1, data2):
            self.path.append({
                'value': item[0]['range'],
                'text': item[1]['text'],
            })
