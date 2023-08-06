"""
anchor
===============================================================================
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional, Dict

import defcon
from fontParts.base.base import TransformationMixin
from fontTools.misc import transform

from .color import Color

if TYPE_CHECKING:
    from . import Number, Transformation
    from .glyph import Glyph


class Anchor(defcon.Anchor, TransformationMixin):
    x: Number
    y: Number

    def __init__(
        self, glyph: Optional[Glyph] = None, anchorDict: Optional[Dict[str, Any]] = None
    ):
        super().__init__(glyph, anchorDict)
        self._selected = False

    def __repr__(self) -> str:
        return f'<wbDefcon Anchor "{self.name}" ({self.x}, {self.y}) at {id(self)}>'

    # color

    def _get_color(self) -> Optional[Color]:
        color:Optional[Color] = self.get("color")
        return color

    def _set_color(self, color: Optional[Color]) -> None:
        if color is None:
            newColor = None
        else:
            newColor = Color(color)
        oldColor = self.get("color")
        if newColor == oldColor:
            return
        self["color"] = newColor
        self.postNotification(
            "Anchor.ColorChanged", data=dict(oldValue=oldColor, newValue=newColor)
        )

    color = property(
        _get_color,
        _set_color,
        doc="""The anchors's :class:`Color` object. 
        When setting, the value can be a UFO color string, 
        a sequence of (r, g, b, a) or a :class:`Color` object. 
        Setting this posts *Anchor.ColorChanged* and *Anchor.Changed* notifications.""",
    )

    def asDict(self) -> Dict[str, Any]:
        return dict(x=self.x, y=self.y, name=self.name, color=self.color)

    # ----------
    # Selection
    # ----------

    @property
    def selected(self) -> bool:
        """The selection state of the anchor"""
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        self._selected = bool(value)

    def round(self, ndigits: int = 0) -> None:
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
        t = transform.Transform(*matrix)
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y
