import math
from PyQt5.QtCore import QPoint, QRect, QRectF
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton


class WaterCircleButton(MrxyButton):

    def __init__(self, *args, **kwargs):
        super(WaterCircleButton, self).__init__(*args, **kwargs)

        self.center_pos = QPoint()
        self.in_circle = False
        self.radius = 16

    @classmethod
    def by_icon(cls, icon, parent):
        instance = super(WaterCircleButton, cls).by_icon(icon, parent)
        instance.in_circle = False
        instance.radius = 16
        return instance

    @classmethod
    def by_pixmap(cls, pixmap, parent):
        instance = super(WaterCircleButton, cls).by_pixmap(pixmap, parent)
        instance.in_circle = False
        instance.radius = 16
        return instance

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        if self.in_circle and not self.pressing and not self.inArea(self.mapFromGlobal(QCursor.pos())):
            self.in_circle = False
            super(WaterCircleButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        if self.in_circle or (not self.hovering and self.inArea(event.pos())):
            return super(WaterCircleButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.pressing:
            super(WaterCircleButton, self).mouseReleaseEvent(event)

            if self.leave_after_clicked or (not self.inArea(event.pos()) and not self.pressing): # 鼠标移出
                self.in_circle = False
                super(WaterCircleButton, self).leaveEvent(event)

    def mouseMoveEvent(self, event):
        is_in = self.inArea(event.pos())

        if is_in and not self.in_circle: # 鼠标移入
            self.in_circle = True
            super(WaterCircleButton, self).enterEvent(event)
        elif not is_in and self.in_circle and not self.pressing: # 鼠标移出
            self.in_circle = False
            super(WaterCircleButton, self).leaveEvent(None)

        if self.in_circle:
            super(WaterCircleButton, self).mouseMoveEvent(event)

    def resizeEvent(self, event):
        self.center_pos = self.geometry().center() - self.geometry().topLeft()
        self.radius = min(self.size().width(), self.size().height())/ 2

        return super(WaterCircleButton, self).resizeEvent(event)

    def getBgPainterPath(self):
        path = QPainterPath()
        w = self.size().width()
        h = self.size().height()
        rect = QRectF(w/2-self.radius, h/2-self.radius, self.radius*2, self.radius*2)
        path.addEllipse(rect)
        return path

    def getWaterPainterPath(self, water):
        path = MrxyButton.getWaterPainterPath(self, water) & self.getBgPainterPath()
        return path

    def simulateStatePress(self, s):
        self.in_circle = True
        MrxyButton.simulateStatePress(s)
        self.in_circle = False

    def inArea(self, point):
        return (point - self.center_pos).manhattanLength() <= self.radius
