"""
font
===============================================================================
"""
from __future__ import annotations
import os
import logging
import defcon
from typing import TYPE_CHECKING, Type, List, Generator, Optional, Sequence, Iterator
from fontTools.ufoLib import UFOFileStructure, UFOFormatVersion, UFOReader

from .point import Point
from .contour import Contour
from .component import Component
from .guideline import Guideline
from .anchor import Anchor
from .lib import Lib
from .image import Image
from .glyph import Glyph
from .kerning import Kerning
from .info import Info
from .groups import Groups
from .features import Features
from .uniData import UnicodeData
from .layer import Layer
from .layerSet import LayerSet
from .imageSet import ImageSet
from .dataSet import DataSet

if TYPE_CHECKING:
    import ufoLib2
    from wbpUFO.document import UfoDocument

log = logging.getLogger(__name__)


class Font(defcon.Font):
    _featuresClass: Type[Features]
    _glyphSet: Layer
    _groupsClass: Type[Groups]
    _infoClass: Type[Info]
    _kerningClass: Type[Kerning]
    _layerSetClass: Type[LayerSet]
    _libClass: Type[Lib]
    _ufoFormatVersion: Optional[UFOFormatVersion]
    _ufoFileStructure: Optional[UFOFileStructure]
    data: DataSet
    guidelines: Sequence[Guideline]
    images: ImageSet
    kerning: Kerning
    info: Info
    lib: Lib

    def __init__(self, path: Optional[str] = None):
        super().__init__(
            path,
            kerningClass=Kerning,
            infoClass=Info,
            groupsClass=Groups,
            featuresClass=Features,
            libClass=Lib,
            unicodeDataClass=UnicodeData,
            layerSetClass=LayerSet,
            layerClass=Layer,
            imageSetClass=ImageSet,
            dataSetClass=DataSet,
            guidelineClass=Guideline,
            glyphClass=Glyph,
            glyphContourClass=Contour,
            glyphPointClass=Point,
            glyphComponentClass=Component,
            glyphAnchorClass=Anchor,
            glyphImageClass=Image,
        )
        self._doc: Optional[UfoDocument] = None
        if not isinstance(self._ufoFormatVersion, UFOFormatVersion):
            self._ufoFormatVersion = UFOFormatVersion.FORMAT_3_0
        if not self._ufoFileStructure:
            self._ufoFileStructure = UFOFileStructure.ZIP

    def __repr__(self) -> str:
        return f"<wbDefcon Font at 0x{id(self):04X}>"

    def getParent(self) -> None:
        return None

    # -----------
    # Properties
    # -----------

    # @property
    # def info(self) -> Info:
    #     "The font's :class:`Info` object."
    #     return self._get_info()

    # @property
    # def lib(self) -> Lib:
    #     return self._get_lib()

    # -----------
    # Sub-Objects
    # -----------

    # layers

    def instantiateLayerSet(self) -> LayerSet:
        return self._layerSetClass(font=self)

    # -------
    # Methods
    # -------

    def getSaveProgressBarTickCount(
        self,
        formatVersion: Optional[UFOFormatVersion] = None,
        structure: Optional[UFOFileStructure] = None,
        path: Optional[str] = None,
    ) -> int:
        """
        Get the number of ticks that will be used by a progress bar
        in the save method. Subclasses may override this method to
        implement custom saving behavior.
        """
        # if not format version is given, use the existing.
        # if that doesn't exist, go to 3.
        if formatVersion is None:
            formatVersion = self._ufoFormatVersion[0]
        if formatVersion is None:
            formatVersion = UFOFormatVersion.FORMAT_3_0
        if structure is None:
            structure = self._ufoFileStructure
        saveAll = structure == UFOFileStructure.ZIP
        if not self.path:
            saveAll = True
        elif path and os.path.realpath(path) != os.path.realpath(self.path):
            saveAll = True
        count = 0
        count += 1  # info
        count += 1  # groups
        count += 1  # lib
        if formatVersion != self._ufoFormatVersion and formatVersion < 3:
            count += 1
        else:
            count += int(self.kerning.dirty or saveAll)
        if formatVersion >= 2:
            count += int(self.features.dirty or saveAll)
        if formatVersion >= 3:
            count += self.images.getSaveProgressBarTickCount(formatVersion)
            count += self.data.getSaveProgressBarTickCount(formatVersion)
        count += self.layers.getSaveProgressBarTickCount(formatVersion)
        return count

    # -----------
    # Workbench stuff
    # -----------

    @property
    def document(self) -> Optional[UfoDocument]:
        return self._doc

    @document.setter
    def document(self, doc: UfoDocument) -> None:
        assert self._doc is None, "Can not replace document in Font"
        assert doc.font is self
        self._doc = doc

    @document.deleter
    def document(self) -> None:
        self._doc = None

    @property
    def selectedGlyphNames(self) -> List[str]:
        return self._glyphSet.selectedGlyphNames

    @selectedGlyphNames.setter
    def selectedGlyphNames(self, value: Sequence[str]) -> None:
        self._glyphSet.selectedGlyphNames = value

    @selectedGlyphNames.deleter
    def selectedGlyphNames(self) -> None:
        self._glyphSet.selectedGlyphNames = []

    @property
    def selectedGlyphs(self) -> Iterator[Glyph]:
        return self._glyphSet.selectedGlyphs

    @selectedGlyphs.setter
    def selectedGlyphs(self, value) -> None:
        self._glyphSet.selectedGlyphs = value

    @selectedGlyphs.deleter
    def selectedGlyphs(self) -> None:
        del self._glyphSet.selectedGlyphs

    def selectAll(self) -> None:
        self._glyphSet.selectedGlyphNames = self._glyphSet.keys()

    @property
    def selectedGlyphCount(self) -> int:
        return self._glyphSet.selectedGlyphCount

    def selectRect(
        self,
        rect,
        addToSelection: bool = False,
        selectGuidelines: bool = True,
    ) -> None:
        """Select subobjects (guidelines) by rect"""
        x0, y0, x1, y1 = rect
        min_x = min(x0, x1)
        max_x = max(x0, x1)
        min_y = min(y0, y1)
        max_y = max(y0, y1)
        if not addToSelection:
            for guideline in self.guidelines:
                guideline.selected = False
        if selectGuidelines:
            for guideline in self.guidelines:
                if min_x <= guideline.x <= max_x and min_y <= guideline.y <= max_y:
                    guideline.selected = True

    def showGlyph(self, name: str, newPage: bool = False, view=None) -> bool:
        """
        Show the glyph identified by name in the UI
        """
        if self.document:
            return self.document.showGlyph(name, newPage, view)
        return False

    # # data comparison

    def _testFontDataForExternalModifications(
        self, obj, fileName: str, reader: Optional[UFOReader] = None
    ) -> bool:
        # font is not on disk
        if self.path is None:
            return False
        # data has not been loaded
        if obj is None:
            return False
        # make a reader if necessary
        closeReader = False
        if reader is None:
            closeReader = True
            reader = UFOReader(self.path, validate=False)
        # get the mod time from the reader
        modTime = reader.getFileModificationTime(fileName)
        # fallback
        result = False
        # file is not in the UFO
        if modTime is None:
            if obj._dataOnDisk:
                result = True
            result = False
        # time stamp mismatch
        elif (
            modTime != obj._dataOnDiskTimeStamp
            or self._ufoFileStructure == UFOFileStructure.ZIP
        ):
            data = reader.readBytesFromPath(fileName)
            if data != obj._dataOnDisk:
                result = True
        if closeReader:
            reader.close()
        # fallback
        return result

    # -----------
    # Get Font object from other implementations
    # -----------

    @classmethod
    def fromUFOlib2_Font(cls, font: ufoLib2.Font) -> Font:
        fontObj: Font = cls()
        # == update attributes instantiated by __init__ ==
        # go ahead and load the layers
        fontObj._layers.disableNotifications()
        for layer in font.layers:
            newLayer = fontObj._layers.newLayer(layer.name)
            newLayer.disableNotifications()
            for glyph in layer:
                newGlyph = newLayer.newGlyph(glyph.name)
                newGlyph.copyDataFromGlyph(glyph)
            newLayer.lib.update(layer.lib)
            newLayer.dirty = True
            newLayer.enableNotifications()
        fontObj._layers.dirty = False
        fontObj._layers.enableNotifications()
        # get the image file names
        fontObj._images.disableNotifications()
        fontObj._images.fileNames = font.images.fileNames[:]
        fontObj._images.enableNotifications()
        # get the data directory listing
        fontObj._data.disableNotifications()
        fontObj._data.fileNames = font.data.fileNames[:]
        fontObj._data.enableNotifications()

        # == update all other attributes ==
        # info
        fontObj._info = fontObj._infoClass.fromUFOlib2_Info(fontObj, font.info)
        fontObj.beginSelfInfoSetNotificationObservation()
        # groups
        fontObj._groups = fontObj._groupsClass.fromUFOlib2_Groups(fontObj, font.groups)
        fontObj.beginSelfGroupsNotificationObservation()
        # kerning
        fontObj._kerning = fontObj._kerningClass.fromUFOlib2_Kerning(
            fontObj, font.kerning
        )
        fontObj.beginSelfKerningNotificationObservation()
        # features
        fontObj._features = fontObj._featuresClass.fromUFOlib2_Features(
            fontObj, font.features
        )
        fontObj.beginSelfFeaturesNotificationObservation()
        # lib
        fontObj._lib = fontObj._libClass.fromUFOlib2_Lib(
            font=fontObj, ufolib2_Lib=font.lib
        )
        fontObj.beginSelfLibNotificationObservation()
        # done, mark as dirty
        fontObj._path = font.path
        fontObj._dirty = True

        return fontObj
