from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent, QRect, pyqtSignal, QObject
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QDialog, QMessageBox, QHBoxLayout
from qasync import QtCore
from qtpy.QtGui import QPalette, QPainter, QBrush, QPen, QColor, QHelpEvent
import math
import copy

from common.loader.resource import ResourceLoader

'''
加载模态层
TODO: 当窗体移动时更新模态层坐标
'''

class Loading(QWidget):
    _thresold = 10000
    on_outer_close = pyqtSignal()

    def __init__(self, *args, modal=False, **kwargs):
        super(Loading, self).__init__(*args, **kwargs)
        # 是否是模态层，如果是将父窗口挂起
        self.modal = modal
        if modal:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
            self.setWindowModality(Qt.ApplicationModal)

        # procedure
        self.setObjectName('Loading')
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.hide()
        self.set_ui()
        self.place()

        # 计时器，超时关闭
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.timer.start(self._thresold)

        # 关闭信号
        self.on_outer_close.connect(self.hide)

    def set_ui(self):
        self.spinner = Spinner(self)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(70.0)
        self.spinner.setNumberOfLines(8)
        self.spinner.setLineLength(8)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(8)
        self.spinner.setRevolutionsPerSecond(1)
        self.spinner.setColor(QColor(240, 240, 240))

    def place(self):
        pass

    def show(self):
        geometry = self.parent().geometry()
        self.raise_()
        if self.parent().isWindow():
            if self.modal:
                self.setGeometry(geometry)
            else:
                self.setGeometry(QRect(QPoint(), geometry.size()))
        else:
            # 如果显示的容器不是一个窗口，重新计算坐标
            if self.modal:
                self.setGeometry(QRect(self.parent().mapToGlobal(QPoint(geometry.x(), geometry.y())), geometry.size()))
            else:
                self.setGeometry(geometry)
        self.spinner.start()
        super(Loading, self).show()

    def hide(self):
        if hasattr(self, 'spinner'):
            self.spinner.stop()
        super(Loading, self).hide()

class Spinner(QWidget):
    def __init__(self, *args, centerOnParent=True, disableParentWhenSpinning=True, **kwargs):
        super(Spinner, self).__init__(*args, **kwargs)

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

        self.setAttribute(Qt.WA_TranslucentBackground)

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parent() != None and self._disableParentWhenSpinning:
            self.parent().setDisabled(False)

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
        if self.parent() != None and self._centerOnParent:
            self.move(self.parent().width()/2 - self.width()/2,
                      self.parent().height()/2 - self.height()/2)

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parent() != None and self._disableParentWhenSpinning:
            self.parent().setDisabled(True)

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

'''
文本加载对话框
'''

class TextLoading(QObject):
    on_outer_close = pyqtSignal()

    def __init__(self):
        super(TextLoading, self).__init__()

        self.on_outer_close.connect(self.hide)

    def show(self, waiting_info: str = "加载中，请稍后"):
        '''
        等待对话框
        '''
        if not hasattr(self, 'dialog'):
            self.dialog = QDialog(None, Qt.FramelessWindowHint)
            self.dialog.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.Tool |
                   Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint |
                   Qt.WindowMaximizeButtonHint)
        self.dialog.resize(200, 40)
        self.dialog.layout = QHBoxLayout(self.dialog)
        self.dialog.label = QLabel(waiting_info)
        self.dialog.label.setFont(ResourceLoader().qt_font_text_xs)
        self.dialog.layout.addWidget(self.dialog.label, alignment=Qt.AlignCenter)
        self.dialog.exec_()

    def hide(self):
        if hasattr(self, 'dialog'):
            self.dialog.close()

'''
Toast
'''

# class Toast(QObject):
#     @staticmethod
#     def show():
#         #