"""
color
===============================================================================
"""
from colorsys import rgb_to_hsv, hsv_to_rgb
from enum import Enum

import wx
from defcon.objects.color import _stringify, _stringToSequence
from fontTools.misc.py23 import basestring
from wx.lib.colourdb import getColourList, updateColourDB

if not wx.GetApp():
    from wbBase.application import App
    app = App(test=True)
updateColourDB()



class Color(str):

    """
    This object represents a color. This object is immutable.

    The initial argument can be either a color string as defined in the UFO
    specification or a sequence of (red, green, blue, alpha) components.

    By calling str(colorObject) you will get a UFO compatible color string.
    You can also iterate over the object to create a sequence::

        colorTuple = tuple(colorObject)
    """

    def __new__(cls, value):
        # convert from string
        if isinstance(value, basestring):
            value = _stringToSequence(value)
        # convert from wx.Colour
        elif isinstance(value, wx.Colour):
            value = tuple(c / 255 for c in value)
        r, g, b, a = value
        # validate the values
        color = (("r", r), ("g", g), ("b", b), ("a", a))
        for component, v in color:
            if v < 0 or v > 1:
                raise ValueError(
                    "The color for %s (%s) is not between 0 and 1."
                    % (component, str(v))
                )
        # convert back to a normalized string
        r = _stringify(r)
        g = _stringify(g)
        b = _stringify(b)
        a = _stringify(a)
        s = ",".join((r, g, b, a))
        # call the super
        return super().__new__(cls, s)

    @classmethod
    def from_wx(cls, wxColour):
        return cls(
            (
                wxColour.red / 255,
                wxColour.green / 255,
                wxColour.blue / 255,
                wxColour.alpha / 255,
            )
        )

    @classmethod
    def from_hsv(cls, h, s, v):
        r, g, b = hsv_to_rgb(h, s, v)
        return cls((r, g, b, 1))

    def __eq__(self, other):
        # print(f"__eq__({self, other})")
        try:
            return super().__eq__(self.__class__(other))
        except ValueError:
            return False
        except TypeError:
            return False

    def __iter__(self):
        value = _stringToSequence(self)
        return iter(value)

    def _get_r(self):
        return _stringToSequence(self)[0]

    r = property(_get_r, doc="The red component.")

    def _get_g(self):
        return _stringToSequence(self)[1]

    g = property(_get_g, doc="The green component.")

    def _get_b(self):
        return _stringToSequence(self)[2]

    b = property(_get_b, doc="The blue component.")

    def _get_a(self):
        return _stringToSequence(self)[3]

    a = property(_get_a, doc="The alpha component.")

    @property
    def wx(self):
        """Return color as wx.Colour"""
        return wx.Colour(
            round(self.r * 255),
            round(self.g * 255),
            round(self.b * 255),
            round(self.a * 255),
        )

    @property
    def hsv(self):
        """tuple (Hue, Saturation, Value (Brightness))"""
        # r, g, b, a = self.sequence
        return rgb_to_hsv(self.r, self.g, self.b)

    @property
    def hue(self):
        return self.hsv[0]


# def _stringToSequence(value):
#     r, g, b, a = [i.strip() for i in value.split(",")]
#     value = []
#     for component in (r, g, b, a):
#         try:
#             v = int(component)
#             value.append(v)
#             continue
#         except ValueError:
#             pass
#         v = float(component)
#         value.append(v)
#     return value


# def _stringify(v):
#     """
# 	>>> _stringify(1)
# 	'1'
# 	>>> _stringify(.1)
# 	'0.1'
# 	>>> _stringify(.01)
# 	'0.01'
# 	>>> _stringify(.001)
# 	'0.001'
# 	>>> _stringify(.0001)
# 	'0.0001'
# 	>>> _stringify(.00001)
# 	'0.00001'
# 	>>> _stringify(.000001)
# 	'0'
# 	>>> _stringify(.000005)
# 	'0.00001'
# 	"""
#     # it's an int
#     i = int(v)
#     if v == i:
#         return str(i)
#         # it's a float
#     else:
#         # find the shortest possible float
#         for i in range(1, 6):
#             s = "%%.%df" % i
#             s = s % v
#             if float(s) == v:
#                 break
#                 # see if the result can be converted to an int
#         f = float(s)
#         i = int(f)
#         if f == i:
#             return str(i)
#             # otherwise return the float
#         return s


# red = Color((1, 0, 0, 1))
# green = Color((0, 1, 0, 1))
# blue = Color((0, 0, 1, 1))
# yellow = Color((1, 1, 0, 1))
# magenta = Color((1, 0, 1, 1))
# cyan = Color((0, 1, 1, 1))

mark = Enum(
    "mark",
    [
        (c, Color(wx.Colour(c)))
        for c in getColourList()
        if " " not in c and c[-1] not in "01234567899"
    ],
    type=Color,
    module=__name__,
)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
