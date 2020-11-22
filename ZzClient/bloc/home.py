import threading
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtCore import pyqtSignal
from bloc.base_bloc import BaseBloc
from common.util.route import Navigation

'''
主窗口数据块
'''

class Bloc_Home(BaseBloc):

    def set_bloc(self):
        '''数据块管理'''
        pass

    def set_signal(self):
        # 导航变更事件
        self.router.on_navigation_changed.connect(self.__on_navigation_changed)

    def __on_navigation_changed(self, navigation: Navigation):
        # 根据导航显示指定页面
        self.pager.show_page(navigation)

class Bloc_Navbar(BaseBloc, QObject):
    def __init__(self, *args, **kwargs):
        super(Bloc_Navbar, self).__init__(*args, **kwargs)

    def set_signal(self):
        # 模块初始化事件
        self.router.on_module_loaded.connect(self.on_module_loaded)

class Bloc_SideBar(BaseBloc, QObject):

    def __init__(self, *args, **kwargs):
        super(Bloc_SideBar, self).__init__(*args, **kwargs)

    def set_signal(self):
        # 导航变更事件
        self.router.on_navigation_changed.connect(self.__on_navigation_changed)

    def __on_navigation_changed(self, navigation: Navigation):
        # 1).获取要显示的菜单
        menu = self.router.get_current_menu(navigation)
        # 2).判断重复点击
        reload = True
        if menu == self.menu:
            reload = False
        self.on_navigation_changed(navigation, menu, reload)