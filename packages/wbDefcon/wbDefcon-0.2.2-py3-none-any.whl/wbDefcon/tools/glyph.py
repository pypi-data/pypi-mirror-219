"""
glyph
===============================================================================
"""
import re

from feaASTools.renameGlyph import renameGlyphInFeatureText

digits = re.compile(r"^[0-9]*$")


def renameGlyph(
    glyph,
    newName,
    inComponents=True,
    inGroups=True,
    inKerning=True,
    inFeatures=True,
    allLayers=True,
):
    font = glyph.font
    if not font:
        glyph.name = newName
        return
    oldName = glyph.name
    if oldName != newName:
        if glyph.layer == font.layers.defaultLayer:
            if newName in font:
                raise ValueError(f"Glyph with name '{newName}' already exists in {font}.")
        else:
            if newName in glyph.layer:
                raise ValueError(
                    f"Glyph with name '{newName}' already exists on layer '{glyph.layer.name}'."
                )
        if allLayers:
            for layer in font.layers:
                if newName in layer:
                    raise ValueError(
                        f"Glyph with name '{newName}' already exists on layer '{layer.name}'."
                    )
        glyph.name = newName
        if inComponents:
            composites = glyph.layer.componentReferences.get(oldName, ())
            for name in composites:
                composite = glyph.layer[name]
                for component in composite.components:
                    if component.baseGlyph == oldName:
                        component.baseGlyph = newName
        if glyph.layer == font.layers.defaultLayer:
            if inGroups:
                groups = font.groups
                for groupName in [g for g in groups if oldName in groups[g]]:
                    groups[groupName] = [
                        newName if n == oldName else n for n in groups[groupName]
                    ]
            if inKerning:
                kerning = font.kerning
                pairs = tuple(kerning.keys())
                for pair in pairs:
                    if oldName in pair:
                        value = kerning.pop(pair)
                        newPair = tuple(newName if n == oldName else n for n in pair)
                        kerning[newPair] = value
            if inFeatures:
                featureText = font.features.text
                if featureText:
                    font.features.text = renameGlyphInFeatureText(
                        featureText, oldName, newName
                    )
        if allLayers:
            for layer in font.layers:
                if layer != glyph.layer and oldName in layer:
                    renameGlyph(
                        layer[oldName],
                        newName,
                        inComponents,
                        inGroups,
                        inKerning,
                        inFeatures,
                        allLayers=False,
                    )


def glyphNameInFont(font, name):
    """Return True if glyph with name exists on any layer in font"""
    for layer in font.layers:
        if name in layer:
            return True
    return False


def getSaveKeepName(glyph):
    oldName = glyph.name
    if "." in oldName:
        base, ext = oldName.rsplit(".", 1)
        if digits.match(ext):
            oldName = base
    num = 1
    newName = oldName + ".%02d" % num
    font = glyph.font
    if not font:
        while newName == glyph.name:
            num += 1
            newName = oldName + ".%02d" % num
        return newName
    while glyphNameInFont(font, newName):
        num += 1
        newName = oldName + ".%02d" % num
    return newName


def deleteGlyph(
    glyph, inComponents=None, inGroups=True, inKerning=True, allLayers=True
):
    font = glyph.font
    if not font:
        del glyph
        return
    glyphName = glyph.name
    if inComponents:
        composites = glyph.layer.componentReferences.get(glyphName, ())
        for name in composites:
            composite = glyph.layer[name]
            for component in reversed(composite.components):
                if component.baseGlyph == glyphName:
                    if inComponents == "delete":
                        composite.removeComponent(component)
                    if inComponents == "decompose":
                        composite.decomposeComponent(component)
    if glyph.layer == font.layers.defaultLayer:
        if inGroups:
            groups = font.groups
            for groupName in [g for g in groups if glyphName in groups[g]]:
                groups[groupName] = [n for n in groups[groupName] if n != glyphName]
        if inKerning:
            kerning = font.kerning
            for pair in [p for p in kerning.keys()]:
                if glyphName in pair:
                    del kerning[pair]
    if allLayers:
        for layer in [l for l in font.layers if glyphName in l]:
            deleteGlyph(
                layer[glyphName],
                inComponents,
                inGroups=False,
                inKerning=False,
                allLayers=False,
            )
    else:
        del glyph.layer[glyphName]
