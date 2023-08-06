"""
component
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Sequence

import defcon
from fontParts.base.base import TransformationMixin
from fontTools.misc import transform

if TYPE_CHECKING:
    from defcon.tools.notifications import Notification

    from . import Number, Transformation
    from .glyph import Glyph


class Component(defcon.Component, TransformationMixin):
    baseGlyph: str
    transformation: Transformation

    def __init__(self, glyph: Optional[Glyph] = None):
        super().__init__(glyph)
        self._selected = False

    def __repr__(self) -> str:
        return f'<wbDefcon Component "{self.baseGlyph}" of "{self.glyph.name}" at  0x{id(self):04X}>'

    # ----------
    # Selection
    # ----------

    @property
    def selected(self) -> bool:
        """The selection state of the component"""
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        newVal = bool(value)
        if newVal != self._selected:
            self._selected = newVal
            self.postNotification("Component.SelectionChanged")

    def round(self, ndigits: int = 0) -> None:
        """round the offset part of the transformation"""
        transformation = list(self.transformation)
        transformation[4] = round(transformation[4], ndigits)
        transformation[5] = round(transformation[5], ndigits)
        self.transformation = tuple(transformation)

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix: Transformation, **kwargs: Any) -> None:
        """
        Subclasses may override this method.
        """
        t = transform.Transform(*matrix)
        transformation = t.transform(self.transformation)
        self.transformation = tuple(transformation)

    # --------------
    # Offset
    # --------------
    @property
    def offset(self) -> Sequence[Number]:
        """The component's offset."""
        sx, sxy, syx, sy, ox, oy = self.transformation
        return ox, oy

    @offset.setter
    def offset(self, value: Sequence[Number]) -> None:
        sx, sxy, syx, sy, ox, oy = self.transformation
        ox, oy = value
        self.transformation = sx, sxy, syx, sy, ox, oy

    # --------------
    # Scale
    # --------------
    @property
    def scale(self) -> Sequence[Number]:
        """The component's scale."""
        sx, sxy, syx, sy, ox, oy = self.transformation
        return sx, sy

    @scale.setter
    def scale(self, value: Sequence[Number]) -> None:
        sx, sxy, syx, sy, ox, oy = self.transformation
        sx, sy = value
        self.transformation = sx, sxy, syx, sy, ox, oy

    # ------------------------
    # Notification Observation
    # ------------------------

    def baseGlyphDataChangedNotificationCallback(
        self, notification: Notification
    ) -> None:
        self.destroyAllRepresentations()
        super().baseGlyphDataChangedNotificationCallback(notification)
