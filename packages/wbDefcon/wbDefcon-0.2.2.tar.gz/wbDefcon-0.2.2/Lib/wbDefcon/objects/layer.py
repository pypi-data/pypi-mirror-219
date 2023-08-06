"""
layer
===============================================================================
"""
from __future__ import annotations

import logging
from typing import Iterator, List, Sequence, Type, TYPE_CHECKING, Optional

import defcon
from fs.errors import FilesystemClosed

from .anchor import Anchor
from .color import Color
from .component import Component
from .contour import Contour
from .glyph import Glyph
from .guideline import Guideline
from .image import Image
from .lib import Lib
from .point import Point
from .uniData import UnicodeData

if TYPE_CHECKING:
    from fontTools.ufoLib.glifLib import GlyphSet
    from .layerSet import LayerSet

log = logging.getLogger(__name__)


class Layer(defcon.Layer):
    _glyphClass: Type[Glyph]
    _color: Color
    _glyphSet: GlyphSet

    def __init__(
        self, layerSet: Optional[LayerSet] = None, glyphSet: Optional[GlyphSet] = None
    ):
        super().__init__(
            layerSet,
            glyphSet,
            libClass=Lib,
            unicodeDataClass=UnicodeData,
            guidelineClass=Guideline,
            glyphClass=Glyph,
            glyphContourClass=Contour,
            glyphPointClass=Point,
            glyphComponentClass=Component,
            glyphAnchorClass=Anchor,
            glyphImageClass=Image,
        )
        self._selectedGlyphNames:List[str] = []

    def __repr__(self) -> str:
        if self.name:
            return f"<wbDefcon Layer {self.name} at 0x{id(self):04X}>"
        return f"<wbDefcon Layer at 0x{id(self):04X}>"

    # color

    def _get_color(self) -> Color:
        return self._color

    def _set_color(self, color: Color) -> None:
        if color is None:
            newColor = None
        else:
            newColor = Color(color)
        oldColor = self._color
        if oldColor != newColor:
            self._color = newColor
            data = dict(oldColor=oldColor, newColor=newColor)
            self.postNotification(notification="Layer.ColorChanged", data=data)
            self.dirty = True

    color = property(
        _get_color,
        _set_color,
        doc="The layer's :class:`Color` object. When setting, the value can be a UFO color string, a sequence of (r, g, b, a) or a :class:`Color` object. Setting this posts *Layer.ColorChanged* and *Layer.Changed* notifications.",
    )

    # --------------
    # Glyph Creation
    # --------------

    def instantiateGlyphObject(self) -> Glyph:
        return self._glyphClass(layer=self)

    def loadGlyph(self, name:str) -> Glyph:
        """
        Load a glyph from the glyph set. This should not be called
        externally, but subclasses may override it for custom behavior.
        """
        # log.debug("loadGlyph(%r)", name)
        if (
            self._glyphSet is None
            or name not in self._glyphSet
            or name in self._scheduledForDeletion
        ):
            raise KeyError("%s not in layer" % name)
        glyph = self.instantiateGlyphObject()
        glyph.disableNotifications()
        glyph._isLoading = True
        glyph.name = name
        try:
            self._stampGlyphDataState(glyph)
            # log.debug("_stampGlyphDataState worked")
        except FilesystemClosed:
            # for UFOFileStructure.ZIP, if zip is closed get a new one from the reader
            font = self.font
            self._glyphSet = font._reader.getGlyphSet(
                self.name,
                validateRead=font._layers.ufoLibReadValidate,
                validateWrite=font._layers.ufoLibWriteValidate,
            )
            self._stampGlyphDataState(glyph)
            # log.debug("_stampGlyphDataState glyphSet reloaded")
        self._insertGlyph(glyph)
        pointPen = glyph.getPointPen()
        self._glyphSet.readGlyph(glyphName=name, glyphObject=glyph, pointPen=pointPen)
        glyph.dirty = False
        glyph._isLoading = False
        glyph.enableNotifications()
        return glyph

    def reloadGlyphs(self, glyphNames: Sequence[str]) -> None:
        """
        Reload the glyphs. This should not be called externally.
        """
        for glyphName in glyphNames:
            if glyphName not in self._glyphs:
                self.loadGlyph(glyphName)
            else:
                glyph = self._glyphs[glyphName]
                glyph.destroyAllRepresentations(None)
                glyph.clear()
                pointPen = glyph.getPointPen()
                if self._glyphSet is not None:
                    try:
                        self._glyphSet.readGlyph(
                            glyphName=glyphName, glyphObject=glyph, pointPen=pointPen
                        )
                    except FilesystemClosed:
                        # for UFOFileStructure.ZIP, if zip is closed get a new one from the reader
                        font = self.font
                        self._glyphSet = font._reader.getGlyphSet(
                            self.name,
                            validateRead=font._layers.ufoLibReadValidate,
                            validateWrite=font._layers.ufoLibWriteValidate,
                        )
                        self._glyphSet.readGlyph(
                            glyphName=glyphName, glyphObject=glyph, pointPen=pointPen
                        )
                glyph.dirty = False
                self._stampGlyphDataState(glyph)
        data = dict(glyphNames=glyphNames)
        # post a change notification for any glyphs that
        # reference the reloaded glyphs via components.
        componentReferences = self.componentReferences
        referenceChanges = set()
        for glyphName in glyphNames:
            if glyphName not in componentReferences:
                continue
            for reference in componentReferences[glyphName]:
                if reference in glyphNames:
                    continue
                if reference not in self._glyphs:
                    continue
                if reference in referenceChanges:
                    continue
                glyph = self._glyphs[reference]
                glyph.destroyAllRepresentations(None)
                glyph.postNotification(notification=glyph.changeNotificationName)
                referenceChanges.add(reference)

    def newGlyph(self, name: str) -> Glyph:
        log.debug("%r in %r -> %r", name, self, name in self)
        glyph:Glyph
        if name in self:
            # log.debug("clear existing glyph")
            glyph = self[name]
            glyph.holdNotifications(note="Requested by Layer.newGlyph.")
            glyph.clearContours()
            glyph.clearComponents()
            glyph.clearAnchors()
            glyph.clearGuidelines()
            glyph.clearImage()
            glyph.width = 0
            glyph.note = None
            glyph.unicode = None
            glyph.markColor = None
            glyph.releaseHeldNotifications()
            return glyph
        # log.debug("%r create new glyph '%s'", self, name)
        glyph = super().newGlyph(name)
        return glyph

    # --------------
    # Selection
    # --------------

    @property
    def selectedGlyphNames(self) -> Sequence[str]:
        return [n for n in self._selectedGlyphNames if n in self]

    @selectedGlyphNames.setter
    def selectedGlyphNames(self, value: Sequence[str]) -> None:
        assert isinstance(value, (list, tuple, set, frozenset))
        oldSelection = frozenset(self._selectedGlyphNames)
        selectedGlyphNames = set(n for n in value if n in self)
        self._selectedGlyphNames = list(selectedGlyphNames)
        glyphNames = self.font.document.fontView.frame.glyphGridPanel.glyphNames
        self._selectedGlyphNames.sort(key=glyphNames.index)
        unselected = frozenset(oldSelection - selectedGlyphNames)
        selected = frozenset(selectedGlyphNames - oldSelection)
        if unselected or selected:
            data = dict(unselected=unselected, selected=selected)
            self.postNotification(notification="Layer.GlyphSelectionChanged", data=data)

    @selectedGlyphNames.deleter
    def selectedGlyphNames(self) -> None:
        self.selectedGlyphNames = []

    @property
    def selectedGlyphs(self) -> Iterator[Glyph]:
        for name in self.selectedGlyphNames:
            yield self[name]

    @selectedGlyphs.setter
    def selectedGlyphs(self, value: Sequence[Glyph]) -> None:
        self.selectedGlyphNames = [g.name for g in value]

    @selectedGlyphs.deleter
    def selectedGlyphs(self) -> None:
        self.selectedGlyphNames = []

    @property
    def selectedGlyphCount(self) -> int:
        return len([n for n in self._selectedGlyphNames if n in self])
