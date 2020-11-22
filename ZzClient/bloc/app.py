import threading
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

'''
全局数据块
问题：这里采用了另外一种单例模式，用内部类实现单例，如果使用之前的单例模式，会出现静态成员变量不唯一的现象 => Bloc_App().app_closed绑定信号槽后接收不到信号量
'''

class Bloc_App(QObject):
    '''
    单例模式
    '''
    class _A(QObject):
        '''
        全局信号槽
        '''
        app_closed = pyqtSignal()
        signin = pyqtSignal()
        signout = pyqtSignal()

        def display(self):
            '''
            返回当前实例的ID，是全局唯一的
            '''
            return id(self)

    # 单例线程锁
    _instance_lock = threading.Lock()

    def __init__(self):
        super(Bloc_App, self).__init__()

        if not hasattr(Bloc_App, "_instance"):
            with Bloc_App._instance_lock:
                if not hasattr(Bloc_App, "_instance"):
                    Bloc_App._instance = Bloc_App._A()

    def __getattr__(self, attr):
        '''
        代理_A的所有成员变量和成员方法
        '''
        return getattr(self._instance, attr)

