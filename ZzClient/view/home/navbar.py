from qtpy import QtGui, QtCore
from qtpy.QtWidgets import QScrollArea, QVBoxLayout, QFrame
from qtpy.QtGui import QPainter, QColor, QPainterPath
from qtpy.QtCore import Qt, QRectF, QEvent, QPoint
import math
from ZzClient.widget.view import BaseView
from ZzClient.config.const import Config
from PyQt5.QtCore import QObject

'''
左侧导航栏
'''

class Navbar(BaseView, QScrollArea):
    def __init__(self, *args, **kwargs):
        super(Navbar, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        self.setObjectName('Navbar')
        self.set_style('home/navbar')

        # 固定宽度
        self.setFixedWidth(Config().navbar_width)
        # 导航栏
        self.navigation = Navigation(self)
        # 设置布局
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.navigation)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

class Navigation(BaseView):
    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        self.setObjectName("Navigation")

        self.setFixedWidth(Config().navbar_width)
        self.backgroundColor = QColor('#FFFFFF')
        self.selectedColor = QColor("#F0F0F0")
        self.rowHeight = 40
        self.currentIndex = 0
        self.listItems = ["首页", "测试1", "测试2"]
        # 安装事件拦截器
        self.installEventFilter(self)
        # 主窗口大小调整区域
        self.window_zoom_zone = [QPoint(x, y) for x in range(0, 5) for y in range(5, self.height() - 5)]

    def addItem(self, title):
        self.listItems.append(title)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Draw background color
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawRoundedRect(self.rect(), 5, 5)

        # Draw items
        count = 0
        for str in self.listItems:
            itemPath = QPainterPath()
            itemPath.addRect(0, count * self.rowHeight, self.width(), self.rowHeight)

            if self.currentIndex == count:
                painter.setPen(QColor("#00B379"))
                painter.fillPath(itemPath, self.selectedColor)
            else:
                painter.setPen(QColor("#2A2A2A"))
                painter.fillPath(itemPath, self.backgroundColor)

            painter.drawText(QRectF(0, count * self.rowHeight, self.width(), self.rowHeight),
                             Qt.AlignCenter | Qt.AlignHCenter, str)

            count += 1

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            # 左侧边界不拦截事件，放路给主窗口调整窗口大小
            if event.pos() in self.window_zoom_zone:
                return QObject.eventFilter(self, obj, event)
            self._mousePressEvent(event)
            return True

        return QObject.eventFilter(self, obj, event)

    def _mousePressEvent(self, event):
        if event.pos().y() / self.rowHeight < len(self.listItems):
            self.currentIndex = math.floor(event.y() / self.rowHeight)
            self.parent().bloc.on_navbar_changed.emit(self.currentIndex)

            self.update()