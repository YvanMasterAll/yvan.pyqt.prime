from qtpy.QtGui import QFont
import qtpy
import logging
import traceback
import sys
from qtpy.QtCore import QSettings, QTextCodec
from qtpy.QtWidgets import QShortcut
from qtpy.QtCore import Qt

# 全局方法

def initialize():
    print("执行初始化工作...")

class Const:
    # 常用尺寸
    navbar_width    = 100

    # Qt版本
    qt_version      = tuple(int(v) for v in qtpy.QT_VERSION.split('.'))

    # 配置目录
    env_file        = '.env'
    except_file     = '.except_file'
    log_file        = '.log'
    error_file      = '.error'

def setStyle(name, widget):
    with open('qss/' + name + '.qss', 'r', encoding='utf-8') as f:
        widget.setStyleSheet(f.read())

# 日志记录

logger = logging.getLogger("debug")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(Const.log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)

logger_err = logging.getLogger("error")
logger_err.setLevel(logging.ERROR)
handler_err = logging.FileHandler(Const.error_file)
handler_err.setLevel(logging.ERROR)
handler_err.setFormatter(formatter)
console_err = logging.StreamHandler()
console_err.setLevel(logging.ERROR)
console_err.setFormatter(formatter)
logger_err.addHandler(handler_err)
logger_err.addHandler(console_err)

# 异常处理

def handle_error(e):
    # TODO: 将异常信息记录到日志中
    if isinstance(e, BaseException):
        logger_err.error(traceback.format_exc())
        show_error(traceback.format_exc())

def show_error(message):
    from PyQt5.QtWidgets import QApplication, QErrorMessage, QCheckBox, QPushButton, QLabel, QStyle
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    # 当前窗口关闭程序退出
    app.setQuitOnLastWindowClosed(True)
    # 设置内置错误图标
    app.setWindowIcon(app.style().standardIcon(QStyle.SP_MessageBoxCritical))
    w = QErrorMessage()
    w.finished.connect(lambda _: app.quit)
    w.resize(600, 400)
    # 去掉右上角?
    w.setWindowFlags(w.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    w.setWindowTitle(w.tr('Error'))
    # 隐藏图标、勾选框、按钮
    w.findChild(QLabel, '').setVisible(False)
    w.findChild(QCheckBox, '').setVisible(False)
    w.findChild(QPushButton, '').setVisible(False)
    w.showMessage(escape(message))
    sys.exit(app.exec_())

# 转义方法

def escape(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace('\'', "&#x27;")
    s = s.replace('\n', '<br/>')
    s = s.replace(' ', '&nbsp;')
    return s

# 本地环境

class Setting:

    _Setting = None

    @classmethod
    def init(cls, parent=None):
        """初始化配置实例
        :param cls:
        :param parent:
        """
        if not cls._Setting:
            cls._Setting = QSettings(Const.env_file, QSettings.IniFormat, parent)
            cls._Setting.setIniCodec(QTextCodec.codecForName('utf-8'))

    @classmethod
    def value(cls, key, default=None, typ=None):
        """获取配置中的值
        :param cls:
        :param key:        键名
        :param default:    默认值
        :param typ:        类型
        """
        cls.init()
        if default != None and typ != None:
            return cls._Setting.value(key, default, typ)
        if default != None:
            return cls._Setting.value(key, default)
        return cls._Setting.value(key)

    @classmethod
    def setValue(cls, key, value):
        """更新配置中的值
        :param cls:
        :param key:        键名
        :param value:      键值
        """
        cls.init()
        cls._Setting.setValue(key, value)
        cls._Setting.sync()

# 打印UI结构

def dumpStructure(widget, space=0):
    """打印UI结构
    :param widget:            父控件
    :param space:             层次缩进
    """
    print('{}{} : {}'.format(
        ' ' * space, widget.metaObject().className(), widget.objectName()))
    for c in widget.children():
        dumpStructure(c, space + 4)

# 样式注入器

class ConnectStyleSheetInspector(object):

    def __init__(self, main_window, shortcut):
        self.shortcut = shortcut
        self.main_window = main_window
        shortcut_ = QShortcut(self.shortcut, main_window)
        shortcut_.setContext(Qt.ApplicationShortcut)

        def ShowStyleSheetEditor():
            style_sheet_inspector_class = GetStyleSheetInspectorClass()
            style_sheet_inspector = [
                c for c in self.main_window.children() if
                isinstance(c, style_sheet_inspector_class)]
            if style_sheet_inspector:
                style_sheet_inspector = style_sheet_inspector[0]
            else:
                style_sheet_inspector = style_sheet_inspector_class(self.main_window)
                style_sheet_inspector.setFixedSize(600, 400)
            style_sheet_inspector.show()

        shortcut_.activated.connect(ShowStyleSheetEditor)

def GetStyleSheetInspectorClass():
    """
    Indirection mostly to simplify tests.
    """
    try:
        from qt_style_sheet_inspector import StyleSheetInspector
    except ImportError as error:
        msg = 'You need to Install qt_style_sheet_inspector.'
        raise RuntimeError(msg)
    return StyleSheetInspector