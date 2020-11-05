from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from qtpy.QtGui import QPainter, QColor, QPainterPath
from ZzClient.widget.view import BaseView

# 标题栏

class Titlebar(BaseView):
    def __init__(self, *args, **kwargs):
        super(Titlebar, self).__init__(*args, **kwargs)

        self.procedure()

    """初始化"""
    def set_ui(self):
        self.setObjectName('Titlebar')
        self.set_style("home/titlebar")

        # Buttons
        self.closeButton = QPushButton('×', self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMinimumSize(21, 17)
        self.closeButton.setMouseTracking(False)

    def place(self):
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.closeButton)

        self.setLayout(self.layout)
