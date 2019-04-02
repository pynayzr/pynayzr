# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class PTSCropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        super().__init__('pts')
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        self.title_box = (348, 600, 1150, 660)
        self.subpoint_box = (120, 590, 340, 670)
        self.subtitle_box = None
