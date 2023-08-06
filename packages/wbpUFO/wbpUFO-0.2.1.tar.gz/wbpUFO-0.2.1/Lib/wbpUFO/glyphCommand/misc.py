"""
misc
===============================================================================

Misc Glyph Commands 
"""
import logging

import wx

from wbDefcon import Color

from .base import GlyphCommand
from .parameter import (
    ParamBoolRequired,
    ParamColour,
    ParamEnumeration,
    ParamStrRequired,
)

log = logging.getLogger(__name__)


class NoteCommand(GlyphCommand):
    name = "Note"
    ADD = 0
    REPLACE = 1
    parameters = [
        ParamStrRequired("t", "Text"),
        ParamEnumeration("m", "Mode", ["Add to note", "Replace note"], ADD),
    ]

    def _execute(self, glyph):
        if glyph.note and self.m == self.ADD:
            glyph.note = glyph.note.strip() + "\n" + self.t
            print("text added")
        else:
            glyph.note = self.t
            print("text set")


class SkipExportCommand(GlyphCommand):
    name = "Skip export"
    parameters = [ParamBoolRequired("s", "Skip", True)]

    def _execute(self, glyph):
        skipExportGlyphs = glyph.font.lib.get("public.skipExportGlyphs", [])
        if self.s:
            if glyph.name in skipExportGlyphs:
                return
            skipExportGlyphs.append(glyph.name)
        else:
            if glyph.name in skipExportGlyphs:
                skipExportGlyphs.remove(glyph.name)
            else:
                return
        glyph.font.lib["public.skipExportGlyphs"] = skipExportGlyphs


class MarkCommand(GlyphCommand):
    name = "Mark glyph"
    parameters = [ParamColour("c", "Colour", wx.WHITE)]

    def _execute(self, glyph):
        if self.c == wx.WHITE:
            glyph.markColor = None
        else:
            glyph.markColor = Color.from_wx(self.c)
