import sys
from os.path import abspath

from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QGridLayout
from gitdb.util import join, dirname
from qtpy import QtCore, QtWidgets, uic
import resources.qss.theme.dark.style_rc
from config.theme import Theme
from ZzClient.test.widget.form._form import Ui_Form
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
'''

# _ui = join(dirname(abspath(__file__)), './_form.ui')

class Window(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setFixedSize(440, 500)
        self.setStyleSheet(Style)

        # uic.loadUi(_ui, self)

        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    # fontDB = QFontDatabase()
    # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
    # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
    # app.setFont(QFont('Microsoft YaHei'))
    window = Window()
    window.show()

    sys.exit(app.exec_())