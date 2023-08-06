"""
features
===============================================================================
"""
from __future__ import annotations

import io
import logging
from typing import TYPE_CHECKING, Optional

import defcon
import fontTools.feaLib.ast as ast
from fontTools.feaLib.error import FeatureLibError
from fontTools.feaLib.parser import Parser

if TYPE_CHECKING:
    from ufoLib2.objects.features import Features as UFOlib2_Features
    from .font import Font

log = logging.getLogger(__name__)


class Features(defcon.Features):
    @classmethod
    def fromUFOlib2_Features(cls, font:Font, ufolib2_features:UFOlib2_Features) -> Features:
        features = cls(font)
        features.text = ufolib2_features.text
        return features

    def getSyntaxtree(self, useGlyphNames: bool = True) -> Optional[ast.FeatureFile]:
        return self.getRepresentation("syntaxtree", useGlyphNames=useGlyphNames)

    def setSyntaxtree(self, syntaxtree: ast.FeatureFile) -> None:
        assert isinstance(syntaxtree, ast.FeatureFile)
        self.text = syntaxtree.asFea()


def featureSyntaxtreeRepresentationFactory(
    features: Features, useGlyphNames: bool = True
) -> Optional[ast.FeatureFile]:
    text = features.text
    if text:
        featureFile = io.StringIO(text)
        if useGlyphNames and features.font:
            glyphNames = features.font.keys()
        else:
            glyphNames = ()
        # return Parser(featureFile, glyphNames).parse()
        try:
            return Parser(featureFile, glyphNames).parse()
        except FeatureLibError:
            log.warning("featureSyntaxtreeRepresentationFactory failed")
    log.info("No feature text")
    return None


defcon.registerRepresentationFactory(
    Features, "syntaxtree", featureSyntaxtreeRepresentationFactory
)
