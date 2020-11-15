import math
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton

ANI_STEP_3 = 40

class PointMenuButton(MrxyButton):

    def __init__(self, *args, **kwargs):
        super(PointMenuButton, self).__init__(*args, **kwargs)

        self.setUnifyGeomerey(True)
        self.radius = 2
        self.setClickAniDuration(600)

    def mousePressEvent(self, event):
        self.slotClicked()

        return super(PointMenuButton, self).mousePressEvent(event)

    def paintEvent(self, event):
        super(PointMenuButton, self).paintEvent(event)

        if not self.show_foreground:
            return # 不显示前景

        w = self._w
        h = self._h
        l = self._l+w/3
        t = self._t+h/3
        r = w*2/3
        b = h*2/3
        mx = self._l+w/2+self.offset_pos.x()
        my = self._t+h/2+self.offset_pos.y()

        # 画笔
        painter = QPainter(self)
        painter.setPen(QPen(self.icon_color))
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self.click_ani_appearing:
            midx = (l+r) / 2
            move_radius = (b-t)*3/4/2
            path = QPainterPath()

            # 第一个点
            if self.click_ani_progress <= ANI_STEP_3: # 画圈
                tp = self.click_ani_progress / ANI_STEP_3
                o = QPoint(midx, t + move_radius)
                p = QPoint(o.x() - move_radius * math.sin(math.pi * tp), o.y() - move_radius * math.cos(math.pi * tp))
                path.addEllipse(p.x()-self.radius, p.y()-self.radius, self.radius<<1, self.radius<<1)
            elif self.click_ani_progress <= ANI_STEP_3*2: # 静止
                o = QPoint(midx, t + move_radius*2)
                path.addEllipse(o.x()-self.radius, o.y()-self.radius, self.radius<<1, self.radius<<1)
            else: # 下移
                tp = (self.click_ani_progress-ANI_STEP_3*2) / (100.0 - ANI_STEP_3*2)
                p = QPoint(midx, b-(1-tp)*(b-t)/6)
                path.addEllipse(p.x()-self.radius, p.y()-self.radius, self.radius<<1, self.radius<<1)

            # 第二个点
            if self.click_ani_progress <= (100-ANI_STEP_3*2): # 静止
                o = QPoint(midx, (t+b)/2)
                path.addEllipse(o.x()-self.radius, o.y()-self.radius, self.radius<<1, self.radius<<1)
            else: # 不动
                o = QPoint(midx, (t+b)/2)
                path.addEllipse(o.x()-self.radius, o.y()-self.radius, self.radius<<1, self.radius<<1)

            # 第三个点
            if self.click_ani_progress <= ANI_STEP_3: # 静止
                o = QPoint(midx, b)
                path.addEllipse(o.x()-self.radius, o.y()-self.radius, self.radius<<1, self.radius<<1)
            elif self.click_ani_progress > ANI_STEP_3 and self.click_ani_progress <= ANI_STEP_3*2: # 画圈
                tp = (self.click_ani_progress-ANI_STEP_3) / ANI_STEP_3
                o = QPoint(midx, b - move_radius)
                p =QPoint(o.x() + move_radius * math.sin(math.pi * tp), o.y() + move_radius * math.cos(math.pi * tp))
                path.addEllipse(p.x()-self.radius, p.y()-self.radius, self.radius<<1, self.radius<<1)
            else: # 上移
                tp = (self.click_ani_progress-ANI_STEP_3*2) / (100-ANI_STEP_3*2)
                p = QPoint(midx, t+(1-tp)*(b-t)/6)
                path.addEllipse(p.x()-self.radius, p.y()-self.radius, self.radius<<1, self.radius<<1)

            painter.fillPath(path, QColor(self.icon_color))
        else:
            path = QPainterPath()
            path.addEllipse((l+r)/2-self.radius, t-self.radius, self.radius<<1, self.radius<<1)
            path.addEllipse((l+r)/2-self.radius, (t+b)/2-self.radius, self.radius<<1, self.radius<<1)
            path.addEllipse((l+r)/2-self.radius, b-self.radius, self.radius<<1, self.radius<<1)
            painter.fillPath(path, QColor(self.icon_color))

