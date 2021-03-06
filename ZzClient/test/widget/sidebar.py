import sys
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient, QLabel
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
        sidebar = SideBar(self)
        layout.addWidget(sidebar)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        Bloc_App().app_closed.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    app.setFont(ResourceLoader.load_app_font())
    window = Window()
    window.show()

    sys.exit(app.exec_())