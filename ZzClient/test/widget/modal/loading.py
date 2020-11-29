import asyncio
import math, sys
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTextEdit, QGridLayout, QPushButton, QLabel
from qtpy.QtGui import QPalette, QPainter, QBrush, QPen, QColor

from common.util.worker import Worker
from widget.activity.modal.loading import Spinner, Loading, TextLoading

'''
菊花测试
'''

# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#
#         widget = QWidget(self)
#         self.editor = QTextEdit()
#         self.editor.setPlainText("0123456789" * 100)
#         layout = QGridLayout(widget)
#         layout.addWidget(self.editor, 0, 0, 1, 3)
#         button = QPushButton("Wait")
#         layout.addWidget(button, 1, 1, 1, 1)
#
#         self.setCentralWidget(widget)
#         self.overlay = Spinner2(self.centralWidget())
#         self.overlay.hide()
#         button.clicked.connect(self.show_loading)
#
#     def show_loading(self):
#         self.timer = QTimer()
#         self.timer.start(20000)
#         self.timer.timeout.connect(self.close_loading)
#         self.overlay.show()
#
#     def close_loading(self):
#         self.overlay.hide()
#
#     def resizeEvent(self, event):
#         self.overlay.resize(event.size())
#         event.accept()
#
# class MainWindow2(QMainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#
#         widget = QWidget(self)
#         self.editor = QTextEdit()
#         self.editor.setPlainText("0123456789" * 100)
#         layout = QGridLayout(widget)
#         layout.addWidget(self.editor, 0, 0, 1, 3)
#         self.button = QPushButton("Wait")
#         layout.addWidget(self.button, 1, 1, 1, 1)
#
#         self.setCentralWidget(widget)
#
#         self.setObjectName("Window")
#         self.centralWidget().setObjectName("Widget")
#         self.spinner = Spinner(self)
#         self.spinner.setRoundness(70.0)
#         self.spinner.setMinimumTrailOpacity(15.0)
#         self.spinner.setTrailFadePercentage(70.0)
#         self.spinner.setNumberOfLines(10)
#         self.spinner.setLineLength(10)
#         self.spinner.setLineWidth(5)
#         self.spinner.setInnerRadius(10)
#         self.spinner.setRevolutionsPerSecond(1)
#         self.spinner.setColor(QColor(81, 4, 71))
#         self.button.setObjectName("button")
#         self.button.clicked.connect(self.show_loading)
#
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.close_loading)
#
#     def show_loading(self):
#         self.timer.start(2000)
#         self.setDisabled(True)
#         self.spinner.start()
#
#     def close_loading(self):
#         self.spinner.stop()
#
# if __name__ == "__main__":
#     # Loading
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
#
#     # Spinner
#     # app = QApplication(sys.argv)
#     # window = MainWindow2()
#     # window.show()
#     # sys.exit(app.exec_())


import sys
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem
from qtpy import QtCore, QtWidgets, QtGui
import resources.qss.theme.dark.style_rc
from bloc.app import Bloc_App
from common.loader.resource import ResourceLoader
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
'''

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        self.setStyleSheet(Style)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        widget = QWidget(self)
        widget.setFixedSize(300, 300)
        widget.setLayout(QVBoxLayout())
        widget.move(0, 0)

        # loader = Loading(self, modal=True)  # 推荐
        # loader = Loading(self, modal=False)
        # loader = Loading(widget, modal=True)
        loader = Loading(widget, modal=False) # 推荐

        btn2 = QPushButton()
        btn2.setText("hello")
        widget.layout().addWidget(btn2)

        btn1 = QPushButton()
        btn1.setText("点我")
        layout.addWidget(btn1)
        btn1.clicked.connect(loader.show)

        self.textLoading = TextLoading()
        btn1 = QPushButton()
        btn1.setText("点我")
        layout.addWidget(btn1)
        btn1.clicked.connect(self.show_textloading)

    async def long_time_work(self):
        await asyncio.sleep(3)
        self.textLoading.on_outer_close.emit()

    def show_textloading(self):
        Worker().run_task(self.long_time_work())
        self.textLoading.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        Bloc_App().app_closed.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    app.setFont(ResourceLoader.load_app_font())
    window = Window()
    window.show()

    sys.exit(app.exec_())