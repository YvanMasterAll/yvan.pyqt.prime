import datetime
import traceback

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFontMetrics, QPainter
from PyQt5.QtWidgets import QWidget, QLayoutItem, QLayout

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

'''
移除所有子部件
'''
def clear_widget(widget: QWidget):
    w = widget.findChild(QWidget)
    while w:
        w.deleteLater()
        del w
        w = widget.findChild(QWidget)

'''
清空布局
'''
def clear_layout(layout:QLayout):
    item = layout.takeAt(0)
    while item:
        w = item.widget()
        l = item.layout()
        if w:
            w.setParent(None)
        if l:
            clear_layout(l)
            l.setParent(None)
        item = layout.takeAt(0)

'''
计算文本尺寸
'''
def calculate_text_width(font, text):
    fm = QFontMetrics(font)
    return fm.width(text)
def calculate_text_height(font):
    fm = QFontMetrics(font)
    return fm.height()
def calculate_text_rect(text, font=None, painter=None, x=0, y=0, flag=Qt.TextSingleLine):
    if not painter and not font:
        return
    if painter:
        fm = QFontMetrics(painter.font())
        rect = fm.boundingRect(QRect(x, y, 0, 0), flag, text)
        return rect
    if font:
        fm = QFontMetrics(font)
        rect = fm.boundingRect(QRect(x, y, 0, 0), flag, text)
        return rect

'''
计算居中位置
'''
def calculate_middle_rect(prect: QRect, width, height, x=None, y=None):
    _w = prect.width()
    _h = prect.height()
    _x = prect.x()
    _y = prect.y()
    if x and y:
        return QRect(x + _x, y + _y, width, height)
    return QRect(_x + (_w - width)/2, _y + (_h - height)/2, width, height)

'''
日期处理
'''
def toDateStr(_datetime=None):
    if _datetime:
        return _datetime.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")