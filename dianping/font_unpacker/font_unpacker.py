import logging
import json
from fontTools.ttLib import TTFont

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class FontUnpacker:

    def __init__(self, base_font: TTFont, base_font_mapping: dict, content):
        self.mapping = {}
        self._create_font_mapping(base_font, base_font_mapping, content)
        pass

    def unpack(self, data: str) -> str:
        return self.mapping.get(data, ' ')

    def _create_font_mapping(self, base_font: TTFont, base_font_mapping: dict, content):
        font_file_path = './temp.woff'
        with open(font_file_path, 'wb') as font_file:
            font_file.write(content)

        self.mapping = {}

        online_font = TTFont(font_file_path)
        uni_list = online_font.getGlyphNames()
        online_data_count = len(uni_list)

        base_font_keys = list(base_font_mapping.keys())
        base_data_count = len(base_font_keys)

        for i in range(online_data_count):
            online_glyph = online_font['glyf'][uni_list[i]]
            for j in range(base_data_count):
                base_glyph = base_font['glyf'][base_font_keys[j]]
                if online_glyph == base_glyph:
                    if uni_list[i] in base_font_mapping:
                        key = f'"\\u{uni_list[i][3:]}"'
                        key = json.loads(key)
                        self.mapping[key] = base_font_mapping[base_font_keys[j]]
