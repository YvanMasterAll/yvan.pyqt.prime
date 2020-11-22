from PyQt5.QtCore import QPoint, QRect, Qt, QTimeLine, QEasingCurve, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QColor
from PyQt5.QtWidgets import QWidget, QStackedWidget


class SideSlideDecorator(QWidget):
    m_slidePos:QPoint
    m_slideWidgetPixmap:QPixmap
    m_timeline:QTimeLine
    m_backgroundPixmap:QPixmap
    m_decorationColor:QColor

    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(SideSlideDecorator, self).__init__(*args, **kwargs)

        self.resize(self.maximumSize())

        self.m_backgroundPixmap = QPixmap()

        self.m_slidePos = QPoint()
        self.m_timeline = QTimeLine()
        self.m_timeline.setDuration(260)
        self.m_timeline.setUpdateInterval(40)
        self.m_timeline.setEasingCurve(QEasingCurve.OutQuad)
        self.m_timeline.setStartFrame(0)
        self.m_timeline.setEndFrame(10000)

        self.m_decorationColor = QColor(0, 0, 0, 0)

        def frameChanged(_value):
            self.m_decorationColor = QColor(0, 0, 0, _value / 100)
            self.update()
        self.m_timeline.frameChanged.connect(frameChanged)

    def grabSlideWidget(self, _slideWidget):
        self.m_slideWidgetPixmap = _slideWidget.grab()

    def grabParent(self):
        # self.m_backgroundPixmap = self.parentWidget().grab()
        pass

    def decorate(self, _dark):
        if self.m_timeline.state() == QTimeLine.Running:
            self.m_timeline.stop()

        self.m_timeline.setDirection(QTimeLine.Forward if _dark else QTimeLine.Backward)
        self.m_timeline.start()

    def slidePos(self):
        return self.m_slidePos

    def setSlidePos(self, _pos):
        if self.m_slidePos != _pos:
            self.m_slidePos = _pos
            self.update()

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.m_backgroundPixmap)
        painter.fillRect(self.rect(), self.m_decorationColor)
        painter.drawPixmap(self.m_slidePos, self.m_slideWidgetPixmap)

        super(SideSlideDecorator, self).paintEvent(_event)

    def mousePressEvent(self, _event):
        self.clicked.emit()

        super(SideSlideDecorator, self).mousePressEvent(_event)

    _slidePos = pyqtProperty(QPoint, fget=slidePos, fset=setSlidePos)