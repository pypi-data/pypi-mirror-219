"""
imageSet
===============================================================================
"""

from defcon.objects.imageSet import ImageSet as defconImageSet

class ImageSet(defconImageSet):
    def __init__(self, font=None):
        super().__init__(font)
        self._dirty = False
