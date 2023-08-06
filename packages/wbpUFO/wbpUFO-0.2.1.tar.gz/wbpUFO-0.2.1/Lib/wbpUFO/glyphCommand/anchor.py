"""
anchor
===============================================================================

Glyph Commands related to glyph anchors
"""
import wx

from wbDefcon import Anchor, Color, Glyph

from .base import GlyphCommand
from .parameter import (
    ParamBoolRequired,
    ParamStrRequired,
    ParamColour,
    ParamIntRequired,
)


class AddAnchorCommand(GlyphCommand):
    name = "Add anchor"
    parameters = [
        ParamIntRequired("x", "Horizontal position (x)", 0),
        ParamIntRequired("y", "Vertical position (y)", 0),
        ParamStrRequired("n", "Name"),
        ParamColour("c", "Colour", wx.WHITE),
        ParamBoolRequired("r", "Replace existing anchor (by name)", False),
    ]

    def _execute(self, glyph: Glyph):
        for anchor in glyph.anchors:
            if anchor.name == self.n:
                if self.r:
                    anchor.holdNotifications()
                    anchor.x = self.x
                    anchor.y = self.y
                    if self.c != wx.WHITE:
                        anchor.color = Color.from_wx(self.c)
                    anchor.releaseHeldNotifications()
                return
        anchor = Anchor(anchorDict=dict(name=self.n, x=self.x, y=self.y))
        if self.c != wx.WHITE:
            anchor.color = Color.from_wx(self.c)
        glyph.appendAnchor(anchor)


class RemoveAnchorCommand(GlyphCommand):
    name = "Remove anchor (by name)"
    parameters = [ParamStrRequired("n", "Name")]

    def _execute(self, glyph: Glyph):
        for anchor in reversed(glyph.anchors):
            if anchor.name == self.n:
                glyph.removeAnchor(anchor)


class ClearAnchorCommand(GlyphCommand):
    name = "Clear all anchors"

    def _execute(self, glyph: Glyph):
        glyph.clearAnchors()
