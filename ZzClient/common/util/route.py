import threading
import os
from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class Navigation:
    def __init__(self, path, name):
        self.path = path
        self.name = name

'''
路由管理器
'''

class RouteManager(QObject):
    # 单例添加线程锁
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例
        '''
        if not hasattr(RouteManager, "_instance"):
            with RouteManager._instance_lock:
                if not hasattr(RouteManager, "_instance"):
                    RouteManager._instance = QObject.__new__(cls)
        return RouteManager._instance

    # 路由栈
    __stack = []
    __stack_threshold = 100
    # 路由
    __routes = []
    # 菜单
    __menus = []
    # 信号
    on_navigation_changed = pyqtSignal(Navigation)
    on_module_loaded = pyqtSignal(list)

    def get_current_menu(self, navigation: Navigation):
        '''
        当前要显示的菜单
        '''
        menu = None
        for root in self.__menus:
            root_children = root['children']
            for m in root_children:
                if navigation.name == m['name']:
                    menu = root

        return menu

    def load_modules(self, routes=[], menus=[]):
        '''
        模块初始化
        '''
        self.__routes = routes
        self.__menus = menus
        # 发送通知
        timer = QTimer(self)
        timer.singleShot(0, lambda :self.on_module_loaded.emit(self.__routes))

    def navigate_to(self, route_name):
        '''
        导航
        '''
        navigation = Navigation(name=None, path=None)
        match = False
        # 0).匹配路由
        for route in self.__routes:
            _route_name = route_name
            # 0.1).如果是根路由匹配redirect
            if route_name == route['name'] and route['redirect'] != None:
                _route_name = route['redirect']['name']
            route_children = route['children']
            # 0.2).匹配子路由
            for r in route_children:
                if r['name'] == _route_name:
                    match = True
                    navigation.name = _route_name
                    navigation.path = '{root}/{path}'.format(root=route['path'], path=r['path'])
        if match:
            # 1).将路由添加到栈
            self.__stack.append(navigation)
            # 2).发送通知
            self.on_navigation_changed.emit(navigation)
            # 3).如果栈满自动清除旧路由
            while len(self.__stack) > self.__stack_threshold:
                del self.__stack[0]










