import logging
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SVGItdUnpacker:

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

    def _content_updated(self, content: str):
        pattern = re.compile(r'font-size:(\d+?)px', re.MULTILINE)
        match = pattern.findall(content)
        if match:
            self.font_size = int(match[0])
            logger.info(f'{self.type_} svg unpacker got font size {self.font_size}')
        else:
            msg = f'Failed to find font size for {self.type_} svg.'
            raise ValueError(msg)

        pattern = re.compile(r'\s*?<text x=".*?" y="(\d+?)">(\d+?)</text>', re.MULTILINE)
        match = pattern.findall(content)
        if match:
            for item in match:
                self.path.append({
                    'value': int(item[0]),
                    'text': item[1]
                })
        else:
            msg = f'Failed to find text for {self.type_} svg.'
            raise ValueError(msg)
