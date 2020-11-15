from PyQt5.QtCore import pyqtSignal, Qt
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton, NolinearType

class WinSidebarButton(MrxyButton):

    def __init__(self, *args, **kwargs):
        super(WinSidebarButton, self).__init__(*args, **kwargs)

        self.setUnifyGeomerey(True)
        self.tl_radius = 0

    def paintEvent(self, event):
        super(WinSidebarButton, self).paintEvent(event)

        if not self.show_foreground:
            return # 不显示前景

        dx = self.offset_pos.x()
        dy = self.offset_pos.y()
        l = self._l + self._w/3+dx
        t = self._t + self._h/3+dy
        w = self._w/3
        h = self._h/3

        painter = QPainter(self)
        painter.setPen(QPen(self.icon_color))
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self.click_ani_appearing:
            pro = self.click_ani_progress / 100.0
            if self.getState():
                pro = 1 - pro
            painter.drawEllipse(l+w/2-w*pro/2, t+h/2-h*pro/2, w*pro, h*pro)

            if self.getState():
                pro = self.getSpringBackProgress(self.click_ani_progress, 50) / 100.0
            else:
                pro = 1 - self.click_ani_progress / 100.0

            l = self._l + self._w/3+dx
            t = self._t + self._h/3+dy
            w = self._w / 3
            h = self._h / 3

            l += w/2.0 - w*pro/2
            t += h/2.0 - h*pro/2
            w *= pro
            h *= pro

            path = QPainterPath()
            path.addEllipse(l, t, w, h)
            painter.fillPath(path, self.icon_color)
        elif self.getState():
            path = QPainterPath()
            path.addEllipse(l, t, w, h)
            painter.fillPath(path, self.icon_color)
        else:
            painter.drawEllipse(l, t, w, h)

    def slotClicked(self):
        if self.getState():
            self.setState(False)
        else:
            self.setState(True)
        return self.slotClicked()

    def setTopLeftRadius(self, r):
        '''
        针对圆角的设置
        '''
        self.tl_radius = r

    def getBgPainterPath(self):
        if not self.tl_radius:
            return MrxyButton.getBgPainterPath()

        path = MrxyButton.getBgPainterPath()
        round_path = QPainterPath()
        round_path.addEllipse(0, 0, self.tl_radius * 2, self.tl_radius * 2)
        corner_path = QPainterPath()
        corner_path.addRect(0, 0, self.tl_radius, self.tl_radius)
        corner_path -= round_path
        path -= corner_path
        return path

    def getWaterPainterPath(self, water):
        return MrxyButton.getWaterPainterPath(self, water) & WinSidebarButton.getBgPainterPath()