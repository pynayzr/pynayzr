# -*- coding: utf-8 -*-


class CropBase:
    def __init__(self, name):
        self.name = name
        self.image = None

        # [Left, Top, Right, Bottom]
        self.title_box = None
        self.subpoint_box = None
        self.subtitle_box = None
        self.person_box = None
        self.source_box = None

    def __del__(self):
        if self.image:
            self.image.close()

    def title(self):
        if self.title_box:
            return self.image.crop(self.title_box)
        return None

    def subpoint(self):
        if self.subpoint_box:
            return self.image.crop(self.subpoint_box)
        return None

    def subtitle(self):
        if self.subtitle_box:
            return self.image.crop(self.subtitle_box)
        return None

    def bottom(self):
        # XXX: Assume image is 720p
        return self.image.crop([0, 530, 1280, 720])

    def person(self):
        if self.person_box:
            return self.image.crop(self.person_box)
        return None

    def source(self):
        if self.source_box:
            return self.image.crop(self.source_box)
        return None
