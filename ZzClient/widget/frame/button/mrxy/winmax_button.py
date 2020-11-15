from PyQt5.QtCore import pyqtSignal, Qt
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton, NolinearType

class WinMaxButton(MrxyButton):
    def __init__(self, *args, **kwargs):
        super(WinMaxButton, self).__init__(*args, **kwargs)

        self.setUnifyGeomerey(True)

    def paintEvent(self, event):
        super(WinMaxButton, self).paintEvent(event)

        if not self.show_foreground:
            return  # 不显示前景

        w = self._w
        h = self._h
        dx = self.offset_pos.x()
        dy = self.offset_pos.y()
        r = QRect()
        if self.click_ani_appearing or self.click_ani_disappearing:
            pro = self.click_ani_progress / 800.0
            r = QRect(
                        self._l+(w/3+dx) - (w/3+dx)*pro,
                        self._t+(h/3+dy) - (h/3+dy)*pro,
                        w/3 + (w*2/3)*pro,
                        h/3 + (h*2/3)*pro
                        )
        else:
            r = QRect(self._l+w/3+dx, self._t+h/3+dy, w/3, h/3)

        painter = QPainter(self)
        painter.setPen(QPen(self.icon_color))
        painter.drawRect(r)