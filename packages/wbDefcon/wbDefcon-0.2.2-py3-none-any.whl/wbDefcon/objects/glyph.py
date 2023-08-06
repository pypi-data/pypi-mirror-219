"""
glyph
===============================================================================
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Type, Union, List, Dict, Sequence
import defcon
from fontTools.pens.pointInsidePen import PointInsidePen

from fontParts.base.base import TransformationMixin

from ..pens.outlineTestPen import OutlineTestPen
from ..undomanager import UndoManager
from .anchor import Anchor
from .color import Color
from .component import Component
from .contour import Contour
from .guideline import Guideline
from .image import Image
from .lib import Lib
from .point import Point

if TYPE_CHECKING:
    from wbpUFO.view.glyph import UfoGlyphView
    from . import Transformation, Number
    from .font import Font
    from .layer import Layer
    from ..pens.outlineTestPen import OutlineError

# Number = Union[int, float]
# Matrix = Sequence[Number]


def outlineTestRepresentationFactory(glyph: Glyph) -> List[OutlineError]:
    pen = OutlineTestPen(glyph.layer._glyphSet)
    glyph.drawPoints(pen)
    return pen.errors


class GlyphUndoManager(UndoManager):
    parent: Glyph

    @property
    def glyph(self) -> Glyph:
        return self.parent

    @property
    def font(self) -> Optional[Font]:
        glyph = self.glyph
        if glyph:
            return glyph.font
        return None

    def undo(self) -> None:
        font = self.font
        if font:
            font.holdNotifications()
        super().undo()
        if font:
            font.releaseHeldNotifications()

    def redo(self) -> None:
        font = self.font
        if font:
            font.holdNotifications()
        super().redo()
        if font:
            font.releaseHeldNotifications()


class Glyph(defcon.Glyph, TransformationMixin):
    _undoManager: Optional[GlyphUndoManager]
    anchorClass: Type[Anchor]
    anchors: List[Anchor]
    componentClass: Type[Component]
    components: Component
    contourClass: Type[Contour]
    font: Optional[Font]
    guidelineClass: Type[Guideline]
    guidelines: List[Guideline]
    image: Image
    imageClass: Type[Image]
    layer: Optional[Layer]
    leftMargin: Number
    lib: Lib
    libClass: Type[Lib]
    name: str
    pointClass: Type[Point]
    rightMargin: Number
    unicode: Optional[int]
    width: Number

    def __init__(self, layer: Optional[Layer] = None):
        super(Glyph, self).__init__(
            layer,
            contourClass=Contour,
            pointClass=Point,
            componentClass=Component,
            anchorClass=Anchor,
            guidelineClass=Guideline,
            libClass=Lib,
            imageClass=Image,
        )

    def __repr__(self) -> str:
        return f'<wbDefcon Glyph "{self.name}" at 0x{id(self):04X}>'

    # ----------
    # mark color
    # ----------

    def _get_markColor(self) -> Optional[Color]:
        value: Color
        value = self.lib.get("public.markColor")
        if value is not None:
            value = Color(value)
        return value

    def _set_markColor(self, value: Optional[Color]) -> None:
        # convert to a color object
        if value is not None:
            value = Color(value)
        # don't write if there is no change
        oldValue = self.lib.get("public.markColor")
        if oldValue is not None:
            oldValue = Color(oldValue)
        if value == oldValue:
            return
        # remove
        if value is None:
            if "public.markColor" in self.lib:
                del self.lib["public.markColor"]
        # store
        else:
            self.lib["public.markColor"] = value
        self.postNotification(
            notification="Glyph.MarkColorChanged",
            data=dict(oldValue=oldValue, newValue=value),
        )

    markColor = property(
        _get_markColor,
        _set_markColor,
        doc="""The glyph's mark color. When setting, the value can be a UFO color string, 
        a sequence of (r, g, b, a) or a :class:`Color` object. Setting this 
        posts *Glyph.MarkColorChanged* and *Glyph.Changed* notifications.""",
    )

    # --------
    # Contours
    # --------
    def instantiateContour(self, contourDict: Dict[str, list] = None) -> Contour:
        contour = self.contourClass(glyph=self)
        if contourDict is not None:
            contour.setDataFromSerialization(contourDict)
        return contour

    # ------------
    # Point Inside
    # ------------

    def pointInside(self, coordinates: Sequence[Number], evenOdd: bool = False) -> bool:
        """
        Returns a boolean indicating if **(x, y)** is in the
        "black" area of the glyph.
        """
        (x, y) = coordinates
        pen = PointInsidePen(glyphSet=self.layer, testPoint=(x, y), evenOdd=evenOdd)
        self.draw(pen)
        return pen.getResult()

    # --------------
    # Transformation
    # --------------
    def _transformBy(self, matrix: Transformation, **kwargs) -> None:
        """
        Subclasses may override this method.
        """
        self.disableNotifications(observer=self)
        self.holdNotifications()
        for contour in self:
            contour.transformBy(matrix)
        for component in self.components:
            component.transformBy(matrix)
        for anchor in self.anchors:
            anchor.transformBy(matrix)
        for guideline in self.guidelines:
            guideline.transformBy(matrix)
        self.enableNotifications(observer=self)
        self.releaseHeldNotifications()

    def move(self, values: Sequence[Number]) -> None:
        """
        Move all contours, components and anchors in the glyph
        by **(x, y)**.

        This posts a *Glyph.Changed* notification.
        """
        (x, y) = values
        self.disableNotifications(observer=self)
        self.holdNotifications()
        for contour in self:
            contour.move((x, y))
        for component in self._components:
            component.move((x, y))
        for anchor in self._anchors:
            anchor.move((x, y))
        self.enableNotifications(observer=self)
        self.releaseHeldNotifications()
        # self.postNotification("Glyph.Changed")

    # ----------
    # Selection
    # ----------

    @property
    def selected(self) -> bool:
        """The selection state of the glyph"""
        if self.layer:
            return self.name in self.layer._selectedGlyphNames
        return False

    @selected.setter
    def selected(self, value: bool) -> None:
        if self.layer:
            selected = bool(value)
            selectedGlyphNames = set(self.layer._selectedGlyphNames)
            if selected:
                selectedGlyphNames.add(self.name)
            elif self.name in selectedGlyphNames:
                selectedGlyphNames.remove(self.name)
            self.layer.selectedGlyphNames = list(selectedGlyphNames)

    def selectRect(
        self,
        rect: Sequence[Number],
        addToSelection: bool = False,
        selectPoints: bool = True,
        selectComponents: bool = True,
        selectAnchors: bool = True,
        selectGuidelines: bool = True,
    ) -> None:
        x0, y0, x1, y1 = rect
        min_x = min(x0, x1)
        max_x = max(x0, x1)
        min_y = min(y0, y1)
        max_y = max(y0, y1)
        if not addToSelection:
            for contour in self:
                contour.selected = False
            for anchor in self.anchors:
                anchor.selected = False
            for component in self.components:
                component.selected = False
            for guideline in self.guidelines:
                guideline.selected = False
        if selectPoints:
            for contour in self:
                for point in contour.onCurvePoints:
                    if min_x <= point.x <= max_x and min_y <= point.y <= max_y:
                        point.selected = True
                contour.updateSelection()
        if selectComponents:
            for component in self.components:
                x0, y0, x1, y1 = component.controlPointBounds
                if x0 >= min_x and y0 >= min_y and x1 <= max_x and y1 <= max_y:
                    component.selected = True
        if selectAnchors:
            for anchor in self.anchors:
                if min_x <= anchor.x <= max_x and min_y <= anchor.y <= max_y:
                    anchor.selected = True
        if selectGuidelines:
            for guideline in self.guidelines:
                if min_x <= guideline.x <= max_x and min_y <= guideline.y <= max_y:
                    guideline.selected = True

    # undo

    def _get_undoManager(self) -> GlyphUndoManager:
        if self._undoManager is None:
            # create undoManager on demand
            self._undoManager = GlyphUndoManager(self)
            self._undoManager.destroyRepresentations.append("outlineErrors")
            self.addObserver(self._undoManager, "handleNotification", None)
        return self._undoManager

    def _set_undoManager(self, manager: GlyphUndoManager) -> None:
        assert isinstance(manager, UndoManager)
        assert manager.parent == self
        self._undoManager = manager

    undoManager = property(
        _get_undoManager,
        _set_undoManager,
        doc="The undo manager assigned to this glyph.",
    )

    def show(self, newPage: bool = False, view: Optional[UfoGlyphView] = None) -> bool:
        if self.font:
            return self.font.showGlyph(self.name, newPage, view)
        return False

    def getOutlineErrors(self) -> List[OutlineError]:
        return self.getRepresentation("outlineErrors")

    def round(
        self,
        ndigits: int = 0,
        roundPoints: bool = True,
        roundAnchors: bool = True,
        roundComponents: bool = True,
    ) -> None:
        if roundPoints:
            for contour in self:
                contour.round(ndigits)
                contour.postNotification("Contour.PointsChanged")
        if roundAnchors:
            for anchor in self.anchors:
                anchor.round(ndigits)
        if roundComponents:
            for component in self.components:
                component.round(ndigits)


defcon.registerRepresentationFactory(
    Glyph,
    "outlineErrors",
    outlineTestRepresentationFactory,
    destructiveNotifications=("Glyph.ContoursChanged", "Glyph.ComponentsChanged"),
)
