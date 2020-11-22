import sys

import qtawesome
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QToolButton
from qtpy import QtCore, QtWidgets
import resources.qss.theme.dark.style_rc
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.form.baselineedit import BaseLineEdit
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
'''

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setObjectName("Widget")
        self.resize(560, 421)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        # 编辑框1
        btn1 = QToolButton()
        btn1.setIcon(qtawesome.icon('fa5s.inbox', color=QColor('#FFFEFE')))
        btn1.setIconSize(QSize(32, 32))
        btn1.setStyleSheet("background-color:transparent")
        lineEdit1 = BaseLineEdit(self, leftWidget=None, rightWidget=btn1)
        lineEdit1.setFixedHeight(50)
        # lineEdit1.setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred)
        lineEdit1.setStyleSheet("QLineEdit{border-radius:25pxfont-size:15pt}")
        lineEdit1.setLeftRightLayoutMargin(20, 20)
        lineEdit1.setPlaceholderText("please input search content")
        self.horizontalLayout.addWidget(lineEdit1)
        # 编辑框2
        btn2 = QToolButton()
        btn2.setIcon(QIcon(QPixmap("./images/calendar.png")))
        btn2.setIconSize(QSize(32, 32))
        btn2.setStyleSheet("background-color:transparent")
        lineEdit2 = BaseLineEdit(self, leftWidget=btn2)
        lineEdit2.setFixedHeight(50)
        lineEdit2.setLeftRightLayoutMargin(5, 20)
        self.horizontalLayout_2.addWidget(lineEdit2)
        # 编辑框3
        btn3 = QToolButton()
        btn3.setIcon(QIcon(QPixmap("./images/search.png")))
        btn3.setIconSize(QSize(32, 32))
        btn3.setStyleSheet("background-color:transparent")
        btn3_2 = QToolButton()
        btn3_2.setIcon(QIcon(QPixmap("./images/delete.png")))
        btn3_2.setIconSize(QSize(32, 32))
        btn3_2.setStyleSheet("background-color:transparent")
        btn3_2.clicked.connect(self.btn3_2Slot)
        self.lineEdit3 = BaseLineEdit(self, leftWidget=btn3, rightWidget=btn3_2)
        self.lineEdit3.setFixedHeight(50)
        self.lineEdit3.setLeftRightLayoutMargin(5, 5)
        self.lineEdit3.setText("delete")
        self.horizontalLayout_3.addWidget(self.lineEdit3)
        # 编辑框4
        lineEdit4 = BaseLineEdit(self)
        lineEdit4.setFixedHeight(50)
        self.horizontalLayout_4.addWidget(lineEdit4)

    def btn3_2Slot(self):
        self.lineEdit3.clear

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