from PyQt5.QtGui import QIcon, QKeySequence, QFontDatabase, QFont
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout, QDesktopWidget, QVBoxLayout
from qtpy.QtCore import Qt
import sys
from config.theme import Theme
from common.util.func import handle_error
from common.loader.inspector import ConnectStyleSheetInspector
from config.const import Config
from widget.application import QSingleApplication
from ZzClient.view.home.index import HomePage
import cgitb
import os
from common.loader.resource import ResourceLoader

'''
待添加组件
- 全局Loading
- 表单 + 查询
- 列表 + 分页
- 列表 + 刷新
- 模态层
- Toast + Popmenu + Dropmenu + 通知
- Drawer
- 树结构
- Tabbar
'''

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
        # 设置主题样式
        Theme.load()
        # 设置字体
        # fontDB = QFontDatabase()
        # fontDB.addApplicationFont(':/font/Roboto-Regular.ttf')
        # app.setFont(QFont('Roboto'))
        # 设置雅黑字体
        # fontDB = QFontDatabase()
        # fontDB.addApplicationFont('../resources/font/Microsoft-YaHei.ttf')
        # app.setFont(QFont('Microsoft YaHei'))
        # 图标字体
        ResourceLoader.load_icon_font()
        # 加载模块
        ResourceLoader.load_modules()
        # 创建窗体
        window = HomePage()
        window.resize(1024 ,768)
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