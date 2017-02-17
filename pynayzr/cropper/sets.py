# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class SETSCropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        self.title_box = (275, 560, 1200, 641)
        self.subpoint_box = (275, 645, 420, 720)
        self.subtitle_box = (432, 645, 1280, 720)
        self.source_box = (75, 475, 275, 530)
