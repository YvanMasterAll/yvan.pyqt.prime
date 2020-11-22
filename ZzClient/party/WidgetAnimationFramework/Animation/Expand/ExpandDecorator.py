from PyQt5.QtCore import QPoint, QRect, Qt, pyqtProperty
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QColor
from PyQt5.QtWidgets import QWidget, QStackedWidget


class ExpandDecorator(QWidget):
    m_expandRectPixmap:QPixmap
    m_expandRect:QRect
    m_fillColor:QColor

    def __init__(self, *args, **kwargs):
        super(ExpandDecorator, self).__init__(*args, **kwargs)

    def expandRect(self):
        return self.m_expandRect

    def setExpandRect(self, _expandRect):
        if self.m_expandRect != _expandRect:
            self.m_expandRect = _expandRect

            self.update()

    def grabExpandRect(self):
        self.m_expandRectPixmap = QPixmap(self.m_expandRect.size())
        # self.parentWidget().render(self.m_expandRectPixmap, QPoint(), QRegion(self.m_expandRect))
        self.m_expandRectPixmap = self.parentWidget().grab(QRect(QPoint(), self.m_expandRect))

    def setFillColor(self, _fillColor):
        if self.m_fillColor != _fillColor:
            self.m_fillColor = _fillColor

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setOpacity(min(self.m_expandRect.height() / self.height(), 0.4))
        painter.fillRect(self.rect(), Qt.black)
        painter.setOpacity(1)
        painter.fillRect(self.m_expandRect, self.m_fillColor)
        painter.drawPixmap(self.m_expandRect.topLeft(), self.m_expandRectPixmap)

        painter.setPen(Qt.black)
        left = QPoint()
        right = QPoint()
        left = self.m_expandRect.topLeft()
        right = self.m_expandRect.topRight()
        left.setY(left.y() - 1)
        right.setY(right.y() - 1)
        painter.setOpacity(0.1)
        painter.drawLine(left, right)

        left.setY(left.y() - 1)
        right.setY(right.y() - 1)
        painter.setOpacity(0.4)
        painter.drawLine(left, right)

        left.setY(left.y() - 1)
        right.setY(right.y() - 1)
        painter.setOpacity(0.2)
        painter.drawLine(left, right)

        left = self.m_expandRect.bottomLeft()
        right = self.m_expandRect.bottomRight()
        left.setY(left.y() + 1)
        right.setY(right.y() + 1)
        painter.setOpacity(0.1)
        painter.drawLine(left, right)

        left.setY(left.y() + 1)
        right.setY(right.y() + 1)
        painter.setOpacity(0.4)
        painter.drawLine(left, right)

        left.setY(left.y() + 1)
        right.setY(right.y() + 1)
        painter.setOpacity(0.2)
        painter.drawLine(left, right)

        left.setY(left.y() + 1)
        right.setY(right.y() + 1)
        painter.setOpacity(0.1)
        painter.drawLine(left, right)

        super(ExpandDecorator, self).paintEvent(_event)

    _expandRect = pyqtProperty(QRect, fget=expandRect, fset=setExpandRect)