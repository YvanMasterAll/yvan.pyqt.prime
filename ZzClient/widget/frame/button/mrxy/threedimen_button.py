from PyQt5.QtCore import QPoint, QRect, QRectF
from PyQt5.QtGui import QColor, QCursor, QPainterPath
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from widget.frame.button.mrxy.mrxy_button import MrxyButton

AOPER = 10
SHADE = 10

class ThreeDimenButton(MrxyButton):

    def __init__(self, *args, **kwargs):
        super(ThreeDimenButton, self).__init__(*args, **kwargs)

        self.setMouseTracking(True)
        self.in_rect = False
        self.aop_w = self.width() / AOPER
        self.aop_h = self.height() / AOPER

        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setColor(QColor(0x88, 0x88, 0x88, 0x64))
        self.shadow_effect.setBlurRadius(10)
        self.setGraphicsEffect(self.shadow_effect)

        self.setJitterAni(False)

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        if self.in_rect and not self.pressing and not self.inArea(self.mapFromGlobal(QCursor.pos())):
            self.in_rect = False
            super(ThreeDimenButton, self).leaveEvent(None)

        # 不return，因为区域不一样

    def mousePressEvent(self, event):
        # 因为上面可能有控件，所以可能无法监听到 enter 事件
        if not self.in_rect and self.inArea(event.pos()): # 鼠标移入
            self.in_rect = True
            super(ThreeDimenButton, self).enterEvent(event)

        if self.in_rect:
            return super(ThreeDimenButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.pressing:
            super(ThreeDimenButton, self).mouseReleaseEvent(event)

            if self.leave_after_clicked or (not self.inArea(event.pos()) and not self.pressing): # 鼠标移出
                self.in_rect = False
                super(ThreeDimenButton, self).leaveEvent(None)

    def mouseMoveEvent(self, event):
        is_in = self.inArea(event.pos())

        if is_in and not self.in_rect: # 鼠标移入
            self.in_rect = True
            super(ThreeDimenButton, self).enterEvent(event)
        elif not is_in and self.in_rect and not self.pressing: # 鼠标移出
            self.in_rect = False
            super(ThreeDimenButton, self).leaveEvent(None)

        if self.in_rect:
            super(ThreeDimenButton, self).mouseMoveEvent(event)

    def resizeEvent(self, event):
        self.aop_w = self.width() / AOPER
        self.aop_h = self.height() / AOPER
        return super(ThreeDimenButton, self).resizeEvent(event)

    def anchorTimeOut(self):
        # 因为上面有控件挡住了，所以需要定时监控move情况
        self.mouse_pos = self.mapFromGlobal(QCursor.pos())
        if not self.pressing and not self.inArea(self.mouse_pos): # 鼠标移出
            super(ThreeDimenButton, self).leaveEvent(None)

        MrxyButton.anchorTimeOut(self)

        # 修改阴影的位置
        if self.offset_pos == QPoint(0,0):
            self.shadow_effect.setOffset(0, 0)
        else:
            if self.offset_pos.manhattanLength() > SHADE:
                sx = -SHADE * self.offset_pos.x() / self.offset_pos.manhattanLength()
                sy = -SHADE * self.offset_pos.y() / self.offset_pos.manhattanLength()
                self.shadow_effect.setOffset(sx*self.hover_progress/100, sy*self.hover_progress/100)
            else:
                self.shadow_effect.setOffset(-self.offset_pos.x()*self.hover_progress/100, -self.offset_pos.y()*self.hover_progress/100)

    def getBgPainterPath(self):
        path = QPainterPath()
        if self.hover_progress: # 鼠标悬浮效果
            '''
            位置比例 = 悬浮比例 × 距离比例
            坐标位置 ≈ 鼠标方向偏移
            '''
            hp = self.hover_progress / 100.0
            o = QPoint(self.width()/2, self.height()/2)         # 中心点
            m = self.limitPointXY(self.mapFromGlobal(QCursor.pos())-o, self.width()/2, self.height()/2) # 当前鼠标的点
            f = self.limitPointXY(self.offset_pos, self.aop_w, self.aop_h)  # 偏移点（压力中心）

            lt = QPoint()
            lb = QPoint()
            rb = QPoint()
            rt = QPoint()
            # 左上角
            p = QPoint(self.aop_w, self.aop_h) - o
            prob = self.dian_cheng(m, p) / self.dian_cheng(p, p)
            lt = o + (p) * (1-prob*hp/AOPER)
            # 左下角
            p = QPoint(self.width() - self.aop_w, self.aop_h) - o
            prob = self.dian_cheng(m, p) / self.dian_cheng(p, p)
            rt = o + (p) * (1-prob*hp/AOPER)
            # 右上角
            p = QPoint(self.aop_w, self.height() - self.aop_h) - o
            prob = self.dian_cheng(m, p) / self.dian_cheng(p, p)
            lb = o + (p) * (1-prob*hp/AOPER)
            # 右下角
            p = QPoint(self.width() - self.aop_w, self.height() - self.aop_h) - o
            prob = self.dian_cheng(m, p) / self.dian_cheng(p, p)
            rb = o + (p) * (1-prob*hp/AOPER)
            path.moveTo(lt)
            path.lineTo(lb)
            path.lineTo(rb)
            path.lineTo(rt)
            path.lineTo(lt)
        else:
            # 简单的path，提升性能用
            path.addRect(self.aop_w, self.aop_h, self.width()-self.aop_w*2, self.height()-self.aop_h*2)

        return path

    def getWaterPainterPath(self, water):
        circle = QRectF(water.point.x() - self.water_radius*water.progress/100,
                    water.point.y() - self.water_radius*water.progress/100,
                    self.water_radius*water.progress/50,
                    self.water_radius*water.progress/50)
        path = QPainterPath()
        path.addEllipse(circle)
        return path & self.getBgPainterPath()

    def simulateStatePress(self, s, a):
        self.in_rect = True
        MrxyButton.simulateStatePress(s, a)
        self.in_rect = False

    def inArea(self, point):
        return not (point.x() < self.aop_w \
            or point.x() > self.width()-self.aop_w \
            or point.y() < self.aop_h \
            or point.y() > self.height()-self.aop_h)

    '''
    计算两个向量的叉积
    获取压力值
    '''
    def cha_cheng(self, a, b):
        return a.x() * b.y() - b.x()* a.y()

    def dian_cheng(self, a, b):
        return a.x() * b.x() + a.y() * b.y()

    def limitPointXY(self, v, w, h):
        # 注意：成立时，v.x not = 0，否则除零错误
        if v.x() < -w:
            v.setY(v.y()*-w/v.x())
            v.setX(-w)

        if v.x() > w:
            v.setY(v.y()*w/v.x())
            v.setX(w)

        if v.y() < -h:
            v.setX(v.x()*-h/v.y())
            v.setY(-h)

        if v.y() > h:
            v.setX(v.x()*h/v.y())
            v.setY(h)

        return v
