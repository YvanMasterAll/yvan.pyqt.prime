from PyQt5.QtCore import QPoint, QRect, pyqtProperty, Qt
from PyQt5.QtGui import QPixmap, QPainter, QRegion, QColor, QPainterPath
from PyQt5.QtWidgets import QWidget, QStackedWidget

class StackedWidgetFadeInDecorator(QWidget):
    m_opacity:float = 1

    def __init__(self, *args, _fadeWidget, **kwargs):
        super(StackedWidgetFadeInDecorator, self).__init__(*args, **kwargs)

        self.m_containerPixmap = QPixmap()
        self.m_fadeWidgetPixmap = QPixmap()
        self.m_fadeWidget = _fadeWidget
        self.grabFadeWidget()

    def opacity(self):
        return self.m_opacity

    def setOpacity(self, _opacity):
        if self.m_opacity != _opacity:
            self.m_opacity = _opacity

            self.update()

    def grabContainer(self):
        if isinstance(self.parentWidget(), QStackedWidget):
            self.m_containerPixmap = self.grabWidget(self.parentWidget().currentWidget())

    def grabFadeWidget(self):
        self.m_fadeWidgetPixmap = self.grabWidget(self.m_fadeWidget)

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.m_containerPixmap)
        painter.setOpacity(self.m_opacity)
        # path = QPainterPath()
        # path.addRect(0, 0, 1000, 1000)
        # painter.fillPath(path, Qt.red)
        painter.drawPixmap(0, 0, self.m_fadeWidgetPixmap)

        super(StackedWidgetFadeInDecorator, self).paintEvent(_event)

    def grabWidget(self, _widgetForGrab):
        size = self.parentWidget().size()
        _widgetForGrab.resize(size)
        self.resize(size)
        # widgetPixmap = QPixmap(size)
        # _widgetForGrab.render(widgetPixmap, QPoint(), QRegion(QRect(QPoint(), size)))
        widgetPixmap = _widgetForGrab.grab(QRect(QPoint(), self.size()))
        return widgetPixmap

    opacity = pyqtProperty(float, fget=opacity, fset=setOpacity)

