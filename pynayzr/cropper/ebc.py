# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class EBCCropper(crop.CropBase):
    # TODO: Not complete
    def __init__(self, image_path=None, img=None):
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        self.title_box = (320, 578, 1200, 642)
        self.subpoint_box = (320, 642, 480, 700)
        self.subtitle_box = (480, 642, 1280, 700)
