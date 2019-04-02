# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class CTVCropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        self.title_box = (255, 575, 1270, 645)
        self.subpoint_box = (260, 650, 434, 690)
        self.subtitle_box = (440, 650, 1280, 720)
