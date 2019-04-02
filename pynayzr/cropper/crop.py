# -*- coding: utf-8 -*-


class CropBase:
    def __init__(self, name):
        self.name = name
        self._image = None

        # [Left, Top, Right, Bottom]
        self.title_box = None
        self.subpoint_box = None
        self.subtitle_box = None
        self.person_box = None
        self.source_box = None

        # Base size (720p)
        self.bw = 1280
        self.bh = 720

        # Image size
        self.iw = None
        self.ih = None

    def __del__(self):
        if self._image:
            self._image.close()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, im):
        self.iw, self.ih = im.size
        self.rx = self.iw / self.bw
        self.ry = self.ih / self.bh
        self._image = im

    def resize(self, box):
        if self.rx == 1.0 and self.ry == 1.0:
            return box
        return [int(box[0] * self.ry), int(box[1] * self.rx),
                int(box[2] * self.ry), int(box[3] * self.rx)]

    def title(self):
        if self.title_box:
            return self.image.crop(self.resize(self.title_box))
        return None

    def subpoint(self):
        if self.subpoint_box:
            return self.image.crop(self.resize(self.subpoint_box))
        return None

    def subtitle(self):
        if self.subtitle_box:
            return self.image.crop(self.resize(self.subtitle_box))
        return None

    def bottom(self):
        # XXX: Assume image is 720p
        return self.image.crop(self.resize([0, 530, 1280, 720]))

    def person(self):
        if self.person_box:
            return self.image.crop(self.resize(self.person_box))
        return None

    def source(self):
        if self.source_box:
            return self.image.crop(self.resize(self.source_box))
        return None
