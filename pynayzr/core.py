# -*- coding: utf-8 -*-

import json
import datetime
from PIL import Image
from pynayzr import cropper
from pynayzr import ocr
from pynayzr.ocr import get_google_credentials
from pynayzr import streams


class NewsModel:
    """News model to chop image and do OCR for images
    """

    def __init__(self, news, image_path=None, parser=ocr.parse_by_google):
        if news not in cropper.support_news:
            raise NotImplementedError

        # Force parser to tesseract if google credentials not found
        if not get_google_credentials()[0]:
            parser = ocr.parse_by_tesseract

        # Choice image source from live or image
        # NOTE: Image size must be 1280x720
        self.news = news
        if image_path:
            self.img = Image.open(image_path)
        else:
            self.img = streams.get(news)
        self.crop = cropper.support_news[news](img=self.img)
        self.parser = parser

        self.crop_title = self.crop.title()
        self.crop_subpoint = self.crop.subpoint()
        self.crop_subtitle = self.crop.subtitle()
        self.crop_bottom = self.crop.bottom()

        # Lazy parse
        self._parsed = False
        self.title = None
        self.subpoint = None
        self.subtitle = None
        self._type = 'unknown'
        self.subject = None
        self.source = None

    def _parse(self):
        self._parsed = True
        self.title = self.parser(self.crop_title)
        self.subpoint = self.parser(self.crop_subpoint)
        self.subtitle = self.parser(self.crop_subtitle) if self.crop_subtitle else ""

    @property
    def type(self):
        if self.title and self.subtitle:
            self._type = 'news'
        if not self.title and (not self.subtitle or len(self.subtitle) < 5):
            self._type = 'advertisement'
        return self._type

    def to_json(self):
        if not self._parsed:
            self._parse()

        ret = {
            'title': self.title, 'subpoint': self.subpoint,
            'subtitle': self.subtitle, 'type': self.type,
            'source': self.source, 'news': self.news,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return json.dumps(ret, ensure_ascii=False)

    def save_all(self, filename: str, img_type='jpg'):
        self.img.save(f'{filename}.{img_type}')
        self.crop_title.save(f'{filename}_title.{img_type}')
        self.crop_subpoint.save(f'{filename}_subpoint.{img_type}')
        if self.crop_subtitle:
            self.crop_subtitle.save(f'{filename}_subtitle.{img_type}')
        self.crop_bottom.save(f'{filename}_bottom.{img_type}')

    def debug(self):
        self.img.show()
        self.crop.title().show()
        self.crop.subpoint().show()
        self.crop.subtitle().show()


def analyze(news, parser=ocr.parse_by_google):
    return NewsModel(news, parser=parser)
