from PyQt5.QtGui import QIcon, QKeySequence, QColor
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout
from qtpy import QtGui

from bloc.home import Bloc_Home
from view.home.pager import Pager
from view.test1page import Test1Page
from view.test2page import Test2Page
from view.home.navbar import NavBar
from view.home.sidebar import SideBar
from widget.view import BaseView
from widget.base_activity import BaseActivity
from widget.frame.bar.nav_titlebar import NavTitleBar

'''
主页
'''

class HomePage(BaseActivity, Bloc_Home):
    style_name = 'home/index'

    def __init__(self, *args, **kwargs):
        super(HomePage, self).__init__(*args, **kwargs)

        self.procedure()
        self.setMouseTracking(True) # 设置鼠标跟踪，激活窗体拉伸和拖拽
        self.installEventFilter(self) # 设置事件过滤器，激活标题栏缩放

    def set_ui(self):
        self.setObjectName("Home")

        # 标题栏
        self.titlebar = NavTitleBar(self)
        self.bar = self.titlebar
        # 侧边栏
        self.sidebar = SideBar(self)
        # 分页器
        self.pager = Pager()
        self.pager.setObjectName("Pager")

    def place(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout_body = QHBoxLayout()
        self.layout_body.setContentsMargins(0, 0, 0, 0)
        self.layout_content = QVBoxLayout()
        # 标题栏
        self.layout.addWidget(self.titlebar)
        # 侧边栏
        self.layout_body.addWidget(self.sidebar)
        # 分页器
        self.layout_content.addWidget(self.pager)

        self.layout_body.addLayout(self.layout_content)
        self.layout.addLayout(self.layout_body)
        self.addLayout(self.layout)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # 程序关闭
        self.global_bloc.app_closed.emit()