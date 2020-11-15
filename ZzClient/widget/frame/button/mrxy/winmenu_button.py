from PyQt5.QtCore import pyqtSignal, Qt
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton, NolinearType

class WinMenuButton(MrxyButton):
    def __init__(self, *args, **kwargs):
        super(WinMenuButton, self).__init__(*args, **kwargs)

        self.setUnifyGeomerey(True)

    def paintEvent(self, event):
        super(WinMenuButton, self).paintEvent(event)

        if not self.show_foreground:
            return  # 不显示前景

        w = self._w
        h = self._h
        dx = self.offset_pos.x()
        dy = self.offset_pos.y()

        painter = QPainter(self)
        painter.setPen(QPen(self.icon_color))

        if self.click_ani_appearing:
            pro = self.click_ani_progress / 100.0
            if not self.getState():
                pro = 1 - pro

            len = w/3
            l = self._l+w/3
            r = self._l+w*2/3
            t = self._t+h/3 + pro*h/3
            painter.drawLine(QPoint(l+dx/4,t+dy/4), QPoint(r+dx/4,t+dy/4))

            l = self._l+w/3+pro*w/24
            r = self._l+w*2/3-pro*w/24
            t = self._t+w/2+pro*h*5/18
            painter.drawLine(QPoint(l+dx/2,t+dy/2), QPoint(r+dx/2,t+dy/2))

            l = self._l+w/3+pro*w/12
            r = self._l+w*2/3-pro*w/12
            t = self._t+w*2/3+pro*h*2/9
            painter.drawLine(QPoint(l+dx,t+dy), QPoint(r+dx,t+dy))

            '''
            half_len = w/6 # self.quick_sqrt(w/3*w/3 + h/3*h/3) / 2 # 长度
            painter.setRenderHint(QPainter.Antialiamath.sing, True)
    
            # 第一个点
            mx = w/2
            my = h/3 + pro*h/6
            angle = pro*PI*5/4
            sx = mx - half_len*math.cos(angle)
            sy = my - half_len*math.sin(angle)
            ex = mx + half_len*math.cos(angle)
            ey = my + half_len*math.sin(angle)
            painter.drawLine(QPoint(sx,sy), QPoint(ex,ey))
    
            # 第三个点
            mx = w/2
            my = h*2/3 - pro*h/6
            angle = pro*PI*3/4
            sx = mx - half_len*math.cos(angle)
            sy = my - half_len*math.sin(angle)
            ex = mx + half_len*math.cos(angle)
            ey = my + half_len*math.sin(angle)
            painter.drawLine(QPoint(sx,sy), QPoint(ex,ey))
    
            # 第二个点(设置透明度)
            mx = w/2
            my = h/2
            angle = pro*PI
            sx = mx - half_len*math.cos(angle)
            sy = my - half_len*math.sin(angle)
            ex = mx + half_len*math.cos(angle)
            ey = my + half_len*math.sin(angle)
            color = QColor(self.icon_color)
            color.setAlpha(color.alpha() * (1-pro))
            painter.setPen(QPen(color))
            painter.drawLine(QPoint(sx,sy), QPoint(ex,ey))
            '''
        elif self.getState():
            painter.drawLine(self._l+w/3+dx/4, self._t+h*2/3+dy/4, w*2/3+dx/4,h*2/3+dy/4)
            painter.drawLine(self._l+w/3+w/24+dx/2, self._t+h*7/9+dy/2, w*2/3-w/24+dx/2, h*7/9+dy/2)
            painter.drawLine(self._l+w/3+w/12+dx, self._t+h*8/9+dy, w*2/3-w/12+dx, h*8/9+dy)

            '''
            painter.drawLine(QPoint(0.39*w, 0.39*h), QPoint(0.61*w, 0.61*h))
            painter.drawLine(QPoint(0.39*w, 0.61*h), QPoint(0.61*w, 0.39*h))
            '''
        else:
            painter.drawLine(QPoint(self._l+w/3+dx/4,self._t+h/3+dy/4), QPoint(self._l+w*2/3+dx/4,self._t+h/3+dy/4))
            painter.drawLine(QPoint(self._l+w/3+dx/2,self._t+h/2+dy/2), QPoint(self._l+w*2/3+dx/2,self._t+h/2+dy/2))
            painter.drawLine(QPoint(self._l+w/3+dx,self._t+h*2/3+dy), QPoint(self._l+w*2/3+dx,self._t+h*2/3+dy))

    def slotClicked(self):
        if self.getState():
            self.setState(False)
        else:
            self.setState(True)
        return MrxyButton.slotClicked(self)
