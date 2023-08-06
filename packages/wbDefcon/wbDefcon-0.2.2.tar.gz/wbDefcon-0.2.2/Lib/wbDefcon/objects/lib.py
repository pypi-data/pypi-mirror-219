"""
lib
===============================================================================
"""

import defcon

class Lib(defcon.Lib):

    @classmethod
    def fromUFOlib2_Lib(cls, font=None, layer=None, glyph=None, ufolib2_Lib=None):
        lib = cls(font=font, layer=layer, glyph=glyph)
        lib.disableNotifications()
        lib.update(ufolib2_Lib)
        lib.dirty = True
        lib.enableNotifications()
        return lib
