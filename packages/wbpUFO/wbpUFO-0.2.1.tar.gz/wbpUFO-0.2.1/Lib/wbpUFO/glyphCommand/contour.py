"""
contour
===============================================================================

Glyph Commands related to contours
"""
from booleanOperations import BooleanOperationManager as Boolean

# from fontToolsTools.pens.cleanupContourPointPen import CleanupContourPointPen

from .base import GlyphCommand
from .parameter import (
    ParamBoolRequired,
    ParamEnumeration,
    ParamFlags,
    ParamFloatRequired,
    ParamIntRequired,
)


class ShiftGlyphCommand(GlyphCommand):
    name = "Shift"
    SHIFT_OUTLINE = 1
    SHIFT_ANCHORS = 2
    SHIFT_COMPONENTS = 4
    parameters = [
        ParamIntRequired("x", "Horizontal shift", 0),
        ParamIntRequired("y", "Vertical shift", 0),
        ParamFlags(
            "f",
            "Apply shift to",
            ["Outline", "Anchros", "Components"],
            SHIFT_OUTLINE | SHIFT_ANCHORS,
        ),
        ParamBoolRequired("p", "Preserve Composites", True),
    ]

    def _execute(self, glyph):
        glyph.moveBy((self.x, self.y))
        if self.p:
            font = glyph.font
            if font and hasattr(font, "componentReferences"):
                componentReferences = font.componentReferences
                if glyph.name in componentReferences:
                    distBack = (-self.x, -self.y)
                    for glyphName in componentReferences[glyph.name]:
                        compositeGlyph = font[glyphName]
                        for component in compositeGlyph.components:
                            if component.baseGlyph == glyph.name:
                                component.moveBy(distBack)


class ScaleGlyphCommand(GlyphCommand):
    name = "Scale"
    SCALE_OUTLINE = 1
    SCALE_ANCHORS = 2
    SCALE_COMPONENTS = 4
    parameters = [
        ParamIntRequired("x", "Horizontal scale [%]", 100),
        ParamIntRequired("y", "Vertical scale [%]", 100),
        ParamEnumeration(
            "c", "Scale center", ["Origin point (0,0)", "Center of glyph"], 0
        ),
        ParamFlags(
            "f",
            "Apply scale to",
            ["Outline", "Anchros", "Components"],
            SCALE_OUTLINE | SCALE_ANCHORS,
        ),
    ]

    def _execute(self, glyph):
        glyph.scaleBy((self.x / 100.0, self.y / 100.0))


class SlantGlyphCommand(GlyphCommand):
    name = "Slant"
    parameters = [
        ParamFloatRequired("a", "Slant angle", 10.0),
        ParamEnumeration(
            "d", "Direction", ["Slant to the right", "Slant to the left"], 0
        ),
        ParamEnumeration(
            "c", "Slant center", ["Origin point (0,0)", "Center of glyph"], 0
        ),
    ]

    def _execute(self, glyph):
        glyph.scaleBy((self.x, self.y))


class ContourDirectionCommand(GlyphCommand):
    name = "Contour direction"
    parameters = [
        ParamEnumeration("d", "Direction", ["PostScript", "TrueType", "Reverse all"], 0)
    ]

    def _execute(self, glyph):
        if self.d == 0:
            glyph.correctContourDirection()
        elif self.d == 1:
            glyph.correctContourDirection(trueType=True)
        elif self.d == 2:
            for contour in glyph:
                contour.reverse()


class RemoveOverlapCommand(GlyphCommand):
    name = "Remove overlap"

    def _execute(self, glyph):
        contours = [c for c in glyph]
        Boolean.union([c for c in glyph], glyph.getPointPen())
        for contour in contours:
            glyph.removeContour(contour)


# class CleanupContourCommand(GlyphCommand):
#     name = "Cleanup Contour"

#     def _execute(self, glyph):
#         pen = CleanupContourPointPen(glyph.getPointPen())
#         contours = list(glyph)
#         glyph.clearContours()
#         for contour in contours:
#             contour.drawPoints(pen)


class RoundCommand(GlyphCommand):
    name = "Round"
    ROUND_OUTLINE = 1
    ROUND_ANCHORS = 2
    ROUND_COMPONENTS = 4
    parameters = [
        ParamFlags(
            "f",
            "Round",
            ["Outline", "Anchros", "Components"],
            ROUND_OUTLINE | ROUND_ANCHORS | ROUND_COMPONENTS,
        )
    ]

    def _execute(self, glyph):
        outline = bool(self.f & self.ROUND_OUTLINE)
        anchors = bool(self.f & self.ROUND_ANCHORS)
        components = bool(self.f & self.ROUND_COMPONENTS)
        glyph.round(None, outline, anchors, components)
