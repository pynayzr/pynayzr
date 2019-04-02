# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class CTICropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        super().__init__('cti')
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        self.title_box = (305, 570, 1280, 650)
        self.subpoint_box = (305, 650, 463, 690)
        self.subtitle_box = (465, 650, 1280, 690)
