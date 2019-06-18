from qtpy.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QFrame
from qtpy.QtGui import QPainter, QColor, QPainterPath, QFont
from qtpy.QtCore import Qt, QRectF, QEvent
import math
from base import Const
from styles import Color, Font
from base import setStyle

# 左侧导航栏

class Navbar(QScrollArea):
    def __init__(self, parent=None):
        super(Navbar, self).__init__()
        self.parent = parent

        self.setupUI()

    def setupUI(self):
        self.setObjectName('Navbar')
        setStyle("navbar", self)

        # 固定宽度
        self.setFixedWidth(Const.navbar_width)
        # 导航栏
        self.navigation = Navigation(self)
        # 设置布局
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.navigation)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

class Navigation(QFrame):
    def __init__(self, parent=None):
        super(Navigation, self).__init__()
        self.parent = parent

        self.setupUI()

    def setupUI(self):
        self.setObjectName("Navigation")

        self.setFixedWidth(Const.navbar_width)
        self.backgroundColor = QColor('#FFFFFF')
        self.selectedColor = Color.black50
        self.rowHeight = 40
        self.currentIndex = 0
        self.listItems = ["首页", "测试1", "测试2"]

    def addItem(self, title):
        self.listItems.append(title)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Draw background color
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Draw items
        count = 0
        for str in self.listItems:
            itemPath = QPainterPath()
            itemPath.addRect(0, count * self.rowHeight, self.width(), self.rowHeight)

            if self.currentIndex == count:
                painter.setPen(Color.green900)
                painter.fillPath(itemPath, self.selectedColor)
            else:
                painter.setPen(Color.black900)
                painter.fillPath(itemPath, self.backgroundColor)

            painter.drawText(QRectF(0, count * self.rowHeight, self.width(), self.rowHeight),
                             Qt.AlignCenter | Qt.AlignHCenter, str)

            count += 1

    def _mousePressEvent(self, event):
        if event.pos().y() / self.rowHeight < len(self.listItems):
            self.currentIndex = math.floor(event.y() / self.rowHeight)
            self.parent.bloc.on_navbar_changed.emit(self.currentIndex)

            self.update()