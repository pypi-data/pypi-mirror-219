"""
lineIntersectionPen
===============================================================================
"""
from fontTools.misc.bezierTools import curveLineIntersections, lineLineIntersections
from fontTools.pens.basePen import BasePen


class LineIntersectionPen(BasePen):
    def __init__(self, line=None, glyphSet=None):
        super().__init__(glyphSet)
        self.filterDoubles = True
        self._line = []
        self.line = line
        self.intersections = set()
        self.startPt = None
        self.currentPt = None

    def reset(self):
        self.intersections = set()
        self.startPt = None
        self.currentPt = None

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value
        self.reset()

    def _moveTo(self, pt):
        self.currentPt = pt
        self.startPt = pt

    def _lineTo(self, pt):
        if self.filterDoubles:
            if pt == self.currentPt:
                return
        if self.line:
            intersections = lineLineIntersections(
                self.currentPt, pt, self.line[0], self.line[1]
            )
            for intersection in intersections:
                if all(0 <= t <= 1 for t in (intersection.t1, intersection.t2)):
                    self.intersections.add(intersection.pt)
        self.currentPt = pt

    def _curveToOne(self, pt1, pt2, pt3):
        if self.line:
            intersections = curveLineIntersections(
                (self.currentPt, pt1, pt2, pt3), self.line
            )
            for intersection in intersections:
                if all(0 <= t <= 1 for t in (intersection.t1, intersection.t2)):
                    self.intersections.add(intersection.pt)
        self.currentPt = pt3

    def _closePath(self):
        if self.currentPt != self.startPt:
            self._lineTo(self.startPt)
        self.currentPt = self.startPt = None

    def _endPath(self):
        self.currentPt = None
