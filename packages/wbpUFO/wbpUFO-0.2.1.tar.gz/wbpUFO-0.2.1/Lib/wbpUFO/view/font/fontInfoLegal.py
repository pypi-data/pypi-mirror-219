
import logging
import wx
from .fontInfoLegalUI import FontInfoLegalUI
log = logging.getLogger(__name__)

class FontInfoLegal(FontInfoLegalUI):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.BORDER_NONE | wx.TAB_TRAVERSAL,
    ):
        super().__init__(parent, id, pos, size, style, name="FontInfoLegal")
        self.SetScrollRate(5, 5)

    def __repr__(self):
        return f"<{self.__class__.__name__} of {self.Parent}>"
