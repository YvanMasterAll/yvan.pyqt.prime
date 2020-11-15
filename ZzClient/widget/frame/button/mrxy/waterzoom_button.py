from PyQt5.QtCore import pyqtSignal, Qt, QRectF
import math
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, QCursor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton, NolinearType

DEFAULT_CHOKING = 5

class WaterZoomButton(MrxyButton):

    def __init__(self, *args, **kwargs):
        super(WaterZoomButton, self).__init__(*args, **kwargs)

        self.choking = DEFAULT_CHOKING
        self.radius_zoom = -1
        self.choking_prop = 0

    def setChoking(self, c):
        self.choking = c

    def getChokingSpacing(self,):
        return self.choking * 2

    def getDefaultSpacing(self):
        return DEFAULT_CHOKING * 2

    def setChokingProp(self, p):
        self.choking = min(self.width(), self.height()) * p
        self.choking_prop = p

    def setRadiusZoom(self, radius):
        self.radius_zoom = radius

    def setRadius(self, x, x2):
        # 注意：最终绘制中只计算 x 的半径，无视 y 的半径
        MrxyButton.setRadius(self, x)
        self.radius_zoom = x2

    def getBgPainterPath(self):
        path = QPainterPath()
        c: int
        r: int
        if not self.hover_progress:
            c = self.choking
            r = self.radius_x
        else:
            c = self.choking * (1 - self.getNolinearProg(self.hover_progress, NolinearType.SpringBack50 if self.hovering else NolinearType.SpringBack50))
            r = self.radius_x if self.radius_zoom < 0 else self.radius_x + (self.radius_zoom-self.radius_x) * self.hover_progress / 100

        if r:
            path.addRoundedRect(QRectF(c,c,self.size().width()-c*2,self.size().height()-c*2), r, r)
        else:
            path.addRect(QRect(c,c,self.size().width()-c*2,self.size().height()-c*2))
        return path

    def resizeEvent(self, event):
        super(WaterZoomButton, self).resizeEvent(event)

        if math.fabs(self.choking_prop)>0.0001:
            self.choking = min(self.width(), self.height()) * self.choking_prop
