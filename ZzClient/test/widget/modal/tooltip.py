import sys

import qtawesome
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QListWidget, \
    QListWidgetItem, QSizePolicy, QLabel
from qtpy import QtCore, QtWidgets, QtGui
import resources.qss.theme.dark.style_rc
from bloc.app import Bloc_App
from common.loader.resource import ResourceLoader
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.activity.modal.tooltip import ToolTip
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
ToolTipMenu QListWidget {
    border: none;
    background-color: transparent;
}
'''

class CustomWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        label = QLabel()
        label.setPixmap(qtawesome.icon('mdi.information-variant', color=ResourceLoader().qt_color_text).pixmap(QSize(28, 28)))
        label2 = QLabel()
        label2.setText("这是一个自定义提示")
        layout.addWidget(label)
        layout.addWidget(label2)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        self.setStyleSheet(Style)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # 普通提示
        btn1 = QPushButton('鼠标悬停1', self, minimumHeight=38)
        btn1.setFixedWidth(100)
        ToolTip.bind(btn1, tip='这是按钮1', direction=ToolTip.LEFT)
        layout.addWidget(btn1)
        # 菜单提示
        btn2 = QPushButton('鼠标悬停2', self, minimumHeight=38)
        btn2.setFixedWidth(100)
        tooltip = ToolTip.bind(btn2, tip='这是按钮2', type=ToolTip.MENU, direction=ToolTip.RIGHT, data=['选项一', '选项二', '选项三'], trigger=ToolTip.CLICK)
        tooltip.on_item_clicked.connect(lambda text:print('点击了按钮：{text}'.format(text=text)))
        layout.addWidget(btn2)
        # 自定义提示
        btn3 = QPushButton('鼠标悬停3', self, minimumHeight=38)
        btn3.setFixedWidth(100)
        ToolTip.bind(btn3, tip='这是按钮3', type=ToolTip.CUSTOM, direction=ToolTip.BOTTOM, widget=CustomWidget())
        layout.addWidget(btn3)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        Bloc_App().app_closed.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    app.setFont(ResourceLoader.load_app_font())
    window = Window()
    window.show()

    sys.exit(app.exec_())