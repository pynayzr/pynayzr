# -*- coding: utf-8 -*-

import unittest
from pynayzr import ocr
from pynayzr.cropper import sets


@unittest.skip('just skip')
class TestOCR(unittest.TestCase):
    def setUp(self):
        self.p = sets.SETSCropper('tests/imgs/set/main_02.jpg')
        self.title = self.p.title()
        self.subtitle = self.p.subtitle()

    def test_tesseract(self):
        self.assertEqual(ocr.parse_by_tesseract(self.title),
                         '流氓夜巿隨機打人 攤商遭安全帽砸頭')

    def test_google_vision_api(self):
        ocr.set_google_credentials('tests/key.json')
        self.assertEqual(ocr.parse_by_google(self.title),
                         '流氓夜市隨機打人攤商遭安全帽砸頭\n')


if __name__ == '__main__':
    unittest.main()
