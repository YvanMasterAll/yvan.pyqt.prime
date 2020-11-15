from PyQt5.QtCore import Qt, QPointF, QSize
from PyQt5.QtGui import QWindowStateChangeEvent, QFont, QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel, QPushButton, QApplication
from qtpy import QtGui
from config.const import Config
from widget.view import BaseView

'''
标题栏
'''

class TitleBar(BaseView):

    _radius     = 24
    _padding    = 8
    _move_pos   = None

    def __init__(self, *args, title='', **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        self.title = title
        self.procedure()

    def set_ui(self):
        self.setObjectName("TitleBar")
        self.setMinimumSize(0, self._radius + self._padding)
        self.setMaximumSize(0xFFFFFF, self._radius + self._padding)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(self._padding, 0, self._padding, 0)
        layout.setSpacing(0)
        # 左侧添加4个对应的空白占位
        for i in range(4):
            layout.addItem(QSpacerItem(24, 20, QSizePolicy.Fixed, QSizePolicy.Expanding))
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 标题
        self.labelTitle = QLabel(self, alignment=Qt.AlignCenter)
        self.labelTitle.setObjectName('TitleBar_labelTitle')
        layout.addWidget(self.labelTitle)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 最小化，最大化，还原，关闭按钮
        for name, text in (('buttonMinimum', '0'), ('buttonMaximum', '1'),
                           ('buttonNormal', '2'), ('buttonClose', 'r')):
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
        self._root = self.parent()
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
        super(TitleBar, self).showEvent(event)
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
