from PyQt5.QtCore import QRectF, QRect, Qt
from PyQt5.QtGui import QPainter, QPainterPath, QFontMetrics, QPen, QColor
from PyQt5.QtWidgets import QWidget
from common.loader.resource import ResourceLoader

'''
标签
'''

class Tag(QWidget):
    text = '标签'
    border_radius = 4
    border_width = 1
    padding_v = 4
    padding_h = 4

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

        self.font = ResourceLoader().qt_font_text_tag
        self.text_color = ResourceLoader().qt_color_text
        self.border_color = ResourceLoader().qt_color_text

    def paintEvent(self, event):
        super(Tag, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)
        path = QPainterPath()

        # 绘制文本
        painter.setFont(self.font)
        painter.setPen(self.text_color)
        fm = QFontMetrics(painter.font())
        w = fm.width(self.text)
        h = fm.height()
        rect = QRectF(0, 0, w + self.padding_h*2, h + self.padding_v*2)
        painter.drawText(QRect(self.padding_h, self.padding_v, w, h), Qt.TextWordWrap, self.text)
        # 设置尺寸
        self.setFixedSize(rect.width(), rect.height())
        # 绘制边框
        path.addRoundedRect(rect, self.border_radius, self.border_radius)
        painter.strokePath(path, QPen(self.border_color, self.border_width))

    def tag_width(self):
        fm = QFontMetrics(self.font)
        return fm.width(self.text) + self.padding_h
