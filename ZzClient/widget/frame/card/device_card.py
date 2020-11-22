from PyQt5.QtCore import Qt, QRect, QRectF, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QFontMetrics, QPainterPath, QColor
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel
import math

from common.loader.resource import ResourceLoader
from common.util.func import calculate_text_width, calculate_text_height
from widget.frame.button.mrxy.mrxy_button import NolinearType
from widget.frame.button.mrxy.waterzoom_button import WaterZoomButton
from widget.frame.tag.tag import Tag
from widget.view import BaseView


class State:
    on = 0
    off = 1

class CardModel:
    icon: QPixmap
    sn: str
    name: str
    state: State
    active: str

    def __init__(self, icon, sn, name, state, active):
        self.icon = icon
        self.sn = sn
        self.name = name
        self.state = state
        self.active = active

'''
设备卡片，鼠标悬浮放大拉近
'''

class DeviceCard(WaterZoomButton):
    fixed_width = 220
    fixed_height = 96

    def __init__(self, *args, model:CardModel, **kwargs):
        super(DeviceCard, self).__init__(*args, **kwargs)

        self.model = model
        self.setNormalColor(ResourceLoader().qt_color_background_light)
        self.setHoverColor(ResourceLoader().qt_color_background_light)
        self.setPressColor(ResourceLoader().qt_color_background)
        self.setChoking(4)
        self.setRadius(5, 10)
        self.hover_speed = 10
        self.title_font = ResourceLoader().qt_font_text
        self.body_font = ResourceLoader().qt_font_text_xss
        self.title_color = ResourceLoader().qt_color_text
        self.body_color = ResourceLoader().qt_color_primary_light

        # 添加状态标签
        self.tag = Tag(self)
        self.updateTag()

        self.show()

    def updateTag(self):
        if self.model.state == State.on:
            self.tag.text = "在线"
            self.tag.padding_h = 4
            self.tag.padding_v = 2
            self.tag.text_color = ResourceLoader().qt_color_tag_online
            self.tag.border_color = ResourceLoader().qt_color_tag_online
        else:
            self.tag.text = "离线"
            self.tag.padding_h = 4
            self.tag.padding_v = 2
            self.tag.text_color = ResourceLoader().qt_color_tag_offline
            self.tag.border_color = ResourceLoader().qt_color_tag_offline

    def paintEvent(self, event):
        super(DeviceCard, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)
        path = QPainterPath()

        # 绘制图标
        c = 0
        r = 0
        margin = 0
        if not self.hover_progress or self.hover_progress < 20:
            c = self.choking
            r = self.radius_x
        else:
            c = self.choking * (1 - self.getNolinearProg(self.hover_progress, NolinearType.SlowFaster if self.hovering else NolinearType.SlowFaster))
            r = self.radius_x if self.radius_zoom < 0 else self.radius_x + (self.radius_zoom-self.radius_x) * self.hover_progress / 100

        rect = QRectF(10, 10, 80-c*2, 80-c*2)
        path.addRoundedRect(rect, 4, 4)
        painter.save()
        painter.setClipPath(path, Qt.IntersectClip)
        painter.drawPixmap(rect.x(), rect.y(), rect.width(), rect.height(), self.model.icon)
        painter.restore()

        # 绘制编号
        fm = QFontMetrics(self.title_font)
        line_height = fm.lineSpacing()

        painter.setPen(self.title_color)
        painter.setFont(self.title_font)
        painter.drawText(QPoint(94-c*2, 36), self.model.sn)

        fm = QFontMetrics(self.body_font)
        line_height = fm.lineSpacing()

        painter.setPen(self.body_color)
        painter.setFont(self.body_font)
        f_rect = fm.boundingRect(QRect(94-c*2, 30+line_height, 0, 0), Qt.TextSingleLine, self.model.name)
        painter.drawText(f_rect, Qt.TextSingleLine, self.model.name)
        f_rect = fm.boundingRect(QRect(94-c*2, 46 + line_height, 0, 0), Qt.TextSingleLine, self.model.active)
        painter.drawText(f_rect, Qt.TextSingleLine, self.model.active)

        # 状态位置
        self.tag.move(220 - self.tag.tag_width() - 10 - c, 10)


