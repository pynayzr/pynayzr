# -*- coding: utf-8 -*-

from PIL import Image
from pynayzr.cropper import crop


class CTSCropper(crop.CropBase):
    def __init__(self, image_path=None, img=None):
        super().__init__('cts')
        if not image_path and not img:
            raise ValueError

        if img and not isinstance(img, Image.Image):
            raise TypeError

        if img:
            self.image = img
        if image_path:
            self.image = Image.open(image_path)

        # XXX: CTS will change title box to subtitle sometime
        #      (subtitle for the speaker)
        self.title_box = (205, 575, 1215, 645)
        self.subpoint_box = (190, 655, 330, 690)
        self.subtitle_box = (340, 655, 970, 690)
