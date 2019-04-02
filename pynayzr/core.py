# -*- coding: utf-8 -*-

import asyncio
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

    def __init__(self, news, image_path=None, parser=None,_async=True):
        if news not in cropper.support_news:
            raise NotImplementedError
        self.news = news

        # Force parser to tesseract if google credentials not found
        if not parser:
            parser = ocr.parse_by_async_tesseract if _async else ocr.parse_by_tesseract
        self.parser = parser

        # Lazy parse
        self._async = _async
        self.img = None
        self.crop = None
        self.img_read_timestamp = None
        self._title = None
        self._subpoint = None
        self._subtitle = None
        self._type = 'unknown'
        self.subject = None
        self.source = None

        # Choice image source from live or image
        # NOTE: Image size must be 1280x720
        if image_path:
            self.img = Image.open(image_path)
            self._crop()
        elif not _async:
            self.img = streams.get(news)
            self._crop()

    @classmethod
    async def create(cls, self):
        self.img = await streams.aget(self.news)
        self._crop()
        self.img_read_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self

    @classmethod
    async def create_and_parse(cls, self):
        self = await cls.create(self)
        await self._async_parse()
        return self

    def _crop(self):
        self.crop = cropper.support_news[self.news](img=self.img)
        self.crop_title = self.crop.title()
        self.crop_subpoint = self.crop.subpoint()
        self.crop_subtitle = self.crop.subtitle()
        self.crop_bottom = self.crop.bottom()

    def _parse(self):
        if not self.parser or not self.img or not self.crop:
            return

        if True:
            self._title = self.parser(self.crop_title)
            if self.crop_subtitle:
                self._subtitle = self.parser(self.crop_subtitle)
            self._subpoint = self.parser(self.crop_subpoint)
        else:
            # XXX: Only Bing support this
            # Do it once
            attrs = ['_title', '_subpoint']
            imgs = [self.crop_title, self.crop_subpoint]
            if self.crop_subtitle:
                attrs.append('_subtitle')
                imgs.append(self.crop_subtitle)
            results, j = self.parser(imgs)
            for attr, v in zip(attrs, results):
                setattr(self, attr, v)

    async def _async_parse(self):
        if not self.parser or not self.img or not self.crop:
            return
        self._title = await self.parser(self.crop_title)
        if self.crop_subtitle:
            self._subtitle = await self.parser(self.crop_subtitle)
        self._subpoint = await self.parser(self.crop_subpoint)

    @property
    def type(self):
        if self.title and self.subtitle:
            self._type = 'news'
        if not self.title and (not self.subtitle or len(self.subtitle) < 5):
            self._type = 'advertisement'
        return self._type

    @property
    def title(self):
        if self._title is None and self.img and self.crop:
            self._title = self.parser(self.crop_title)
        return self._title

    @property
    def subtitle(self):
        if self._subtitle is None and self.img and self.crop:
            self._subtitle = self.parser(self.crop_subtitle) if self.crop_subtitle else ""
        return self._subtitle

    @property
    def subpoint(self):
        if self._subpoint is None and self.img and self.crop:
            self._subpoint = self.parser(self.crop_subpoint)
        return self._subpoint

    def to_json(self):
        if not self.img or not self.crop:
            raise ValueError

        # XXX: WTF? You will need to deal with property, I TOLD YOU
        #      >>> nm.subtitle  # this will failed when using async
        if (self._async and
                (self._title is None or self._subtitle is None or
                 self._subpoint is None)):
            asyncio.run(self._async_parse())
        elif self._title is None or self._subtitle is None or self._subpoint is None:
            self._parse()

        ret = {
            'title': self.title, 'subpoint': self.subpoint,
            'subtitle': self.subtitle, 'type': self.type,
            'source': self.source, 'news': self.news,
            'timestamp': self.img_read_timestamp
        }
        return json.dumps(ret, ensure_ascii=False)

    def save_all(self, filename: str, img_type='jpg'):
        if not self.img or not self.crop:
            raise ValueError

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


def analyze(news, parser=ocr.parse_by_google, _async=False):
    return NewsModel(news, parser=parser, _async=_async)


async def async_analyze(news: list, parser=ocr.parse_by_google, parse=False):
    async def mark(key, coro):
        return key, await coro
    if parse:
        d = {n: NewsModel.create_and_parse(NewsModel(n, parser=parser))
             for n in news}
    else:
        d = {n: NewsModel.create(NewsModel(n, parser=parser))
             for n in news}
    return {
        key: result
        for key, result in await asyncio.gather(
                *(mark(key, coro) for key, coro in d.items()))
        }
