import asyncio
import threading
from PyQt5.QtCore import QObject
from bloc.app import Bloc_App

'''
异步编程
'''

class Worker(QObject):
    # 单例线程锁
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例
        '''
        if not hasattr(Worker, "_instance"):
            with Worker._instance_lock:
                if not hasattr(Worker, "_instance"):
                    Worker._instance = QObject.__new__(cls)
                    Worker._instance.setup()
        return Worker._instance

    def setup(self):
        self.loop = asyncio.get_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()
        # 当程序退出时关闭线程
        Bloc_App().app_closed.connect(self.close)

    def close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        self.loop.run_forever()

    def run_task(self, coroutine):
        asyncio.run_coroutine_threadsafe(coroutine, self.loop)