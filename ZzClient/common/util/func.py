import traceback
from .logger import logger_err
import sys

'''
异常处理
'''

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

'''
转义函数
'''

def escape(s):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace('\'', "&#x27;")
    s = s.replace('\n', '<br/>')
    s = s.replace(' ', '&nbsp;')
    return s

'''
打印UI结构
'''

def dumpStructure(widget, space=0):
    '''
    打印UI结构
    :param widget:            父控件
    :param space:             层次缩进
    '''
    print('{}{} : {}'.format(
        ' ' * space, widget.metaObject().className(), widget.objectName()))
    for c in widget.children():
        dumpStructure(c, space + 4)