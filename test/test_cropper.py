# -*- coding: utf-8 -*-

from PIL import Image
import unittest
from pynayzr.cropper import crop, ttv, ftv, sets


class TestCropBase(unittest.TestCase):
    def test_blank_base(self):
        base = crop.CropBase('base')
        self.assertEqual(base.name, 'base')
        self.assertEqual(base.image, None)
        self.assertEqual(base.title_box, None)
        self.assertEqual(base.subtitle_box, None)
        self.assertEqual(base.source_box, None)


class TestTTVCropper(unittest.TestCase):
    def setUp(self):
        self.p = ttv.TTVCropper('tests/imgs/ttv/main_01.jpg')

    def test_crop_title(self):
        self.assertIsInstance(self.p.title(), Image.Image)

    def test_crop_subtitle(self):
        self.assertIsInstance(self.p.subtitle(), Image.Image)


class TestSETSCropper(unittest.TestCase):
    def setUp(self):
        self.p = sets.SETSCropper('tests/imgs/set/main_02.jpg')

    def test_crop_title(self):
        self.assertIsInstance(self.p.title(), Image.Image)

    def test_crop_subtitle(self):
        self.assertIsInstance(self.p.subtitle(), Image.Image)

    def test_crop_source(self):
        self.assertIsInstance(self.p.source(), Image.Image)


class TestFTVCropper(unittest.TestCase):
    def setUp(self):
        self.p = ftv.FTVCropper('tests/imgs/ftv/main_02.jpg')

    def test_crop_title(self):
        self.assertIsInstance(self.p.title(), Image.Image)

    def test_crop_subtitle(self):
        self.assertIsInstance(self.p.subtitle(), Image.Image)


if __name__ == '__main__':
    unittest.main()
