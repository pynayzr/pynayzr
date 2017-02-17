# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class CTICropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        self.title_box = (295, 575, 1280, 649)
        self.subpoint_box = (295, 650, 463, 685)
        self.subtitle_box = (463, 650, 1280, 685)
