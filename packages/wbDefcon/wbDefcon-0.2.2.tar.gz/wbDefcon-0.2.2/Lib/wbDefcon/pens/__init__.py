import logging
from math import sqrt
from fontTools.pens.basePen import BasePen
from fontTools.misc.bezierTools import (
    splitLine,
    calcCubicParameters,
    solveCubic,
    _splitCubicAtT,
)
from .outlineTestPen import OutlineTestPen

log = logging.getLogger(__name__)


class GraphicsPen(BasePen):
    """
    Pen to draw onto a Graphics drawing context (wx.GraphicsContext).
    """

    def __init__(self, glyphSet):
        BasePen.__init__(self, glyphSet)
        self.path = None

    def _moveTo(self, pt):
        self.path.MoveToPoint(pt)

    def _lineTo(self, pt):
        self.path.AddLineToPoint(pt)

    def _curveToOne(self, pt1, pt2, pt3):
        self.path.AddCurveToPoint(pt1, pt2, pt3)

    def _qCurveToOne(self, p1, p2):
        self.path.AddQuadCurveToPoint(*p1 + p2)

    def _closePath(self):
        self.path.CloseSubpath()


graphicsPen = GraphicsPen(None)


class GraphicsRoundingPen(BasePen):
    """
    Pen to draw onto a Graphics drawing context (wx.GraphicsContext).
    """

    def __init__(self, glyphSet):
        BasePen.__init__(self, glyphSet)
        self.path = None

    def _moveTo(self, pt):
        x, y = pt
        self.path.MoveToPoint(round(x), round(y))

    def _lineTo(self, pt):
        x, y = pt
        self.path.AddLineToPoint(round(x), round(y))

    def _curveToOne(self, pt1, pt2, pt3):
        x1, y1 = pt1
        x2, y2 = pt2
        x3, y3 = pt3
        self.path.AddCurveToPoint(x1, y1, x2, y2, round(x3), round(y3))

    def _qCurveToOne(self, p1, p2):
        self.path.AddQuadCurveToPoint(*p1 + p2)

    def _closePath(self):
        self.path.CloseSubpath()


graphicsRoundingPen = GraphicsRoundingPen(None)


class HitTestPen(BasePen):
    """Perform hit test on glyph outline"""

    def __init__(self, position=None, tolerance=2):
        BasePen.__init__(self)
        self.position = position
        self.tolerance = tolerance
        # self.filterDoubles = True
        self.contourIndex = None
        self.segmentIndex = None
        self.startPt = None
        self.hit = None

    @classmethod
    def distance(cls, pt0, pt1):
        x0, y0 = pt0
        x1, y1 = pt1
        dx = abs(x0 - x1)
        dy = abs(y0 - y1)
        return sqrt(dx ** 2 + dy ** 2)

    @classmethod
    def splitCubic(cls, pt1, pt2, pt3, pt4, where, isHorizontal):
        a, b, c, d = calcCubicParameters(pt1, pt2, pt3, pt4)
        ts = solveCubic(
            a[isHorizontal], b[isHorizontal], c[isHorizontal], d[isHorizontal] - where
        )
        ts = [t for t in ts if 0 <= t < 1]
        ts.sort()
        if not ts:
            return [((pt1, pt2, pt3, pt4), 1)]
        parts = _splitCubicAtT(a, b, c, d, *ts)
        ts.append(1)
        # print 'ts', ts
        # print 'parts', parts
        return list(zip(parts, ts))

    @property
    def posX(self):
        return self.position[0]

    @property
    def posY(self):
        return self.position[1]

    @property
    def currentPt(self):
        return self._getCurrentPoint()

    def reset(self):
        self.contourIndex = None
        self.segmentIndex = None
        self.startPt = None
        self.hit = None

    def moveTo(self, pt):
        super().moveTo(pt)
        self.segmentIndex = 0
        # print("moveTo", pt)

    def lineTo(self, pt):
        i = self.segmentIndex
        super().lineTo(pt)
        if self.segmentIndex == i:
            self.segmentIndex += 1
        # print("lineTo", pt)

    def curveTo(self, *points):
        i = self.segmentIndex
        super().curveTo(*points)
        if self.segmentIndex == i:
            self.segmentIndex += 1
        # print("curveTo", *points)

    def qCurveTo(self, *points):
        i = self.segmentIndex
        super().qCurveTo(*points)
        if self.segmentIndex == i:
            self.segmentIndex += 1
        # print("qCurveTo", *points)

    def _moveTo(self, pt):
        if not self.hit:
            # self.currentPt = pt
            self.startPt = pt
            if self.contourIndex is None:
                self.contourIndex = 0
            else:
                self.contourIndex += 1
            # self.segmentIndex = 0

    def _lineTo(self, pt):
        if not self.hit:
            lineLength = self.distance(self.currentPt, pt)
            parts = splitLine(self.currentPt, pt, self.posX, False)
            vHit = None
            if len(parts) > 1:
                for part in parts[:-1]:
                    vDist = self.distance(self.position, part[1])
                    if vDist <= self.tolerance:
                        partLength = self.distance(part[0], part[1])
                        vHit = (vDist, part[1], partLength / lineLength)
            parts = splitLine(self.currentPt, pt, self.posY, True)
            hHit = None
            if len(parts) > 1:
                for part in parts[:-1]:
                    hDist = self.distance(self.position, part[1])
                    if hDist <= self.tolerance:
                        partLength = self.distance(part[0], part[1])
                        hHit = (hDist, part[1], partLength / lineLength)
            if vHit is not None and hHit is not None:
                # todo: make correct calculation of t
                self.hit = (
                    self.contourIndex,
                    self.segmentIndex,
                    (vHit[2] + hHit[2]) / 2.0,
                )
            elif vHit is not None:
                self.hit = (self.contourIndex, self.segmentIndex, vHit[2])
            elif hHit is not None:
                self.hit = (self.contourIndex, self.segmentIndex, hHit[2])
            # self.currentPt = pt
            # self.segmentIndex += 1

    def _curveToOne(self, pt1, pt2, pt3):
        if not self.hit:
            parts = self.splitCubic(self.currentPt, pt1, pt2, pt3, self.posX, False)
            # print parts
            vHits = []
            if len(parts) > 1:
                for part, t in parts[:-1]:
                    vDist = self.distance(self.position, part[-1])
                    # print part, t, vDist
                    if vDist <= self.tolerance:
                        vHits.append((vDist, part, t))
            vHits.sort()
            parts = self.splitCubic(self.currentPt, pt1, pt2, pt3, self.posY, True)
            hHits = []
            if len(parts) > 1:
                for part, t in parts[:-1]:
                    hDist = self.distance(self.position, part[-1])
                    # print part, t, hDist
                    if hDist <= self.tolerance:
                        hHits.append((hDist, part, t))
            hHits.sort()
            if len(vHits) > 0 and len(hHits) > 0:
                # todo: make correct calculation of t
                self.hit = (
                    self.contourIndex,
                    self.segmentIndex,
                    (vHits[0][2] + hHits[0][2]) / 2.0,
                )
            elif len(vHits) > 0:
                self.hit = (self.contourIndex, self.segmentIndex, vHits[0][2])
            elif len(hHits) > 0:
                self.hit = (self.contourIndex, self.segmentIndex, hHits[0][2])
            # self.currentPt = pt3
            # self.segmentIndex += 1

    def _closePath(self):
        # if not self.hit:
        if self.currentPt != self.startPt:
            self._lineTo(self.startPt)
        # self.currentPt = self.startPt = None
        self.startPt = None

    def addComponent(self, glyphName, transformation):
        """we don't make hit tests on components"""
        pass


class ContourHit(object):
    """Helper class to represent result of hit test detection"""

    def __init__(self, glyph, contourIndex, segmentIndex, t):
        self.glyph = glyph
        self.contourIndex = contourIndex
        self.segmentIndex = segmentIndex
        self.t = t

    @property
    def contour(self):
        return self.glyph[self.contourIndex]

    @property
    def segment(self):
        try:
            return self.contour.segments[self.segmentIndex]
        except IndexError as e:
            log.exception("No segment at index %r", self.segmentIndex)
            return None

    @property
    def selected(self):
        if not self.segment:
            return False
        for point in self.segment:
            if not point.selected:
                return False
        return True

    @selected.setter
    def selected(self, value):
        newVal = bool(value)
        changed = False
        try:
            if self.segment[-1]._selected != newVal:
                self.segment[-1]._selected = newVal
                changed = True
            if self.segmentIndex == 0:
                prevSegment = self.contour.segments[-1]
            else:
                prevSegment = self.contour.segments[self.segmentIndex - 1]
            if prevSegment[-1]._selected != newVal:
                prevSegment[-1]._selected = newVal
                changed = True
        except IndexError:
            pass
        if changed:
            self.contour.updateSelection()
            self.contour.postNotification("Contour.SelectionChanged")

    def splitAndInsertPoint(self):
        self.contour.splitAndInsertPointAtSegmentAndT(self.segmentIndex, self.t)
        self.contour.round()

    def convertToCurve(self):
        self.contour.convertSegmentToCurve(self.segmentIndex)
        self.contour.round()


class KeepSmoothPen(BasePen):
    def __init__(self, contour):
        BasePen.__init__(self)
        self.contour = contour
        self.segmentIndex = None
        self.pointIndex = None

    def _moveTo(self, pt):
        self.currentPt = pt
        self.startPt = pt
        self.segmentIndex = 0
        self.pointIndex = 0
        if not self.contour[self.pointIndex].selected:
            print("check move", pt)

    def _lineTo(self, pt):
        self.currentPt = pt
        self.segmentIndex += 1
        self.pointIndex += 1

    def _curveToOne(self, pt1, pt2, pt3):
        self.currentPt = pt3
        self.pointIndex += 3
        self.segmentIndex += 1
