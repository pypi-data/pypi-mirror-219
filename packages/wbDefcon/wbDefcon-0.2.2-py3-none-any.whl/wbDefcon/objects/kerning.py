"""
kerning
===============================================================================
"""
import defcon


def sortedPairListFactory(kerning):
    pairList = list(kerning.keys())
    pairList.sort(key=lambda p: tuple(n.replace("public.kern", "@", 1) for n in p))
    return pairList


class Kerning(defcon.Kerning):
    @property
    def sortedPairList(self):
        return self.getRepresentation("sortedPairList")

    @classmethod
    def fromUFOlib2_Kerning(cls, font, ufolib2_kerning):
        kerning = cls(font)
        kerning.disableNotifications()
        kerning.update(ufolib2_kerning)
        kerning.dirty = True
        kerning.enableNotifications()
        return kerning


defcon.registerRepresentationFactory(
    Kerning,
    "sortedPairList",
    sortedPairListFactory,
    destructiveNotifications=("Kerning.Changed",),
)
