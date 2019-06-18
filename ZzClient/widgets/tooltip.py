from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QDialog
from qtpy.QtGui import QPalette, QPainter, QBrush, QPen, QColor, QHelpEvent
import math
#
# btn1 = QPushButton('鼠标悬停1', self, minimumHeight=38, toolTip='这是按钮1')
#         ToolTip.bind(btn1)
#

# 提示信息

class ToolTip(QWidget):

    _instance = None
    TimeOut = 2000

    def __init__(self, *args, **kwargs):
        super(ToolTip, self).__init__(*args, **kwargs)

        self.setObjectName("ToolTip")
        self.setWindowFlags(self.windowFlags() |
                            Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setVisible(False)
        layout = QVBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        # 定时隐藏
        self._hideTimer = QTimer(self, timeout=self.hide)

    @classmethod
    def bind(cls, widget):
        if not cls._instance:
            cls._instance = cls()
        widget.installEventFilter(cls._instance)

    def setText(self, text):
        self.label.setText(text)

    def eventFilter(self, widget, event):
        if isinstance(event, QHelpEvent):
            return True
        t = event.type()
        if t == QEvent.Enter:           # 鼠标进入
            self.hide()
            self._hideTimer.stop()
            self.setText(widget.toolTip())
            if widget.toolTip():
                self.show()
                # 自动隐藏
                self._hideTimer.start(self.TimeOut)
                pos = widget.mapToGlobal(QPoint(0, 0))
                self.move(pos.x() + widget.width() + 30,
                          pos.y() + int((widget.height() - self.height()) / 2))
        elif t == QEvent.Leave:         # 鼠标离开
            self._hideTimer.stop()
            self.hide()

        return super(ToolTip, self).eventFilter(widget, event)

# 菊花

class Loading(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.w = 15
        self.h = 15
        self.dot_w = 12
        self.dot_h = 12
        self.timeout = 10
        self.dot_count = 6
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))

        for i in range(self.dot_count):
            if math.floor(self.counter/(self.dot_count-1))%self.dot_count == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter%5)*32, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width()/2 + self.w * math.cos(2*math.pi*i/self.dot_count) - self.dot_w/2,
                self.height()/2 + self.h * math.sin(2*math.pi*i/self.dot_count) - self.dot_h/2,
                self.dot_w, self.dot_h)

        painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(50)
        self.counter = 0

    def hideEvent(self, event):
        self.killTimer(self.timer)

    def timerEvent(self, event):
        self.counter += 1
        self.update()
        if self.counter >= self.timeout*20:
            self.killTimer(self.timer)
            self.hide()