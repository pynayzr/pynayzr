# -*- coding: utf-8 -*-

import unittest
from pynayzr import streams


class TestStreams(unittest.TestCase):
    def test_qq(self):
        streams.get('cti').close()


if __name__ == '__main__':
    unittest.main()
