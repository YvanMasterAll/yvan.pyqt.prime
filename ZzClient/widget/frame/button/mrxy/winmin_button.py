from PyQt5.QtCore import pyqtSignal, Qt
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton, NolinearType

class WinMinButton(MrxyButton):
    def __init__(self, *args, **kwargs):
        super(WinMinButton, self).__init__(*args, **kwargs)

        self.setUnifyGeomerey(True)

    def paintEvent(self, event):
        super(WinMinButton, self).paintEvent(event)

        if not self.show_foreground:
            return # 不显示前景

        w = self._w
        h = self._h
        left = QPoint(self._l+w/3, self._t+h/2)
        right = QPoint(self._l+w*2/3, self._t+h/2)
        mid = QPoint(self._l+w/2+self.offset_pos.x(), self._t+h/2+self.offset_pos.y())

        if self.click_ani_appearing or self.click_ani_disappearing:
            pro = self.click_ani_progress / 800.0
            left.setX(left.x()-left.x() * pro)
            right.setX(right.x()+(w-right.x()) * pro)

        painter = QPainter(self)
        path = QPainterPath()
        path.moveTo(left)
        path.cubicTo(left, mid, right)
        painter.setPen(QPen(self.icon_color))
        if left.y() != mid.y():
            painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPath(path)
