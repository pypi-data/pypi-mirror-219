"""
base
===============================================================================

Base classes related to drawing on the cnavas of the glyph editor
"""

import logging
from math import cos, radians, sin

import wx
from fontTools.misc.transform import Identity
from wbBase.tools import get_wxBrush, get_wxFont, get_wxPen

log = logging.getLogger(__name__)

try:
    from math import dist
except ImportError:
    # backport for python 3.7
    from math import sqrt

    def dist(p0, p1):
        dx = abs(p0[0] - p1[0])
        dy = abs(p0[1] - p1[1])
        return sqrt(dx**2 + dy**2)


# -------------------------------------------------------------------------
# Base classes
# -------------------------------------------------------------------------


class BasePlane:
    """
    Base class for all Plain objects
    """

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.canvas = None

    def __repr__(self):
        return f'<{self.__class__.__name__}: "{self.name}">'

    @property
    def transform(self):
        return self.parent.transform

    def draw(self, gc):
        """
        should be overridden by subclass
        """
        raise NotImplementedError


class DrawingPlane(BasePlane):
    """
    Base class to represent DrawingPlane on Canvas
    """

    lockedDflt = False

    def __init__(self, parent, name):
        super(DrawingPlane, self).__init__(parent, name)
        self._locked = self.lockedDflt

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = bool(value)

    @property
    def font(self):
        return self.parent.parent.font

    def getInactiveColour(self, colour):
        return wx.Colour(
            colour.red, colour.green, colour.blue, self.parent.inactiveAlpha
        )

    def getInactiveBrush(self, brush):
        return get_wxBrush(self.getInactiveColour(brush.Colour), brush.Style)

    def getInactivePen(self, pen):
        return get_wxPen(self.getInactiveColour(pen.Colour), pen.Width, pen.Style)

    def hitTest(self, x, y):
        """
        may be overridden by subclass
        Coordinates x, y are in canvas/font units
        """
        return None

    def Refresh(self):
        self.parent.Refresh()


class DrawingPlaneStack(BasePlane):
    """
    Collection of DrawingPlane objects
    """

    childType = DrawingPlane
    activeDflt = False
    inactiveAlphaDflt = 128

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self._active = self.activeDflt
        self._inactiveAlpha = self.inactiveAlphaDflt
        self.canvas = parent
        self._drawingPlanes = []
        self._hitTestOrder = None

    def __iter__(self):
        return iter(self._drawingPlanes)

    def __getitem__(self, key):
        for plane in self._drawingPlanes:
            if plane.name == key:
                return plane
        raise KeyError

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        newVal = bool(value)
        if newVal != self._active:
            self._active = newVal
            self.canvas.Refresh()

    @property
    def inactiveAlpha(self):
        return self._inactiveAlpha

    @property
    def hitTestOrder(self):
        if self._hitTestOrder is None:
            return [p.name for p in self._drawingPlanes]
        return self._hitTestOrder

    def addPlane(self, plane):
        assert issubclass(plane, self.childType)
        newPlane = plane(self)
        newPlane.canvas = self.parent
        self._drawingPlanes.append(newPlane)

    def keys(self):
        return [p.name for p in self._drawingPlanes]

    def get(self, name, default=None):
        for plane in self._drawingPlanes:
            if plane.name == name:
                return plane
        return default

    def draw(self, gc):
        for plane in [p for p in self._drawingPlanes if p.visible]:
            plane.draw(gc)


class GuidelinePlaneMixin:
    """
    Mixin class for font and glyph level guidelines
    """

    LabelFont = get_wxFont(pointSize=7, faceName="Small Fonts")
    LabelPen = wx.TRANSPARENT_PEN
    LabelBrush = get_wxBrush(wx.Colour(230, 230, 240, 200))

    def drawGuidelines(self, gc, guidelines):
        gc.SetFont(self.LabelFont, wx.BLACK)
        d = 3  # distace between point and label
        s = 2  # space around text
        for guideline in guidelines:
            gc.SetBrush(wx.TRANSPARENT_BRUSH)
            line = ((-8000, 0), (8000, 0))
            if guideline.angle is None:
                if guideline.x is None:
                    guideline_x = 0
                    guideline_y = guideline.y
                    guideline_angle = 0
                elif guideline.y is None:
                    guideline_x = guideline.x
                    guideline_y = 0
                    guideline_angle = 90
            else:
                guideline_x = guideline.x
                guideline_y = guideline.y
                guideline_angle = guideline.angle
            line = (
                Identity.translate(guideline_x, guideline_y)
                .rotate(radians(guideline_angle))
                .transformPoints(line)
            )
            (x0, y0), (x1, y1) = self.transform.transformPoints(line)
            x0 = round(x0)
            y0 = round(y0)
            x1 = round(x1)
            y1 = round(y1)
            if guideline.selected:
                gc.SetPen(self.selected_pen)
                gc.StrokeLine(x0, y0, x1, y1)
            gc.SetPen(guideline.wxPen)
            gc.StrokeLine(x0, y0, x1, y1)
            x, y = self.transform.transformPoint((guideline_x, guideline_y))
            x = round(x)
            y = round(y)
            gc.DrawEllipse(x - 3, y - 3, 6, 6)
            gc.SetBrush(self.LabelBrush)
            gc.SetPen(self.LabelPen)
            text = ""
            if guideline.name:
                text += guideline.name
            if guideline_angle in (0.0, 180.0, -180):
                if text:
                    text += f": {guideline_y:0.0f}"
                else:
                    text = f"{guideline_y:0.0f}"
            elif guideline_angle in (90.0, 270.0, -90.0):
                if text:
                    text += f": {guideline_x:0.0f}"
                else:
                    text = f"{guideline_x:0.0f}"
            else:
                if text:
                    text += f": ({guideline_x:0.0f}, {guideline_y:0.0f}) {guideline_angle:0.0f}°"
                else:
                    text = f"({guideline_x:0.0f}, {guideline_y:0.0f}) {guideline_angle:0.0f}°"
            w, h = gc.GetTextExtent(text)
            w = round(w) + 2 * s
            h = round(h) + 2 * s
            x, y = self.transform.transformPoint((guideline_x, guideline_y))
            gc.DrawRoundedRectangle(x - w - d, y + d, w, h, d)
            gc.DrawText(text, x - w, y + d + s - 1)

    def hitTestGuidelines(self, x, y, guidelines):
        delta = self.canvas.screenToCanvasXrel(4)
        for guideline in guidelines:
            distance = dist((x, y), (guideline.x, guideline.y))
            if distance <= delta:
                return guideline
            if guideline.angle in (0, 180) or (
                guideline.angle is None and guideline.x in (0, None)
            ):
                if abs(y - guideline.y) <= delta:
                    return guideline
                continue
            if guideline.angle in (90, 270) or (
                guideline.angle is None and guideline.y in (0, None)
            ):
                if abs(x - guideline.x) <= delta:
                    return guideline
                continue
            for a in (guideline.angle, guideline.angle + 180):
                angle_rad = radians(a)
                p_guide = guideline.x + distance * cos(
                    angle_rad
                ), guideline.y + distance * sin(angle_rad)
                if dist(p_guide, (x, y)) <= delta:
                    return guideline
