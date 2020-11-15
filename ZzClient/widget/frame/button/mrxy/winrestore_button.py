from PyQt5.QtCore import pyqtSignal, Qt
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton, NolinearType

class WinRestoreButton(MrxyButton):
    def __init__(self, *args, **kwargs):
        super(WinRestoreButton, self).__init__(*args, **kwargs)

        self.setUnifyGeomerey(True)

    def paintEvent(self, event):
        super(WinRestoreButton, self).paintEvent(event)

        if not self.show_foreground:
            return # 不显示前景

        # 画出现一角的矩形
        w = self._w
        h = self._h
        dx = self.offset_pos.x()
        dy = self.offset_pos.y()
        br = QRect()
        if self.click_ani_appearing or self.click_ani_disappearing:
            pro = self.click_ani_progress / 800.0
            br = QRect(
                self._l+(w/3+dx) - (w/3+dx)*pro,
                self._t+(h/3+dy) - (h/3+dy)*pro,
                w/3 + (w*2/3)*pro,
                h/3 + (h*2/3)*pro
                )
        else:
            br = QRect(self._l+w/3+dx, self._t+h/3+dy, w/3, h/3)

        # 画原来的矩形
        painter = QPainter(self)
        painter.setPen(QPen(self.icon_color))
        painter.drawRect(br)

        dx /= 2
        dy /= 2
        l = self._l+w*4/9+dx
        t = self._t+h*2/9+dy
        r = self._l+w*7/9+dx
        b = self._t+h*5/9+dy
        if self.click_ani_appearing or self.click_ani_disappearing:
            pro = self.click_ani_progress / 800.0
            l -= l*pro
            t -= t*pro
            r += (w-r)*pro
            b += (h-b)*pro
        topLeft = QPoint(l, t)
        topRight = QPoint(r, t)
        bottomLeft = QPoint(l, b)
        bottomRight = QPoint(r, b)
        points: list = []

        '''
        两个矩形一样大的，所以运行的时候，需要有三大类：
        1、完全重合（可以视为下一点任意之一）
        2、有一个点落在矩形内（4种情况）
        3、完全不重合
        根据3大类共6种进行判断
        '''
        if br.topLeft() == topLeft:
            points.append(topLeft)
            points.append(topRight)
            points.append(bottomRight)
            points.append(bottomLeft)
            points.append(topLeft)
        elif br.contains(topLeft): # 左上角在矩形内
            points.append(QPoint(br.right()+1, t))
            points.append(topRight)
            points.append(bottomRight)
            points.append(bottomLeft)
            points.append(QPoint(l, br.bottom()+1))
        elif br.contains(topRight): # 右上角在矩形内
            points.append(QPoint(r, br.bottom()+1))
            points.append(bottomRight)
            points.append(bottomLeft)
            points.append(topLeft)
            points.append(QPoint(br.left(), t))
        elif br.contains(bottomLeft): # 左下角在矩形内（默认）
            points.append(QPoint(l, br.top()))
            points.append(topLeft)
            points.append(topRight)
            points.append(bottomRight)
            points.append(QPoint(br.right()+1, b))
        elif br.contains(bottomRight): # 右下角在矩形内
            points.append(QPoint(br.left(), b))
            points.append(bottomLeft)
            points.append(topLeft)
            points.append(topRight)
            points.append(QPoint(r, br.top()))
        else: # 没有重合
            points.append(topLeft)
            points.append(topRight)
            points.append(bottomRight)
            points.append(bottomLeft)
            points.append(topLeft)

        if len(points) > 1:
            path = QPainterPath()
            path.moveTo(points[0])
            for point in points:
                path.lineTo(point)
            color = QColor(self.icon_color)
            color.setAlpha(color.alpha()*0.8)
            painter.setPen(QPen(color))
            painter.drawPath(path)

