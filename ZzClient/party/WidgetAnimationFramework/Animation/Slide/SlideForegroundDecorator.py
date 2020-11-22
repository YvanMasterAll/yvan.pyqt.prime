from PyQt5.QtCore import QPoint, QRect, Qt, QTimeLine, QEasingCurve, QSize
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QColor
from PyQt5.QtWidgets import QWidget, QStackedWidget


class SlideForegroundDecorator(QWidget):
    m_foreground:QPixmap

    def __init__(self, *args, **kwargs):
        super(SlideForegroundDecorator, self).__init__(*args, **kwargs)

    def grabParent(self, _size):
        self.resize(_size)
        self.m_foreground = QPixmap(_size)
        # self.parentWidget().render(self.m_foreground, QPoint(), QRegion(QRect(QPoint(), _size)))
        self.m_foreground = self.parentWidget().grab(QRect(QPoint(), _size))

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.m_foreground)

        QWidget.paintEvent(self, _event)