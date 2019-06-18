from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from tooltip import ToolTip

# 全局信号

class _Signals(QObject):

    # 登录状态
    signin      = pyqtSignal()
    signout     = pyqtSignal()

Signals = _Signals()

"""数据块"""

# 主窗口

class Bloc_Window:

    def _setupBlocs(self):
        # 数据管理
        self.titlebar.bloc = Bloc_Titlebar(self.titlebar)
        self.navbar.bloc = Bloc_Navbar(self.navbar)

        self._setupSignals()

    def _setupSignals(self):
        # 初始化信号槽
        print("初始化信号槽...")

    def _showNotice(self, message, timeout=2000):
        """底部提示消息
        :param message:        提示消息
        """
        if hasattr(self, '_tip'):
            self._tip._hideTimer.stop()
            self._tip.close()
            self._tip.deleteLater()
            del self._tip
        self._tip = ToolTip()
        self._tip.setText(message)
        self._tip.show()
        self._tip.move(
            self.pos().x() + int((self.width() - self._tip.width()) / 2),
            self.pos().y() + self.height() - 60,
        )
        self._tip._hideTimer.timeout.connect(self._tip.close)
        self._tip._hideTimer.start(timeout)

    def on_navbar_changed(self, index):
        # 导航栏切换事件
        self.content.setCurrentIndex(index)

# 标题栏

class Bloc_Titlebar(QObject):
    def __init__(self, widget):
        super(Bloc_Titlebar, self).__init__()

        self.widget = widget
        self._setupSignals()

    def _setupSignals(self):
        self.widget.closeButton.clicked.connect(self.widget.parent.close)

# 左侧导航

class Bloc_Navbar(QObject):
    on_navbar_changed = pyqtSignal(int)

    def __init__(self, widget):
        super(Bloc_Navbar, self).__init__()

        self.widget = widget
        self._setupSignals()

    def _setupSignals(self):
        self.on_navbar_changed.connect(self.widget.parent.on_navbar_changed)

