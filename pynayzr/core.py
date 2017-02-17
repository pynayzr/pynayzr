# -*- coding: utf-8 -*-

import json
import datetime
from PIL import Image
from pynayzr import cropper
from pynayzr import ocr
from pynayzr.ocr import get_google_credentials
from pynayzr import streams


class NewsModel:
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

        self.title = parser(self.crop.title())
        self.subpoint = parser(self.crop.subpoint())
        self.subtitle = parser(self.crop.subtitle())
        self._type = 'unknown'
        self.subject = None
        self.source = None

    @property
    def type(self):
        if self.title and self.subtitle:
            self._type = 'news'
        if not self.title and (not self.subtitle or len(self.subtitle) < 5):
            self._type = 'advertisement'
        return self._type

    def to_json(self):
        ret = {
            'title': self.title, 'subpoint': self.subpoint,
            'subtitle': self.subtitle, 'type': self.type,
            'source': self.source, 'news': self.news,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return json.dumps(ret, ensure_ascii=False)

    def debug(self):
        self.img.show()
        self.crop.title().show()
        self.crop.subpoint().show()
        self.crop.subtitle().show()


def analyze(news, parser=ocr.parse_by_google):
    return NewsModel(news, parser=parser)
