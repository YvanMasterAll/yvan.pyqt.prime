import asyncio
import sys

import qtawesome
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer, QRect, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient, QFontMetrics
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QLabel, QStyle, \
    QSizePolicy
from qtpy import QtCore, QtWidgets, QtGui
import resources.qss.theme.dark.style_rc
from bloc.app import Bloc_App
from common.loader.resource import ResourceLoader
from common.util.worker import Worker
from config.theme import Theme
from test.widget.dialog._dialog_custom_form import Ui_Dialog_Custom_Form
from view.home.sidebar import SideBar
from widget.activity.modal.custom_dialog import CustomDialog
from widget.base_activity import BaseActivity
from widget.dialog import SysDialog
from widget.frame.bar.dialog_titlebar import DialogTitleBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.view import BaseView

Style = '''
Window, Window2 {
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

        btn1 = QPushButton()
        btn1.setText("点我")
        layout.addWidget(btn1)
        btn1.clicked.connect(self.on_click1)

        btn1 = QPushButton()
        btn1.setText("点我")
        layout.addWidget(btn1)
        btn1.clicked.connect(self.on_click2)

        btn1 = QPushButton()
        btn1.setText("点我")
        layout.addWidget(btn1)
        btn1.clicked.connect(self.on_click3)

        btn1 = QPushButton()
        btn1.setText("点我")
        layout.addWidget(btn1)
        btn1.clicked.connect(self.on_click4)

        btn1 = QPushButton()
        btn1.setText("点我")
        layout.addWidget(btn1)
        btn1.clicked.connect(self.on_click5)

    def on_click1(self):
        SysDialog.show(SysDialog.INFO, "这是一个简单的信息提示窗", confirm=lambda :print('点击了确认'), )

    def on_click2(self):
        SysDialog.show(SysDialog.WARN, "这是一个警告提示框", confirm=lambda :print('点击了确认'), )

    def on_click3(self):
        SysDialog.show(SysDialog.ERROR, "这是一个错误提示框", confirm=lambda :print('点击了确认'), )

    def on_click4(self):
        SysDialog.show(SysDialog.PROMOT, "这是一个确认框", confirm=lambda :print('点击了确认'), cancel=lambda :print("点击了取消"))

    def on_click5(self):
        SysDialog.show(SysDialog.WARN_PROMOT, "这是一个警告确认框", confirm=lambda :print('点击了确认'), cancel=lambda :print("点击了取消"))

class CustomWidget(QWidget, Ui_Dialog_Custom_Form):
    def __init__(self, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)

        self.setupUi(self)

class Window2(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window2, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        self.setStyleSheet(Style)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        btn = QPushButton()
        btn.setText("打开确认框")
        layout.addWidget(btn)
        # 确认框
        # dialog = CustomDialog(msg="你确定要执行该操作吗，这个操作可能会造成不可逆伤害！如果确定请点击确定按钮。")
        # dialog.on_confirm.connect(lambda :print("点击了确认按钮"))
        # dialog.on_cancel.connect(lambda: print("点击了取消按钮"))
        # btn.clicked.connect(dialog.show)
        # 自定义控件
        dialog = CustomDialog(widget=CustomWidget(), type=CustomDialog.CUSTOM, width=500)
        async def task():
            print('执行异步工作')
            await asyncio.sleep(4)
            dialog.hide_vloading()
        def callback():
            print('点击了确定按钮')
            Worker().run_task(task())
            dialog.show_vloading()
        dialog.on_confirm.connect(callback)
        dialog.on_cancel.connect(lambda: print("点击了取消按钮"))
        btn.clicked.connect(dialog.show)

        self.setLayout(layout)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        Bloc_App().app_closed.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    app.setFont(ResourceLoader.load_app_font())
    # 自定义对话框
    window = Window2()
    # 系统对话框
    # window = Window()
    window.show()

    sys.exit(app.exec_())