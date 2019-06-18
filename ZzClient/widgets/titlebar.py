from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from base import setStyle

# 标题栏

class Titlebar(QFrame):
    def __init__(self, parent=None):
        super(Titlebar, self).__init__()
        self.parent = parent

        self.setupUI()
        self.setupLayouts()

    """初始化"""
    def setupUI(self):
        self.setObjectName('Titlebar')
        setStyle("titlebar", self)

        # Buttons
        self.closeButton = QPushButton('×', self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMinimumSize(21, 17)
        self.closeButton.setMouseTracking(False)

    def setupLayouts(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)
