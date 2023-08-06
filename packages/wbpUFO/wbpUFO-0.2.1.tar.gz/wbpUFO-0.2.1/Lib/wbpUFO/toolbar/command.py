"""
command
===============================================================================
"""
import logging
from functools import wraps

import wx
from booleanOperations import BooleanOperationManager as Boolean
from wbDefcon import Glyph
from wx import aui

from ..glyphCommand.commandListDialog import CommandListDialog
from ..view.font import UfoFontView
from ..view.glyph import UfoGlyphView

log = logging.getLogger(__name__)


def holdFontNotifications(func):
    """Decorator for glyph commands"""

    @wraps(func)
    def wrapper(*args, **kwds):
        glyph = None
        font = None
        if args:
            glyph = args[0]
        if not isinstance(glyph, Glyph):
            glyph = kwds.get("glyph")
        log.debug("holdFontNotifications %r", glyph)
        if glyph and glyph.font:
            font = glyph.font
            font.holdNotifications()
        result = func(*args, **kwds)
        if font:
            font.releaseHeldNotifications()
        return result

    return wrapper


@holdFontNotifications
def remove_overlap(glyph):
    contours = [c for c in glyph]
    glyph.disableNotifications()
    glyph.undoManager.saveState()
    Boolean.union([c for c in glyph], glyph.getPointPen())
    for contour in contours:
        glyph.removeContour(contour)
    glyph.round(roundAnchors=False, roundComponents=False)
    glyph.enableNotifications()
    glyph.postNotification("Glyph.ContoursChanged")


@holdFontNotifications
def contourDirectionPS(glyph):
    glyph.correctContourDirection()


@holdFontNotifications
def contourDirectionTT(glyph):
    glyph.correctContourDirection(trueType=True)


class GlyphCommandToolbar(aui.AuiToolBar):
    commands = (remove_overlap, contourDirectionPS, contourDirectionTT)

    def __init__(self, parent):
        id = wx.ID_ANY
        pos = wx.DefaultPosition
        size = wx.DefaultSize
        style = (
            wx.aui.AUI_TB_HORZ_LAYOUT | wx.aui.AUI_TB_PLAIN_BACKGROUND | wx.NO_BORDER
        )
        aui.AuiToolBar.__init__(self, parent, id, pos, size, style)
        self.SetToolBitmapSize(wx.Size(16, 16))
        self.appendTool("Remove Overlap", "MERGE_CONTOURS", "Merge contours", 0)
        self.AddSeparator()
        self.appendTool("Flip Horizontal", "FLIP_HORIZONTAL", "Flip horizontal")
        self.appendTool("Flip Vertical", "FLIP_VERTICAL", "Flip vertical")
        self.AddSeparator()
        self.appendTool(
            "Set PS Direction", "DIRECTION_PS", "Set PostScript contour direction", 1
        )
        self.appendTool(
            "Set TT Direction", "DIRECTION_TT", "Set TrueType contour direction", 2
        )
        self.AddSeparator()
        self.appendTool(
            "Command List",
            "COMMAND_LIST",
            "Execute Command List",
            handler=self.on_command_list,
        )

    @property
    def app(self):
        return wx.GetApp()

    @staticmethod
    def bitmap(name):
        return wx.ArtProvider.GetBitmap(name, wx.ART_TOOLBAR)

    def appendTool(self, label, bitmapName, helpText, commandIndex=-1, handler=None):
        if not handler:
            handler = self.on_Tool
        tool = self.AddTool(
            wx.ID_ANY, label, self.bitmap(bitmapName), helpText, wx.ITEM_NORMAL
        )
        tool.SetUserData(commandIndex)
        self.Bind(wx.EVT_TOOL, handler, tool)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_Tool, tool)
        return tool

    def on_Tool(self, event):
        tool = self.FindTool(event.Id)
        i = tool.GetUserData()
        if isinstance(i, int) and i >= 0:
            command = self.commands[i]
            view = self.app.documentManager.currentView
            if isinstance(view, UfoFontView):
                font = self.app.documentManager.currentView.font
                for glyph in font.selectedGlyphs:
                    command(glyph)
            elif isinstance(view, UfoGlyphView):
                command(view.glyph)
        else:
            label = self.GetToolLabel(event.Id)
            wx.LogWarning(f'Command "{label}" not yet implemented')

    def on_update_Tool(self, event):
        view = self.app.documentManager.currentView
        if view and view.document:
            if isinstance(view, UfoFontView):
                font = view.document.font
                if font and len(font.selectedGlyphNames) > 0:
                    event.Enable(True)
                else:
                    event.Enable(False)
            elif isinstance(view, UfoGlyphView):
                event.Enable(True)
            else:
                event.Enable(False)
        else:
            event.Enable(False)

    def on_command_list(self, event):
        with CommandListDialog() as dialog:
            view = self.app.documentManager.currentView
            if view and view.document:
                if isinstance(view, UfoFontView):
                    dialog.choice_target.SetSelection(1)  # selected glyphs
                elif isinstance(view, UfoGlyphView):
                    dialog.choice_target.SetSelection(0)  # current glyph
                if dialog.ShowModal() == wx.ID_OK:
                    commandList = dialog.commandList
                    if commandList:
                        dialog.executeCommandList()
