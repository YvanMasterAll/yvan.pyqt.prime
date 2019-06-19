from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QKeySequence
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QApplication, QDesktopWidget, QVBoxLayout
from qtpy.QtCore import Qt
from window import QUnFrameWindow
import sys
from titlebar import Titlebar
from bloc import Bloc_Window
from navbar import Navbar
from test1page import Test1Page
from test2page import Test2Page
import styles
from base import setStyle, initialize, handle_error, Const, ConnectStyleSheetInspector
from application import QSingleApplication
import cgitb
import os

class Window(QUnFrameWindow, Bloc_Window):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setupUI()
        self.setupLayouts()
        self.setupContents()
        self._setupBlocs() # 初始化数据块
        self._setMouseTracking() # 设置鼠标跟踪

    def setupUI(self):
        self.setObjectName("Window")
        self.setWindowIcon(QIcon('resource/icons/favicon.ico'))
        setStyle("window", self)

        # 标题栏
        self.titlebar = Titlebar(self)
        # 左侧导航
        self.navbar = Navbar(self)
        # 主体内容
        self.content = QStackedWidget()
        self.content.setObjectName("Pager")
        self.content_test1 = Test1Page(self)
        self.content_test1.setObjectName("Test1Page")
        self.content_test2 = Test2Page(self)
        self.content_test2.setObjectName("Test2Page")

    def setupContents(self):
        # 分页管理
        self.content.addWidget(self.content_test1)
        self.content.addWidget(self.content_test2)
        self.content.setCurrentIndex(1)

    def setupLayouts(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.titlebar)

        self.layout_content = QHBoxLayout()
        self.layout_content.addWidget(self.navbar)
        self.layout_content.addWidget(self.content)

        self.layout.addLayout(self.layout_content)
        self.addLayout(self.layout)

def start():
    app = QSingleApplication("zzclient", sys.argv)
    # 异常捕获
    os.makedirs(Const.except_file, exist_ok=True)
    sys.excepthook = cgitb.Hook(1, Const.except_file, 5, sys.stderr, '')
    if app.isRunning():
        # 激活窗口
        app.sendMessage('show', 1000)
    else:
        # 窗口关闭程序退出
        app.setQuitOnLastWindowClosed(True)
        # 应用图标
        app.setWindowIcon(QIcon('resources/icons/app.svg'))
        # 设置字体
        # fontDB = QFontDatabase()
        # fontDB.addApplicationFont(':/fonts/Roboto-Regular.ttf')
        # app.setFont(QFont('Roboto'))
        # 设置主题样式
        styles.dark(app)
        window = Window()
        # 样式注入器
        ConnectStyleSheetInspector(main_window=window,
                                   shortcut=QKeySequence(Qt.Key_Tab))
        # 计算居中显示的位置
        desktop = QDesktopWidget().availableGeometry()
        width = (desktop.width() - window.width()) / 2
        height = (desktop.height() - window.height()) / 2
        app.setActivationWindow(window)
        window.show()
        window.move(width, height)
        sys.exit(app.exec_())

if __name__ == '__main__':
    try:
        initialize()
        start()
    except SystemExit:
        pass
    except BaseException as e:
        handle_error(e)