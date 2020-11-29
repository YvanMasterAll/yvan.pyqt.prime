from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent, QRect, QRectF, pyqtSignal, QSize
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QDialog, QListWidget, QListWidgetItem
from qtpy.QtGui import QHelpEvent, QCursor, QPainter, QColor, QPen, QPainterPath

from common.loader.resource import ResourceLoader

'''
提示信息

btn1 = QPushButton('鼠标悬停1', self, minimumHeight=38, toolTip='这是按钮1')
ToolTip.bind(btn1)
'''

class ToolTipMenu(QWidget):
    __item_height = 38
    __item_width = 200
    on_item_clicked = pyqtSignal(str)

    def __init__(self, *args, data, **kwargs):
        super(ToolTipMenu, self).__init__(*args, **kwargs)

        self.__data = data
        self.set_ui()

    def set_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.list_view = QListWidget()
        self.list_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for item in self.__data:
            li = QListWidgetItem()
            li.setText(item)
            li.setTextAlignment(Qt.AlignCenter)
            li.setSizeHint(QSize(0, self.__item_height))
            self.list_view.addItem(li)
        self.setFixedSize(self.__item_width, self.__item_height*len(self.__data) + 16)
        self.list_view.itemClicked.connect(self.__on_item_clicked)
        self.layout.addWidget(self.list_view)

    def __on_item_clicked(self, item):
        self.parent().hide(force=True)
        self.on_item_clicked.emit(item.text())

class ToolTip(QWidget):
    TIP, MENU, CUSTOM = range(3)
    LEFT, TOP, RIGHT, BOTTOM = range(4)
    HOVER, CLICK = range(2)

    _timeout = 1200
    _leave_timeout = 300
    _margin = 10
    _anchor_width = 5

    on_item_clicked = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(ToolTip, self).__init__(*args, **kwargs)

        self.setObjectName("ToolTip")
        self.setWindowFlags(self.windowFlags() | Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setVisible(False)
        self.setStyleSheet("#ToolTip > QLabel { font-size: 12px; color: white; padding: " + str(self._anchor_width+8) + "px; background-color: transparent; }")
        self.layout = QVBoxLayout(self, spacing=0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 定时隐藏
        self._hideTimer = QTimer(self, timeout=self.hide)

    def place(self):
        if self._type == ToolTip.TIP:
            self.label = QLabel(self)
            self.label.setText(self._tip)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setContentsMargins(0, 0, 0, 0)
            self.layout.addWidget(self.label)
        elif self._type == ToolTip.MENU:
            self._widget = ToolTipMenu(data=self._data)
            self._widget.on_item_clicked.connect(self.__on_item_clicked)
            self.layout.addWidget(self._widget)
        elif self._type == ToolTip.CUSTOM:
            self.layout.addWidget(self._widget)
        if self._trigger == ToolTip.CLICK:
            if hasattr(self.parent(), 'clicked'):
                self.parent().clicked.connect(self.on_parent_clicked)

    def setWidget(self, widget:QWidget):
        self.layout.addWidget(widget)

    def __on_item_clicked(self, text):
        self.on_item_clicked.emit(text)

    @staticmethod
    def bind(parent:QWidget, tip=None, widget=None, type=0, data=None, direction=1, trigger=0):
        tooltip = ToolTip(parent)
        tooltip._type = type
        tooltip._direction = direction
        tooltip._parent = parent
        tooltip._tip = tip
        tooltip._widget = widget
        tooltip._data = data
        tooltip._trigger = trigger
        tooltip.place()
        parent.installEventFilter(tooltip)

        return tooltip

    def hide(self, force=False):
        if force:
            return super(ToolTip, self).hide()
        if self.rect().contains(self.mapFromGlobal(QCursor.pos())):
            self._hideTimer.start(self._timeout)
        else:
            super(ToolTip, self).hide()

    def __show(self):
        widget = self.parent()
        if self._direction == ToolTip.RIGHT:
            self.hide()
            self._hideTimer.stop()
            self.show()
            # 自动隐藏
            self._hideTimer.start(self._timeout)
            pos = widget.mapToGlobal(QPoint(0, 0))
            self.move(pos.x() + widget.width() + self._margin,
                      pos.y() + int((widget.height() - self.height()) / 2))
        if self._direction == ToolTip.LEFT:
            self.hide()
            self._hideTimer.stop()
            self.show()
            # 自动隐藏
            self._hideTimer.start(self._timeout)
            pos = widget.mapToGlobal(QPoint(0, 0))
            self.move(pos.x() - self.width() - self._margin,
                      pos.y() + int((widget.height() - self.height()) / 2))
        if self._direction == ToolTip.TOP:
            self.hide()
            self._hideTimer.stop()
            self.show()
            # 自动隐藏
            self._hideTimer.start(self._timeout)
            pos = widget.mapToGlobal(QPoint(0, 0))
            self.move(pos.x() + int((widget.width() - self.width()) / 2),
                      pos.y() - self.height() - self._margin)
        if self._direction == ToolTip.BOTTOM:
            self.hide()
            self._hideTimer.stop()
            self.show()
            # 自动隐藏
            self._hideTimer.start(self._timeout)
            pos = widget.mapToGlobal(QPoint(0, 0))
            self.move(pos.x() + int((widget.width() - self.width()) / 2),
                      pos.y() + widget.height() + self._margin)

    # 按钮点击显示提示
    def on_parent_clicked(self):
        self.__show()

    def eventFilter(self, widget:QWidget, event):
        if isinstance(event, QHelpEvent):
            return True
        t = event.type()
        if t == QEvent.Enter: # 鼠标进入
            if self._trigger == ToolTip.HOVER:
                self.__show()
        elif t == QEvent.Leave: # 鼠标离开
            self._hideTimer.stop()
            self._hideTimer.start(self._leave_timeout)

        return super(ToolTip, self).eventFilter(widget, event)

    def paintEvent(self, event) -> None:
        super(ToolTip, self).paintEvent(event)

        x = self.rect().x() + self._anchor_width
        y = self.rect().y() + self._anchor_width
        w = self.rect().width() - self._anchor_width*2
        h = self.rect().height() - self._anchor_width * 2

        # 背景
        painter = QPainter(self)
        path = QPainterPath()
        path.addRoundedRect(QRectF(x, y, w, h), 4, 4)
        # 画锚
        if self._direction == ToolTip.TOP:
            x1 = x + w/2 - self._anchor_width
            y1 = y + h
            x2 = x + w/2 + self._anchor_width
            y2 = y + h
            x3 = x + w/2
            y3 = y + h + self._anchor_width
            path.moveTo(x1, y1)
            path.lineTo(x2, y2)
            path.lineTo(x3, y3)
        elif self._direction == ToolTip.BOTTOM:
            x1 = x + w / 2 - self._anchor_width
            y1 = y
            x2 = x + w / 2 + self._anchor_width
            y2 = y
            x3 = x + w / 2
            y3 = y - self._anchor_width
            path.moveTo(x1, y1)
            path.lineTo(x2, y2)
            path.lineTo(x3, y3)
        elif self._direction == ToolTip.RIGHT:
            x1 = x
            y1 = y + h/2 - self._anchor_width
            x2 = x
            y2 = y + h/2 + self._anchor_width
            x3 = x - self._anchor_width
            y3 = y + h/2
            path.moveTo(x1, y1)
            path.lineTo(x2, y2)
            path.lineTo(x3, y3)
        elif self._direction == ToolTip.LEFT:
            x1 = x + w
            y1 = y + h/2 - self._anchor_width
            x2 = x + w
            y2 = y + h/2 + self._anchor_width
            x3 = x + w + self._anchor_width
            y3 = y + h/2
            path.moveTo(x1, y1)
            path.lineTo(x2, y2)
            path.lineTo(x3, y3)

        painter.fillPath(path, ResourceLoader().qt_color_separator_dark)
