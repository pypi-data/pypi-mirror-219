"""
contour
===============================================================================
"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Type
import defcon
from fontParts.base.base import TransformationMixin
from fontTools.pens.pointPen import ReverseContourPointPen
from .point import Point

from ..tools.representations import contourFlattenedRepresentationFactory

if TYPE_CHECKING:
    from .glyph import Glyph

Segment = List[Point]

class Contour(defcon.Contour, TransformationMixin):
    pointClass:Type[Point]
    _points:List[Point]
    segments:List[Segment]
    representationFactories = defcon.Contour.representationFactories
    representationFactories["defcon.contour.flattened"][
        "factory"
    ] = contourFlattenedRepresentationFactory

    def __init__(self, glyph:Optional[Glyph]=None):
        super(Contour, self).__init__(glyph, pointClass=Point)

    def __repr__(self) -> str:
        if self.glyph is not None:
            try:
                return f'<wbDefcon Contour {self.glyph.contourIndex(self)} of "{self.glyph.name}" at  0x{id(self):04X}>'
            except ValueError:
                return f"<wbDefcon Contour at  0x{id(self):04X}>"
        return f"<wbDefcon Contour (orphan) at  0x{id(self):04X}>"

    # -------------
    # List Behavior
    # -------------

    def reverse(self) -> None:
        """
        Reverse the direction of the contour. It's important to note
        that the actual points stored in this object will be completely
        repalced by new points.

        This will post *Contour.WindingDirectionChanged*,
        *Contour.PointsChanged* and *Contour.Changed* notifications.
        """
        # from ufoLib.pointPen import ReverseContourPointPen

        oldDirection = self.clockwise
        # put the current points in another contour
        otherContour = self.__class__(glyph=None)
        # draw the points in this contour through
        # the reversing pen.
        reversePen = ReverseContourPointPen(otherContour)
        self.drawPoints(reversePen)
        # clear the points in this contour
        self._clear(postNotification=False)
        # set the points back into this contour
        self._points = otherContour._points
        # post a notification
        self.postNotification(
            "Contour.WindingDirectionChanged",
            data=dict(oldValue=oldDirection, newValue=self.clockwise),
        )
        self.postNotification("Contour.PointsChanged")
        self.dirty = True

    # --------
    # Segments
    # --------

    def segmentIndex(self, point:Point) -> int:
        for i, segment in enumerate(self.segments):
            if point in segment:
                return i
        return -1

    def convertSegmentToCurve(self, segmentIndex:int) -> None:
        segments = self.segments
        segment = segments[segmentIndex]
        point = segment[-1]
        if point.segmentType == "line":
            pointIndex = self.index(point)
            prevPoint = self[pointIndex - 1]
            dx = (point.x - prevPoint.x) / 3
            dy = (point.y - prevPoint.y) / 3
            self._points.insert(pointIndex, Point((point.x - dx, point.y - dy)))
            self._points.insert(pointIndex, Point((prevPoint.x + dx, prevPoint.y + dy)))
            point.segmentType = "curve"
            self.postNotification("Contour.PointsChanged")
            self.dirty = True

    # ----------
    # Selection
    # ----------

    @property
    def selected(self) -> bool:
        """The selection state of the contour. True if all points are selected, False otherwise"""
        if self:
            for point in self:
                if not point.selected:
                    return False
            return True
        return False

    @selected.setter
    def selected(self, value:bool) -> None:
        newVal = bool(value)
        changed = False
        for point in self._points:
            if point._selected != newVal:
                point._selected = newVal
                changed = True
        if changed:
            self.postNotification("Contour.SelectionChanged")

    def updateSelection(self) -> None:
        if self.selected:
            return
        for segmentIndex, segment in enumerate(self.segments):
            if segmentIndex == 0:
                prevSegment = self.segments[-1]
            segmentType = segment[-1].segmentType
            if segmentType == "curve":
                segment[0].selected = prevSegment[-1].selected
                segment[1].selected = segment[2].selected
            prevSegment = segment

    # --------------
    # Transformation
    # --------------

    def _transformBy(self, matrix, **kwargs) -> None:
        """
        Subclasses may override this method.
        """
        for point in self:
            point.transformBy(matrix)
        self.postNotification("Contour.PointsChanged")
        self.dirty = True

    def round(self, ndigits:int=0) -> None:
        for point in self:
            point.round(ndigits)
