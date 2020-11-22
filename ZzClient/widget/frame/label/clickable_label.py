from PyQt5.QtCore import pyqtSignal, pyqtProperty
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel

class ClickableLabel(QLabel):
    mColor:QColor

    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ClickableLabel, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def setColor(self, color):
        self.mColor = color
        self.setStyleSheet("color: {color}".format(color=color.name()))

    def color(self):
        return self.mColor

    _color = pyqtProperty(QColor, fget=color, fset=setColor)