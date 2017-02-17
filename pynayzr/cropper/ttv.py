# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class TTVCropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        # TTV will use title box for substitute
        self.title_box = (293, 554, 1280, 640)
        self.subpoint_box = (252, 640, 434, 720)
        self.subtitle_box = (434, 640, 1280, 720)
