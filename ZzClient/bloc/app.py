import threading
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal

'''
全局数据块
'''

class Bloc_App(QObject):
    '''
    全局信号槽
    '''
    signin      = pyqtSignal()
    signout     = pyqtSignal()

    # 单例线程锁
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例
        '''
        if not hasattr(Bloc_App, "_instance"):
            with Bloc_App._instance_lock:
                if not hasattr(Bloc_App, "_instance"):
                    Bloc_App._instance = QObject.__new__(cls)
        return Bloc_App._instance
