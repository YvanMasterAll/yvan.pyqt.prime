from PyQt5.QtCore import QPoint, QRect, Qt, pyqtProperty
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QColor
from PyQt5.QtWidgets import QWidget, QStackedWidget


class CircleFillDecorator(QWidget):
    m_startPoint = QPoint()
    m_radius:int
    m_fillColor:QColor

    def __init__(self, *args, **kwargs):
        super(CircleFillDecorator, self).__init__(*args, **kwargs)

        self.m_radius = 0
        self.m_fillColor = Qt.red

    def setStartPoint(self, _point):
        localStartPoint = self.mapFromGlobal(_point)
        if self.m_startPoint != localStartPoint:
            self.m_startPoint = localStartPoint

    def radius(self):
        return self.m_radius

    def setRadius(self, _radius):
        if self.m_radius != _radius:
            self.m_radius = _radius

            self.update()

    def setFillColor(self, _fillColor):
        if self.m_fillColor != _fillColor:
            self.m_fillColor = _fillColor

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setPen(self.m_fillColor)
        painter.setBrush(self.m_fillColor)
        opacity = self.m_radius / ((self.width() + self.height()) / 4)
        painter.setOpacity(opacity)
        painter.drawEllipse(self.m_startPoint, self.m_radius, self.m_radius)

        super(CircleFillDecorator, self).paintEvent(_event)

    _radius = pyqtProperty(int, fget=radius, fset=setRadius)