"""
layerSet
===============================================================================
"""
import defcon
from fontTools.ufoLib import UFOReader
from fontTools.ufoLib.errors import UFOLibError

from .point import Point
from .contour import Contour
from .component import Component
from .guideline import Guideline
from .anchor import Anchor
from .lib import Lib
from .image import Image
from .glyph import Glyph
from .layer import Layer
from .uniData import UnicodeData


class LayerSet(defcon.LayerSet):
    def __init__(self, font=None):
        super(LayerSet, self).__init__(
            font,
            layerClass=Layer,
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

    def __repr__(self):
        return f"<wbDefcon LayerSet at {id(self)}>"

    # -------------
    # Layer Creation
    # -------------

    def instantiateLayer(self, glyphSet):
        return self._layerClass(layerSet=self, glyphSet=glyphSet)

    # ---------------------
    # External Edit Support
    # ---------------------

    def reloadLayers(self, layerData):
        """
        Reload the layers. This should not be called externally.
        """
        with UFOReader(self.font.path, validate=self.font.ufoLibReadValidate) as reader:
            # handle the layers
            currentLayerOrder = self.layerOrder
            for layerName, l in layerData.get("layers", {}).items():
                # new layer
                if layerName not in currentLayerOrder:
                    glyphSet = reader.getGlyphSet(
                        layerName,
                        validateRead=self.ufoLibReadValidate,
                        validateWrite=self.font.ufoLibWriteValidate,
                    )
                    self.newLayer(layerName, glyphSet)
                # get the layer
                layer = self[layerName]
                # reload the layer info
                if l.get("info"):
                    layer.color = None
                    layer.lib.clear()
                    try:
                        layer._glyphSet.readLayerInfo(layer)
                    except UFOLibError:
                        # for UFOFileStructure.ZIP, if zip is closed get a new one from the reader
                        layer._glyphSet = reader.getGlyphSet(
                            layerName,
                            validateRead=self.ufoLibReadValidate,
                            validateWrite=self.font.ufoLibWriteValidate,
                        )
                        layer._glyphSet.readLayerInfo(layer)
                    self._stampLayerInfoDataState(layer)
                # reload the glyphs
                glyphNames = l.get("glyphNames", [])
                if glyphNames:
                    layer.reloadGlyphs(glyphNames)
            # handle the order
            if layerData.get("order", False):
                newLayerOrder = reader.getLayerNames()
                for layerName in self.layerOrder:
                    if layerName not in newLayerOrder:
                        newLayerOrder.append(layerName)
                self.layerOrder = newLayerOrder
            # handle the default layer
            if layerData.get("default", False):
                newDefaultLayerName = reader.getDefaultLayerName()
                self.defaultLayer = self[newDefaultLayerName]
