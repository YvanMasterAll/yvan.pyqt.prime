import threading
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

'''
主窗口数据块
'''

class Bloc_Home:

    def set_bloc(self):
        '''
        数据块管理
        '''
        self.titlebar.bloc = Bloc_Titlebar(self.titlebar)
        self.navbar.bloc = Bloc_Navbar(self.navbar)

        self.set_signal()

    def set_signal(self):
        '''
        初始化信号槽
        '''
        print("初始化信号槽...")

    def on_navbar_changed(self, index):
        '''
        导航栏切换事件
        '''
        self.content.setCurrentIndex(index)

class Bloc_Titlebar(QObject):
    def __init__(self, widget):
        super(Bloc_Titlebar, self).__init__()

        self.widget = widget
        self.set_signal()

    def set_signal(self):
        # self.widget.closeButton.clicked.connect(self.widget.parent().close)
        pass

class Bloc_Navbar(QObject):
    on_navbar_changed = pyqtSignal(int)

    def __init__(self, widget):
        super(Bloc_Navbar, self).__init__()

        self.widget = widget
        self.set_signal()

    def set_signal(self):
        self.on_navbar_changed.connect(self.widget.parent().on_navbar_changed)