# -*- coding: utf-8 -*-

import unittest
from pynayzr import streams


class TestStreams(unittest.TestCase):
    def test_all_streams(self):
        for news in streams.support_news:
            with self.subTest(news=news):
                streams.get(news)

    def test_cti(self):
        streams.get('cti').close()

    def test_tvbs(self):
        streams.get('tvbs').close()


if __name__ == '__main__':
    unittest.main()
