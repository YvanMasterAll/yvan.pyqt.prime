from PyQt5.QtCore import pyqtSignal, Qt, QRectF
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton

class WaterFloatButton(MrxyButton):

    def __init__(self, *args, **kwargs):
        super(WaterFloatButton, self).__init__(*args, **kwargs)

        self.center_pos: QPoint
        self.in_area: bool = False
        self.mwidth: int = 0
        self.radius: int = 0
        self.fore_enabled = False
        self.fore_paddings.left = self.fore_paddings.right = self.radius

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        if self.in_area and not self.pressing and not self.inArea(self.mapFromGlobal(QCursor.pos())):
            self.in_area = False
            super(WaterFloatButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        if self.in_area:
            return super(WaterFloatButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.pressing:
            super(WaterFloatButton, self).mouseReleaseEvent(event)

            if not self.pressing and not self.inArea(event.pos()):
                self.in_area = False
                super(WaterFloatButton, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        is_in = self.inArea(event.pos())

        if not self.in_area and is_in: # 鼠标移入
            self.in_area = True
            super(WaterFloatButton, self).enterEvent(None)
        elif self.in_area and not is_in and not self.pressing: # 鼠标移出
            self.in_area = False
            super(WaterFloatButton, self).leaveEvent(None)

        if self.in_area:
            super(WaterFloatButton, self).mouseMoveEvent(event)

    def resizeEvent(self, event):
        w = self.geometry().width()
        h = self.geometry().height()
        if h >= w * 4: # 宽度为准
            self.radius = w / 4
        else:
            self.radius = h/2
        self.mwidth = (w-self.radius*2)

        return super(WaterFloatButton, self).resizeEvent(event)

    def paintEvent(self, event):
        super(WaterFloatButton, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing,True)

        # 鼠标悬浮进度
        edge_color = QColor(self.hover_bg)
        pro = 0
        if self.hover_progress > 0 or self.press_progress or len(self.waters) > 0:
            if self.water_animation:
                '''
                不用判断 water 是出现还是消失状态
                如果一直悬浮的话，颜色不会变
                而如果是点一下立马移开，文字会出现一种“渐隐渐现”的效果
                '''
                if len(self.waters) > 0:
                    pro = max(self.hover_progress, self.waters[-1].progress)
                else:
                    pro = self.hover_progress
            else:
                math.max(self.hover_progress, self.press_progress)
            edge_color.setAlpha(255 * (100 - pro) / 100)

        # 画边框
        path = QPainterPath()
        if self.show_foreground:
            path = self.getBgPainterPath() # 整体背景

            # 出现动画
            if self.show_ani_appearing and self.show_ani_progress != 100 and self.border_bg.alpha() != 0:
                pw = self.size().width() * self.show_ani_progress / 100
                rect = QRect(0, 0, pw, self.size().height())
                rect_path = QPainterPath()
                rect_path.addRect(rect)
                path &= rect_path

                x = self.show_ani_point.x()
                y = self.show_ani_point.y()
                gen = self.quick_sqrt(x*x + y*y)
                x = - self.water_self.radius * x / gen # 动画起始中心点横坐标 反向
                y = - self.water_self.radius * y / gen # 动画起始中心点纵坐标 反向
            if self.border_bg.alpha() != 0: # 如果有背景，则不进行画背景线条
                painter.setPen(self.border_bg)
                painter.drawPath(path)

        # 画文字
        if (self.self_enabled or self.fore_enabled) and self.text != '':
            rect = QRect(QPoint(0,0), self.size())
            color: QColor
            if pro:
                if self.auto_text_color:
                    aim_color = QColor(0, 0, 0) if self.isLightColor(self.hover_bg) else QColor(255, 255, 255)
                    color = QColor(
                        self.text_color.red() + (aim_color.red() - self.text_color.red()) * pro / 100,
                        self.text_color.green() + (aim_color.green() - self.text_color.green()) * pro / 100,
                        self.text_color.blue() + (aim_color.blue() - self.text_color.blue()) * pro / 100,
                        255)
                painter.setPen(color)
            else:
                color = self.text_color
                color.setAlpha(255)
            painter.setPen(color)
            if self.font_size > 0:
                font = painter.font()
                font.setPointSize(self.font_size)
                painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, self.text)

    def getBgPainterPath(self):
        path1 = QPainterPath()
        path2 = QPainterPath()
        path3 = QPainterPath()
        w = self.size().width()
        h = self.size().height()

        mrect = QRectF(w/2-self.mwidth/2, h/2-self.radius, self.mwidth, self.radius*2)
        path1.addRect(mrect)

        o1 = QPoint(w/2-self.mwidth/2, h/2)
        o2 = QPoint(w/2+self.mwidth/2, h/2)
        path2.addEllipse(o1.x()-self.radius, o1.y()-self.radius, self.radius*2, self.radius*2)
        path3.addEllipse(o2.x()-self.radius, o2.y()-self.radius, self.radius*2, self.radius*2)

        return path1 | path2 | path3

    def getWaterPainterPath(self, water):
        path = MrxyButton.getWaterPainterPath(self, water) & self.getBgPainterPath()
        return path

    def inArea(self, point):
        w = self.size().width()
        h = self.size().height()
        o1 = QPoint(w/2-self.mwidth/2, h/2)
        o2 = QPoint(w/2+self.mwidth/2, h/2)
        mrect = QRect(w/2-self.mwidth/2, h/2-self.radius, self.mwidth, self.radius*2)

        if mrect.contains(point):
            return True
        if (point-o1).manhattanLength() <= self.radius or \
                (point-o2).manhattanLength() <= self.radius:
            return True
        return False
