"""
image
===============================================================================
"""
import defcon

from .color import Color


class Image(defcon.Image):

    # color

    def _get_color(self):
        return self.get("color")

    def _set_color(self, color):
        if color is None:
            newColor = None
        else:
            newColor = Color(color)
        oldColor = self.get("color")
        if newColor == oldColor:
            return
        self["color"] = newColor
        self.postNotification(
            "Image.ColorChanged", data=dict(oldValue=oldColor, newValue=newColor)
        )

    color = property(
        _get_color,
        _set_color,
        doc="The image's :class:`Color` object. When setting, the value can be a UFO color string, a sequence of (r, g, b, a) or a :class:`Color` object. Setting this posts *Image.ColorChanged* and *Image.Changed* notifications.",
    )
