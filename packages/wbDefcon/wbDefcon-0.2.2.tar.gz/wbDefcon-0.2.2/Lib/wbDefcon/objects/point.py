"""
point
===============================================================================
"""
from math import sqrt

import defcon
from fontParts.base.base import TransformationMixin
from fontTools.misc import transform


class Point(defcon.Point, TransformationMixin):
    __slots__ = ("_selected",)

    def __init__(
        self, coordinates, segmentType=None, smooth=False, name=None, identifier=None
    ):
        super().__init__(coordinates, segmentType, smooth, name, identifier)
        self._selected = False

    def __iter__(self):
        return iter((self._x, self._y))

    # ----------
    # Selection
    # ----------
    @property
    def selected(self):
        """The selection state of the point"""
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = bool(value)

    def round(self, ndigits=0):
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)

    def distance(self, other):
        other_x, other_y = other
        return sqrt((self.x - other_x) ** 2 + (self.y - other_y) ** 2)

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, **kwargs):
        """
        This is the environment implementation of
        :meth:`BasePoint.transformBy`.

        **matrix** will be a :ref:`type-transformation`.
        that has been normalized with
        :func:`normalizers.normalizeTransformationMatrix`.
        """
        t = transform.Transform(*matrix)
        x, y = t.transformPoint((self.x, self.y))
        self.x = x
        self.y = y
