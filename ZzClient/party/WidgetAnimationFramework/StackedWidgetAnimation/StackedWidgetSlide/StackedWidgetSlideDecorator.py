from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QRegion
from PyQt5.QtWidgets import QWidget, QStackedWidget


class StackedWidgetSlideDecorator(QWidget):
    m_widgetForGrab:QWidget
    m_foreground:QPixmap

    def __init__(self, *args, _widgetForGrab, **kwargs):
        super(StackedWidgetSlideDecorator, self).__init__(*args, **kwargs)

        self.m_widgetForGrab = _widgetForGrab
        self.grabWidget()

    def grabContainer(self):
        if isinstance(self.parentWidget(), QStackedWidget):
            self.m_widgetForGrab = self.parentWidget().currentWidget()
            self.grabWidget()

    def grabWidget(self):
        size = self.parentWidget().size()
        self.m_widgetForGrab.resize(size)
        self.resize(size)
        self.m_foreground = QPixmap(size)
        # self.m_widgetForGrab.render(self.m_foreground, QPoint(), QRegion(QRect(QPoint(), size)))
        self.m_foreground = self.m_widgetForGrab.grab(QRect(QPoint(), size))

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.m_foreground)

        super(StackedWidgetSlideDecorator, self).paintEvent(_event)

