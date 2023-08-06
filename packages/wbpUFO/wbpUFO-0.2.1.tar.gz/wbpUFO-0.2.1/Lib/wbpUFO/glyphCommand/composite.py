"""
composite
===============================================================================

Glyph Commands related to composites
"""
# from glyphConstruction import (
#     GlyphConstructionBuilder,
#     ParseGlyphConstructionListFromString,
# )

from .base import GlyphCommand
from .parameter import ParamFilepathRequired


class DecomposeCommand(GlyphCommand):
    name = "Decompose"

    def _execute(self, glyph):
        glyph.decomposeAllComponents()


class ClearComponentsCommand(GlyphCommand):
    name = "Clear all components"

    def _execute(self, glyph):
        glyph.clearComponents()


# class UpdateCompositeCommand(GlyphCommand):
#     name = "Update composite"
#     parameters = [ParamFilepathRequired("c", "Glyph construction file", default="")]

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._constructions = None

#     @property
#     def constructions(self):
#         if not self._constructions:
#             constructions = ParseGlyphConstructionListFromString(self.c)
#             self._constructions = dict(
#                 (c.split("=", 1)[0].strip(), c) for c in constructions
#             )
#         return self._constructions

#     def _execute(self, glyph):
#         if glyph.components and glyph.name in self.constructions:
#             name = glyph.name
#             font = glyph.font
#             constructionGlyph = GlyphConstructionBuilder(self.constructions[name], font)
#             # newGlyph = font.newGlyph(name)
#             glyph.clearComponents()
#             constructionGlyph.draw(glyph.getPen())
#             glyph.unicode = constructionGlyph.unicode
#             # newGlyph.note = constructionGlyph.note
#             glyph.width = constructionGlyph.width
