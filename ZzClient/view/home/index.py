from PyQt5.QtGui import QIcon, QKeySequence, QColor
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout
from ZzClient.bloc.home import Bloc_Home
from home.navbar import Navbar
from test1page import Test1Page
from test2page import Test2Page
from ZzClient.widget.view import BaseView
from ZzClient.widget.base_activity import BaseActivity
from ZzClient.widget.frame.bar.titlebar import TitleBar

'''
主页
'''

class HomePage(BaseActivity, Bloc_Home):
    def __init__(self, *args, **kwargs):
        super(HomePage, self).__init__(*args, **kwargs)

        self.procedure()
        self.setMouseTracking(True) # 设置鼠标跟踪，激活窗体拉伸和拖拽
        self.installEventFilter(self) # 设置事件过滤器，激活标题栏缩放

    def set_ui(self):
        self.setObjectName("Home")
        self.setWindowIcon(QIcon('resource/img/favicon.ico'))
        self.set_style('home/index')

        # 标题栏
        self.titlebar = TitleBar(self, title="主页")
        self.bar = self.titlebar
        # 左侧导航
        self.navbar = Navbar(self)
        # 主体内容
        self.content = QStackedWidget()
        self.content.setObjectName("Pager")
        self.content_test1 = Test1Page(self)
        self.content_test1.setObjectName("Test1Page")
        self.content_test2 = Test2Page(self)
        self.content_test2.setObjectName("Test2Page")
        # 分页管理
        self.content.addWidget(self.content_test1)
        self.content.addWidget(self.content_test2)
        self.content.setCurrentIndex(1)

    def place(self):
        self.layout = QVBoxLayout()
        # 标题栏
        self.layout.addWidget(self.titlebar)

        self.layout_content = QHBoxLayout()
        self.layout_content.addWidget(self.navbar)
        self.layout_content.addWidget(self.content)

        self.layout.addLayout(self.layout_content)
        self.addLayout(self.layout)