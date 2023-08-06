"""
A set of objects that are suited to being the basis
of the UFO-Workbench tool. This works on UFO files.
"""
__version__ = "0.2.2"

from defcon import registerRepresentationFactory, unregisterRepresentationFactory

from .objects.font import Font
from .objects.layerSet import LayerSet
from .objects.layer import Layer
from .objects.glyph import Glyph
from .objects.contour import Contour
from .objects.point import Point
from .objects.component import Component
from .objects.anchor import Anchor
from .objects.image import Image
from .objects.info import Info
from .objects.groups import Groups
from .objects.kerning import Kerning
from .objects.features import Features
from .objects.lib import Lib
from .objects.uniData import UnicodeData
from .objects.color import Color
from .objects.guideline import Guideline
#from .objects.layoutEngine import LayoutEngine
