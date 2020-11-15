from PyQt5.QtCore import Qt, QPointF, QSize
from PyQt5.QtGui import QWindowStateChangeEvent, QFont, QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel, QPushButton, QApplication, QVBoxLayout, QGraphicsBlurEffect, QGraphicsDropShadowEffect
from qtpy import QtGui
from config.const import Config
from test.widget.separator import Separator
from view.home.navbar import NavBar
from widget.view import BaseView

'''
标题栏
'''

class NavTitleBar(BaseView):

    _radius     = 24
    _padding    = 4
    _move_pos   = None
    _height     = 90
    _logo_size  = 80

    def __init__(self, *args, **kwargs):
        super(NavTitleBar, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        self.setObjectName("TitleBar")
        self.setFixedHeight(self._height)

        # header
        self.header = QWidget(self)
        self.header.setObjectName("Header")
        self.header.setFixedWidth(self.config.sidebar_width)
        self.logo = QWidget(self)
        self.logo.setObjectName('Logo')
        self.logo.setFixedWidth(self._logo_size)
        self.logo.setFixedHeight(self._logo_size)
        # 内容
        self.content = QWidget()
        self.content.setObjectName("Content")
        # 侧边栏
        self.navbar = NavBar(self)
        # 最小化，最大化，还原，关闭按钮
        self.buttons = []
        for name, text in (('buttonMinimum', '0'), ('buttonMaximum', '1'),
                           ('buttonNormal', '2'), ('buttonClose', 'r')):
            button = QPushButton(text, self, font=QFont('Webdings'))
            button.setMinimumSize(self._radius, self._radius)
            button.setMaximumSize(self._radius, self._radius)
            button.setObjectName('TitleBar_%s' % name)
            setattr(self, name, button)
            self.buttons.append(button)

    def configure(self):
        # 支持设置背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 找到父控件(或者自身)，self.parent() or self
        self._root = self.parent()
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

    def place(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 2, 0, 0)
        layout1 = QVBoxLayout()
        layout1.setSpacing(0)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout2 = QHBoxLayout()
        layout2.setSpacing(0)
        layout2.setContentsMargins(0, 20, 0, 0)
        layout3 = QHBoxLayout()
        layout3.setSpacing(0)
        layout3.setContentsMargins(0, 2, 4, self._height)
        layout4 = QHBoxLayout()
        layout4.setSpacing(0)
        layout4.setContentsMargins(0, 0, 0, 0)
        layout5 = QVBoxLayout()
        layout5.setSpacing(0)
        layout5.setContentsMargins(0, 0, 0, 0)
        header_layout = QVBoxLayout()

        self.header.setLayout(header_layout)
        header_layout.setContentsMargins((self.config.sidebar_width - self._logo_size)/2, 0, 0, 0)
        header_layout.addWidget(self.logo)
        layout1.addWidget(self.header)
        layout.addLayout(layout1)
        layout2.addWidget(self.navbar)
        layout4.addLayout(layout2)
        for button in self.buttons:
            layout3.addWidget(button)
        layout4.addLayout(layout3)
        layout5.addLayout(layout4)
        self.content.setLayout(layout5)
        layout.addWidget(self.content)

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

    def showMaximizeButton(self, show=True):
        '''
        显示隐藏最大化按钮
        '''
        self.buttonMaximum.setVisible(show)

    def showNormalButton(self, show=True):
        '''
        显示隐藏还原按钮
        '''
        self.buttonNormal.setVisible(show)

    def showEvent(self, event):
        super(NavTitleBar, self).showEvent(event)
        if not self.isResizable():
            self.showMaximizeButton(False)
            self.showNormalButton(False)
        else:
            self.showMaximizeButton(
                self.isMaximizeable() and not self._root.isMaximized())
            self.showNormalButton(self.isMaximizeable()
                                  and self._root.isMaximized())

    def on_window_change(self):
        '''
        双击标题栏最大化
        '''
        if not self.isMaximizeable() or not self.isResizable():
            # 不能最大化或者不能调整大小
            return
        if self._root.isMaximized():
            self._root.showNormal()
        else:
            self._root.showMaximized()

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
