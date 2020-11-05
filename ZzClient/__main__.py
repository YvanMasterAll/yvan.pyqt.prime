from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout
from qtpy.QtCore import Qt
import sys
from ZzClient.config.theme import Theme
from ZzClient.common.util.func import handle_error
from ZzClient.common.loader.inspector import ConnectStyleSheetInspector
from ZzClient.config.const import Config
from ZzClient.widget.application import QSingleApplication
from ZzClient.view.home.index import HomePage
import cgitb
import os
from loader.resource import ResourceLoader

def start():
    app = QSingleApplication("zzclient", sys.argv)
    # 异常捕获
    os.makedirs(Config().except_path, exist_ok=True)
    sys.excepthook = cgitb.Hook(1, Config().except_path, 5, sys.stderr, '')
    if app.isRunning():
        # 激活窗口
        app.sendMessage('show', 1000)
    else:
        # 窗口关闭程序退出
        app.setQuitOnLastWindowClosed(True)
        # 应用图标
        app.setWindowIcon(ResourceLoader().qt_icon_project_ico)
        # 设置字体
        # fontDB = QFontDatabase()
        # fontDB.addApplicationFont(':/font/Roboto-Regular.ttf')
        # app.setFont(QFont('Roboto'))
        # 设置主题样式
        Theme.load()
        window = HomePage()
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
        # TODO 初始化操作
        start()
    except SystemExit:
        pass
    except BaseException as e:
        handle_error(e)