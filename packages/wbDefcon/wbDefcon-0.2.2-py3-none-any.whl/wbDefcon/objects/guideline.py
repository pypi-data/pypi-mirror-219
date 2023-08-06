"""
guideline
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Sequence
import defcon
from fontParts.base.base import TransformationMixin
from fontTools.misc import transform
import wx

from wbBase.tools import get_wxPen

from .color import Color

if TYPE_CHECKING:
    from . import Number
    from .glyph import Glyph

class Guideline(defcon.Guideline, TransformationMixin):
    def __init__(self, font=None, glyph=None, guidelineDict=None):
        super().__init__(font=font, glyph=glyph, guidelineDict=guidelineDict)
        self._selected = False

    # ----------
    # Attributes
    # ----------

    # x

    def _get_x(self) -> Number:
        return self.get("x", 0)

    def _set_x(self, value:Number) -> None:
        old = self.get("x")
        if value == old:
            return
        self["x"] = value
        self.postNotification(
            "Guideline.XChanged", data=dict(oldValue=old, newValue=value)
        )

    x = property(
        _get_x,
        _set_x,
        doc="""The x coordinate. 
    Setting this will post *Guideline.XChanged* and *Guideline.Changed* notifications.""",
    )

    # y

    def _get_y(self) -> Number:
        return self.get("y", 0)

    def _set_y(self, value:Number) -> None:
        old = self.get("y")
        if value == old:
            return
        self["y"] = value
        self.postNotification(
            "Guideline.YChanged", data=dict(oldValue=old, newValue=value)
        )

    y = property(
        _get_y,
        _set_y,
        doc="""The y coordinate. 
        Setting this will post *Guideline.YChanged* and *Guideline.Changed* notifications.""",
    )

    # angle

    def _get_angle(self) -> Number:
        angle = self.get("angle")
        if isinstance(angle, (int, float)):
            return angle
        if self.x and (self.y in (0, None)):
            return 90.0
        return None

    def _set_angle(self, value:Number):
        old = self.get("angle")
        if value == old:
            return
        if value and value < 0:
            value = value + 360
        if value == old:
            return
        self["angle"] = value
        self.postNotification(
            "Guideline.AngleChanged", data=dict(oldValue=old, newValue=value)
        )

    angle = property(
        _get_angle,
        _set_angle,
        doc="The angle. Setting this will post *Guideline.AngleChanged* and *Guideline.Changed* notifications.",
    )

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
            "Guideline.ColorChanged", data=dict(oldValue=oldColor, newValue=newColor)
        )

    color = property(
        _get_color,
        _set_color,
        doc="""The guideline's :class:`Color` object. 
        When setting, the value can be a UFO color string, 
        a sequence of (r, g, b, a) or a :class:`Color` object. 
        Setting this posts *Guideline.ColorChanged* and *Guideline.Changed* notifications.""",
    )

    # ----------
    # Selection
    # ----------

    @property
    def selected(self) -> bool:
        """The selection state of the component"""
        return self._selected

    @selected.setter
    def selected(self, value):
        newVal = bool(value)
        if newVal != self._selected:
            self._selected = newVal
            self.postNotification("Guideline.SelectionChanged")

    @property
    def wxPen(self):
        # from wbFontParts.color import mark
        penStyle = wx.PENSTYLE_LONG_DASH
        if self.color:
            return get_wxPen(color=self.color.wx, style=penStyle)
        if self.glyph is not None:
            return get_wxPen(color="STEELBLUE", style=penStyle)
        return get_wxPen(color="VIOLETRED", style=penStyle)

    # ----
    # Move
    # ----

    def move(self, values):
        """
        Move the anchor by **(x, y)**.

        This will post *Guideline.XChange*, *Guideline.YChanged* and *Guideline.Changed* notifications if anything changed.
        """
        (x, y) = values
        self.x += x
        self.y += y

    def round(self, ndigits=0):
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)


    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix:Transformation, **kwargs:Any) -> None:
        """
        This is the environment implementation of
        :meth:`BaseAnchor.transformBy`.

        **matrix** will be a :ref:`type-transformation`.
        that has been normalized with
        :func:`normalizers.normalizeTransformationMatrix`.
        """
        #todo: rotation is not implemented
        t = transform.Transform(*matrix)
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y
