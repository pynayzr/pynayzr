# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class TVBSCropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        self.title_box = (320, 572, 1250, 642)
        self.subpoint_box = (320, 645, 475, 680)
        self.subtitle_box = (475, 645, 1280, 680)
