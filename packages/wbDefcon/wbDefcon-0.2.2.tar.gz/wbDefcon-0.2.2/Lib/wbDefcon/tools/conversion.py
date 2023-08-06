"""
conversion
===============================================================================

Convert private robofont attributes to UFO-3 format and back
"""

from ..objects.guideline import Guideline

robofontKey = "com.typemytype.robofont"
publicKey = "public"
guideKey = ".".join((robofontKey, "guides"))
markKey = ".".join((robofontKey, "mark"))
publicMark = ".".join((publicKey, "markColor"))


def robofont_guides_to_UFO3(font):
    # get font level guidelines
    if guideKey in font.lib:
        for guideDict in font.lib[guideKey]:
            font.appendGuideline(
                Guideline(
                    guidelineDict=dict(
                        x=guideDict.get("x", 0),
                        y=guideDict.get("y", 0),
                        angle=guideDict.get("angle", 0.0),
                        name=guideDict.get("name"),
                    )
                )
            )
        del font.lib[guideKey]
    for glyph in font:
        # get glyph level guidelines
        if guideKey in glyph.lib:
            for guideDict in glyph.lib[guideKey]:
                glyph.appendGuideline(
                    Guideline(
                        guidelineDict=dict(
                            x=guideDict.get("x", 0),
                            y=guideDict.get("y", 0),
                            angle=guideDict.get("angle", 0.0),
                            name=guideDict.get("name"),
                        )
                    )
                )
            del glyph.lib[guideKey]


def robofont_mark_to_UFO3(font):
    for glyph in font:
        if markKey in glyph.lib:
            glyph.lib[publicMark] = ",".join(str(c) for c in glyph.lib[markKey])
            del glyph.lib[markKey]


def UFO3_guides_to_robofont(font):
    # get font level guidelines
    guidelines = []
    for guideline in font.guidelines:
        guideDict = dict(
            angle=float(guideline.angle),
            isGlobal=True,
            magnetic=5,
            x=float(guideline.x),
            y=float(guideline.y),
        )
        if guideline.name:
            guideDict["name"] = guideline.name
        guidelines.append(guideDict)
    if guidelines:
        font.lib[guideKey] = guidelines
        font.clearGuidelines()
    for glyph in font:
        # get glyph level guidelines
        guidelines = []
        for guideline in glyph.guidelines:
            guideDict = dict(
                angle=float(guideline.angle),
                isGlobal=False,
                magnetic=5,
                x=float(guideline.x),
                y=float(guideline.y),
            )
            if guideline.name:
                guideDict["name"] = guideline.name
            guidelines.append(guideDict)
        if guidelines:
            glyph.lib[guideKey] = guidelines
            glyph.clearGuidelines()


def UFO3_mark_to_robofont(font):
    for glyph in font:
        if publicMark in glyph.lib:
            glyph.lib[markKey] = [float(c) for c in glyph.lib[publicMark].split(",")]
            del glyph.lib[publicMark]
