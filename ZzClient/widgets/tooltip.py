from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent, QRect
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QDialog
from qtpy.QtGui import QPalette, QPainter, QBrush, QPen, QColor, QHelpEvent
import math
import copy
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
        self.hide()

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

class Spinner(QWidget):
    def __init__(self, parent=None, centerOnParent=True, disableParentWhenSpinning=True):
        QWidget.__init__(self)
        self.parent = parent

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning
        self._color = QColor(Qt.black)
        self._roundness = 100.0
        self._minimumTrailOpacity = 3.14159265358979323846
        self._trailFadePercentage = 80.0
        self._revolutionsPerSecond = 1.57079632679489661923
        self._numberOfLines = 20
        self._lineLength = 10
        self._lineWidth = 2
        self._innerRadius = 10
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parent != None and self._disableParentWhenSpinning:
            self.parent.setDisabled(False)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength)*2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self._timer.setInterval(1000/(self._numberOfLines*self._revolutionsPerSecond))

    def updatePosition(self):
        if self.parent != None and self._centerOnParent:
            self.move(self.parent.pos().x() + self.parent.width()/2 - self.width()/2,
                      self.parent.pos().y() + self.parent.height()/2 - self.height()/2)

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parent != None and self._disableParentWhenSpinning:
            self.parent.setDisabled(True)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def paintEvent(self, event):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(Qt.NoPen)
        for i in range(0, self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength, self._innerRadius + self._lineLength)
            rotateAngle = float(360*i)/float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = int(self.lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines))
            color = self.currentLineColor(distance, self._numberOfLines, self._trailFadePercentage, self._minimumTrailOpacity, self._color)
            painter.setBrush(color)
            # TODO: improve the way rounded rect is painted
            painter.drawRoundedRect(QRect(0, -self._lineWidth/2, self._lineLength, self._lineWidth), self._roundness, self._roundness, Qt.RelativeSize)
            painter.restore()

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines

        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, color):
        _color = copy.copy(color)
        if countDistance == 0:
            return _color

        minAlphaF = minOpacity/100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1)*trailFadePerc/100.0))
        if countDistance > distanceThreshold:
            _color.setAlphaF(minAlphaF)
        else:
            alphaDiff = _color.alphaF() - minAlphaF
            gradient = alphaDiff/float(distanceThreshold + 1)
            resultAlpha = _color.alphaF() - gradient*countDistance

            # if alpha is out of bounds, clip it
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            _color.setAlphaF(resultAlpha)

        return _color

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color):
        self._color = color

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()
