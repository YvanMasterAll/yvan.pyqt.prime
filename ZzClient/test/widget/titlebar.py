#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年7月15日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: CustomWidgets.TitleBar
@description: 自定义标题栏
"""

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QWindowStateChangeEvent, QFont, QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel, QPushButton, QApplication, QDialog, QVBoxLayout
from widget.view import BaseView

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'

class TitleBar(BaseView):

    _radius     = 38
    _move_pos   = None

    def __init__(self, *args, title='', **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.title = title
        self.procedure()

    def set_ui(self):
        self.setMinimumSize(0, self._radius)
        self.setMaximumSize(0xFFFFFF, self._radius)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # 左侧添加4个对应的空白占位
        for name in ('widgetMinimum', 'widgetMaximum', 'widgetNormal', 'widgetClose'):
            widget = QWidget(self)
            widget.setMinimumSize(self._radius, self._radius)
            widget.setMaximumSize(self._radius, self._radius)
            widget.setObjectName('TitleBar_%s' % name)
            setattr(self, name, widget)
            layout.addWidget(widget)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 标题
        self.labelTitle = QLabel(self, alignment=Qt.AlignCenter)
        self.labelTitle.setObjectName('TitleBar_labelTitle')
        layout.addWidget(self.labelTitle)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 最小化，最大化，还原，关闭按钮
        for name, text in (('buttonMinimum', '0'), ('buttonMaximum', '1'), ('buttonNormal', '2'), ('buttonClose', 'r')):
            button = QPushButton(text, self, font=QFont('Webdings'))
            button.setMinimumSize(self._radius, self._radius)
            button.setMaximumSize(self._radius, self._radius)
            button.setObjectName('TitleBar_%s' % name)
            setattr(self, name, button)
            layout.addWidget(button)

    def configure(self):
         # 支持设置背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 找到父控件(或者自身)，self.parent() or self
        self._root = self.window()
        # 设置标题
        self.labelTitle.setText(self.title)
        # 是否需要隐藏最小化或者最大化按钮
        self.showMinimizeButton(self.isMinimizeable())
        self.showNormalButton(False)
        self.showMaximizeButton(self.isMaximizeable())
        # 绑定信号
        self._root.windowTitleChanged.connect(self.setWindowTitle)
        self.buttonMinimum.clicked.connect(self.showMinimized)
        self.buttonMaximum.clicked.connect(self.showMaximized)
        self.buttonNormal.clicked.connect(self.showNormal)
        self.buttonClose.clicked.connect(self._root.close)
        # 对父控件(或者自身)安装事件过滤器
        self._root.installEventFilter(self)

    def showMinimized(self):
        self._root.showMinimized()
        # 强制取消hover状态
        QApplication.sendEvent(self.buttonMinimum, QMouseEvent(QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def showNormal(self):
        self._root.showNormal()
        # 强制取消hover状态
        QApplication.sendEvent(self.buttonMaximum, QMouseEvent(QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def showMaximized(self):
        self._root.showMaximized()
        # 强制取消hover状态
        QApplication.sendEvent(self.buttonNormal, QMouseEvent(QMouseEvent.Leave, QPointF(), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def isMinimizeable(self):
        '''
        是否可以最小化
        '''
        return self.testWindowFlags(Qt.WindowMinimizeButtonHint)

    def isMaximizeable(self):
        '''
        是否可以最大化
        '''
        return self.testWindowFlags(Qt.WindowMaximizeButtonHint)

    def isResizable(self):
        '''
        是否可调整
        '''
        return self._root.minimumSize() != self._root.maximumSize()

    def showMinimizeButton(self, show=True):
        '''
        显示隐藏最小化按钮
        '''
        self.buttonMinimum.setVisible(show)
        self.widgetMinimum.setVisible(show)

    def showMaximizeButton(self, show=True):
        '''
        显示隐藏最大化按钮
        '''
        self.buttonMaximum.setVisible(show)
        self.widgetMaximum.setVisible(show)

    def showNormalButton(self, show=True):
        '''
        显示隐藏还原按钮
        '''
        self.buttonNormal.setVisible(show)
        self.widgetNormal.setVisible(show)

    def showEvent(self, event):
        super(TitleBar, self).showEvent(event)
        if not self.isResizable():
            self.showMaximizeButton(False)
            self.showNormalButton(False)
        else:
            self.showMaximizeButton(
                self.isMaximizeable() and not self._root.isMaximized())
            self.showNormalButton(self.isMaximizeable()
                                  and self._root.isMaximized())

    def eventFilter(self, target, event):
        if isinstance(event, QWindowStateChangeEvent):
            if self._root.isVisible() and not self._root.isMinimized() and \
                    self.testWindowFlags(Qt.WindowMinMaxButtonsHint):
                # 如果当前是最大化则隐藏最大化按钮
                maximized = self._root.isMaximized()
                self.showMaximizeButton(not maximized)
                self.showNormalButton(maximized)
                # 修复最大化边距空白问题
                if maximized:
                    self._oldMargins = self._root.layout().getContentsMargins()
                    self._root.layout().setContentsMargins(0, 0, 0, 0)
                else:
                    if hasattr(self, '_oldMargins'):
                        self._root.layout().setContentsMargins(*self._oldMargins)
        return super(TitleBar, self).eventFilter(target, event)

    def testWindowFlags(self, windowFlags):
        '''
        判断当前窗口是否有该flags
        '''
        return bool(self._root.windowFlags() & windowFlags)

    def setWindowTitle(self, title):
        '''
        设置标题
        '''
        self.labelTitle.setText(title)

__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'


class TestTitleBarBase:

    def __init__(self, *args, **kwargs):
        super(TestTitleBarBase, self).__init__(*args, **kwargs)
        self.resize(500, 400)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        # 添加自定义标题栏
        layout.addWidget(TitleBar(self, title='TitleBar'))
        # 底部空白占位
        layout.addWidget(QWidget(self, objectName='bottomWidget'))


class TestTitleBarWidget(QWidget, TestTitleBarBase):
    pass


class TestTitleBarDialog(QDialog, TestTitleBarBase):
    pass


# 标题栏样式
Style = """
/*标题栏颜色*/
TitleBar {
    background: rgb(65, 148, 216);
}

/*标题栏圆角*/
TitleBar {
    border-top-right-radius: 10px;
    border-top-left-radius: 10px;
}

#TitleBar_buttonClose {
    /*需要把右侧的关闭按钮考虑进去*/
    border-top-right-radius: 10px;
}

/*底部圆角和背景*/
#bottomWidget {
    background: white;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

/*最小化、最大化、还原按钮*/
TitleBar > QPushButton {
    background: transparent;
}
TitleBar > QPushButton:hover {
    background: rgba(0, 0, 0, 30);
}
TitleBar > QPushButton:pressed {
    background: rgba(0, 0, 0, 60);
}

/*关闭按钮*/
#TitleBar_buttonClose:hover {
    color: white;
    background: rgb(232, 17, 35);
}
#TitleBar_buttonClose:pressed {
    color: white;
    background: rgb(165, 69, 106);
}
"""

if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    w = TestTitleBarWidget()
    w.show()

    # 模态属性
    w1 = TestTitleBarDialog()
    w1.setWindowTitle('对话框')
    w1.show()

    # 不可调整大小
    w2 = TestTitleBarWidget()
    w2.setWindowTitle('不可调整大小')
    w2.setMinimumSize(400, 400)
    w2.setMaximumSize(400, 400)
    w2.show()
    sys.exit(app.exec_())