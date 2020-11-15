from PyQt5.QtCore import pyqtSignal, Qt
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton

class WinCloseButton(MrxyButton):

    def __init__(self, *args, **kwargs):
        super(WinCloseButton, self).__init__(*args, **kwargs)

        self.setUnifyGeomerey(True)
        self.tr_radius = 0

    def paintEvent(self, event):
        super(WinCloseButton, self).paintEvent(event)

        if not self.show_foreground:
            return  # 不显示前景

        w = self._w
        h = self._h
        l = self._l+w/3
        t = self._t+h/3
        r = w*2/3
        b = h*2/3
        mx = self._l+w/2+self.offset_pos.x()
        my = self._t+h/2+self.offset_pos.y()

        if self.click_ani_appearing or self.click_ani_disappearing:
            pro = self.click_ani_progress / 100.0
            l -= l * pro
            t -= t * pro
            r += (w-r) * pro
            b += (h-b) * pro

        painter = QPainter(self)
        painter.setPen(QPen(self.icon_color))
        painter.setRenderHint(QPainter.Antialiasing, True)
        if self.offset_pos != QPoint(0,0):
            path = QPainterPath()
            path.moveTo(QPoint(l,t))
            path.cubicTo(QPoint(l,t), QPoint(mx,my), QPoint(r,b))
            path.moveTo(QPoint(r,t))
            path.cubicTo(QPoint(r,t), QPoint(mx,my), QPoint(l,b))

            painter.drawPath(path)
        else:
            painter.drawLine(QPoint(l,t), QPoint(r,b))
            painter.drawLine(QPoint(r,t), QPoint(l,b))

    def setTopRightRadius(self, r):
        '''
        针对圆角的设置
        '''
        self.tr_radius = r

    def getBgPainterPath(self):
        if not self.tr_radius:
            return MrxyButton.getBgPainterPath(self)

        path = MrxyButton.getBgPainterPath()
        round_path = QPainterPath()
        round_path.addEllipse(self.width() - self.tr_radius - self.tr_radius, 0, self.tr_radius*2, self.tr_radius*2)
        corner_path = QPainterPath()
        corner_path.addRect(self.width() - self.tr_radius, 0, self.tr_radius, self.tr_radius)
        corner_path -= round_path
        path -= corner_path
        return path

    def getWaterPainterPath(self, water):
        return MrxyButton.getWaterPainterPath(self, water) & WinCloseButton.getBgPainterPath(self)