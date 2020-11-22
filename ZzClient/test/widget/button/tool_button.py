import sys

import qtawesome
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QToolButton, \
    QMenu
from qtpy import QtCore, QtWidgets
import resources.qss.theme.dark.style_rc
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.view import BaseView

Style = '''
Window {
    background-color: #333842;   
}
/* Button_Primary */
QPushButton[type="0"] {
    background-color: #007AFF;
    padding: 4px 0;
}
/* Button_Primary_Outline */
QPushButton[type="1"] {
    border-color: #007AFF;
    background-color: transparent;
}
QPushButton[type="1"]:hover {
    background-color: transparent;
    color: #007AFF;
}
/* Button_Warning */
QPushButton[type="2"] {
    background-color: #F24958;
}
/* Button_Warning_Outline */
QPushButton[type="3"] {
    background-color: transparent;
    border-color: #F24958;
}
QPushButton[type="3"]:hover {
    background-color: transparent;
    color: #F24958;
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
        # 带菜单按钮
        button = QToolButton()
        button.setText("菜单")
        menu = QMenu()
        for action in ['Action A', 'Action B', 'Action C']:
            menu.addAction(action)
        button.setMenu(menu)
        button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        layout.addWidget(button)
        # pushbutton
        button2 = QPushButton()
        button2.setProperty("type", 0)
        button2.setText("提交")
        layout.addWidget(button2)
        button3 = QPushButton()
        button3.setProperty("type", 1)
        button3.setText("提交")
        layout.addWidget(button3)
        button4 = QPushButton()
        button4.setProperty("type", 2)
        button4.setText("提交")
        layout.addWidget(button4)
        button5 = QPushButton()
        button5.setProperty("type", 3)
        button5.setText("提交")
        layout.addWidget(button5)
        button6 = QPushButton()
        button6.setText("提交")
        layout.addWidget(button6)
        button7 = QPushButton()
        button7.setProperty("type", 0)
        button7.setText("提交")
        button7.setIcon(qtawesome.icon('fa5s.inbox', color=QColor('#FFFEFE')))
        button7.setIconSize(QSize(32, 24))
        layout.addWidget(button7)

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