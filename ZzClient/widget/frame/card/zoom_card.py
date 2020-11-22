from PyQt5.QtCore import Qt, QRect, QRectF, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QFontMetrics, QPainterPath, QColor
from PyQt5.QtWidgets import QScrollArea
import math

from common.loader.resource import ResourceLoader
from widget.frame.button.mrxy.mrxy_button import NolinearType
from widget.frame.button.mrxy.waterzoom_button import WaterZoomButton

class CardModel:
    pixmap: QPixmap
    title: str
    subTitle: str

    def __init__(self, pixmap, title, subTitle):
        self.pixmap = pixmap
        self.title = title
        self.subTitle = subTitle

'''
卡片，鼠标悬浮放大拉近
'''

class ZoomCard(WaterZoomButton):
    fixed_width = 140
    fixed_height = 240
    pixmap_width = 100
    pixmap_height = 150
    title_color = Qt.black
    subTitle_color = Qt.gray

    def __init__(self, *args, model:CardModel, **kwargs):
        super(ZoomCard, self).__init__(*args, **kwargs)

        self.pixmap = model.pixmap
        self.title = model.title
        self.subTitle = model.subTitle

        self.setNormalColor(ResourceLoader().qt_color_text)
        self.setHoverColor(ResourceLoader().qt_color_text)
        self.setChoking(10)
        self.setRadius(5, 10)

        self.show()

    def paintEvent(self, event):
        super(ZoomCard, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)
        path = QPainterPath()

        # 获取图片路径
        c = 0
        r = 0
        margin = 0
        if not self.hover_progress or self.hover_progress < 20:
            c = self.choking
            r = self.radius_x
            margin = 10
        else:
            c = self.choking * (1 - self.getNolinearProg(self.hover_progress, NolinearType.SpringBack50 if self.hovering else NolinearType.SpringBack50))
            r = self.radius_x if self.radius_zoom < 0 else self.radius_x + (self.radius_zoom-self.radius_x) * self.hover_progress / 100
            margin = math.sqrt(125-self.hover_progress)

        rect = QRectF(c+margin,c+margin,self.size().width()-c*2-margin*2,(self.size().width()-c*2-margin*2)*self.pixmap_height/self.pixmap_width)
        path.addRoundedRect(rect, r, r)
        painter.save()
        painter.setClipPath(path, Qt.IntersectClip)
        painter.drawPixmap(QRect(c+margin,c+margin,self.size().width()-c*2-margin*2,(self.size().width()-c*2-margin*2)*self.pixmap_height/self.pixmap_width), self.pixmap)
        painter.restore()

        # 画文字
        fm = QFontMetrics(self.font())
        line_height = fm.lineSpacing()

        painter.setPen(self.title_color)
        painter.drawText(QPoint(rect.left(), rect.bottom()+line_height), self.title)

        painter.setPen(self.subTitle_color)
        f_rect = fm.boundingRect(QRect(rect.left(),rect.bottom()+line_height*1.5,rect.width(),0),Qt.TextWordWrap,self.subTitle)
        painter.drawText(f_rect, Qt.TextWordWrap, self.subTitle)

