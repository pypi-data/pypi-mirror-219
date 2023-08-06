"""
representations
===============================================================================
"""
from fontPens.flattenPen import FlattenPen


# -------
# Contour
# -------

# flattened

def contourFlattenedRepresentationFactory(contour, approximateSegmentLength=5, segmentLines=False):
    from ..objects.glyph import Glyph
    glyph = Glyph()
    outputPen = glyph.getPen()
    flattenPen = FlattenPen(outputPen, approximateSegmentLength=approximateSegmentLength, segmentLines=segmentLines)
    contour.draw(flattenPen)
    output = glyph[0]
    return output
