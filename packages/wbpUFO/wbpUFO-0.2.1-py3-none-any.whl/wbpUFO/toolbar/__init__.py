import wx
from wx import aui


class BaseToolbar(aui.AuiToolBar):
    itemType = wx.ITEM_NORMAL
    def __init__(self, parent, name=None):
        id = wx.ID_ANY
        pos = wx.DefaultPosition
        size = wx.DefaultSize
        style = (
            wx.aui.AUI_TB_HORZ_LAYOUT | wx.aui.AUI_TB_PLAIN_BACKGROUND | wx.NO_BORDER
        )
        super().__init__(parent, id, pos, size, style)
        if isinstance(name, str):
            self.Name = name
        self.SetToolBitmapSize(wx.Size(16, 16))

    @property
    def app(self):
        return wx.GetApp()

    @property
    def currentView(self):
        return self.app.documentManager.currentView

    @staticmethod
    def bitmap(name):
        return wx.ArtProvider.GetBitmap(name, wx.ART_TOOLBAR)

    def appendTool(
        self, label, bitmapName, helpText=wx.EmptyString, commandIndex=-1, kind=None
    ):
        if not helpText:
            helpText = label
        if kind is None:
            kind = self.itemType
        tool = self.AddTool(
            toolId=wx.ID_ANY,
            label=label,
            bitmap=self.bitmap(bitmapName),
            short_help_string=helpText,
            kind=kind,
        )
        tool.SetUserData(commandIndex)
        self.Bind(wx.EVT_TOOL, self.on_Tool, tool)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_Tool, tool)
        return tool

    def on_Tool(self, event):
        event.Skip()

    def on_update_Tool(self, event):
        event.Skip()
