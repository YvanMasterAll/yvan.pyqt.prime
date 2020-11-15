from PyQt5.QtCore import pyqtSignal, QObject
from common.util.http import request, Result, ResultCode, ResultSet

'''
测试aiohttp
'''

def request_test():
    result = request("https://easy-mock.com/mock/5d0992c92fdcca04c50de0bb/api/v1/test", "get")
    try:
        json = result.json
        _result = Result(json)
        signals.signal_test.emit(_result, _result.code)
    except:
        signals.signal_test.emit(Result(None), ResultSet.jsonIllegal)

class Signals(QObject):
    signal_test = pyqtSignal(Result, ResultCode)

def response_test(result, code):
    if code.valid:
        print(result.dict)
    else:
        print(code.msg)

signals = Signals()
signals.signal_test.connect(response_test)
request_test()

'''
测试quamash
在这个例子中, 协程放在全局环境, 不会阻塞到主线程, 所以, 我觉得封装后的网络请求应该也不会阻塞主线程, 通过信号通知的方式达到异步编程
'''

# import sys
# import asyncio
# import time
# from PyQt5.QtWidgets import QApplication, QProgressBar, QWidget, QMainWindow, QVBoxLayout, QPushButton
# from quamash import QEventLoop, QThreadExecutor
#
# class Window(QMainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#
#         widget = QWidget(self)
#         self.layout = QVBoxLayout(widget)
#         button = QPushButton("hello")
#         self.layout.addWidget(button)
#         self.setCentralWidget(widget)
#
#     def run(self):
#         for i in range(5):
#             self.loop.run_until_complete(self.hello())
#
#     async def hello(self):
#         for i in range(5):
#             await asyncio.sleep(1)
#             print("Helo World:%s" % time.time())
#
# app = QApplication(sys.argv)
#
# loop = QEventLoop()
# asyncio.set_event_loop(loop)  # NEW must set the event loop
# progress = QProgressBar()
# progress.setRange(0, 99)
#
# home = Window()
# home.layout.addWidget(progress)
# home.show()
#
# async def master():
#     # await first_50()
#     await home.hello()
#     with QThreadExecutor(1) as exec:
#         await loop.run_in_executor(exec, last_50)
#     # TODO announce completion?
#
# async def first_50():
#     for i in range(50):
#         progress.setValue(i)
#         await asyncio.sleep(.1)
#
# def last_50():
#     for i in range(50,100):
#         loop.call_soon_threadsafe(progress.setValue, i)
#         time.sleep(.1)
#
# with loop: ## context manager calls .close() when loop completes, and releases all resource
#     loop.run_until_complete(master())

'''
测试协程阻塞主线程
'''

# from qtpy.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QTextEdit
# import asyncio, threading, time, sys
#
# class Window(QMainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#
#         widget = QWidget(self)
#         layout = QVBoxLayout(widget)
#         button = QPushButton("hello")
#         layout.addWidget(button)
#         self.setCentralWidget(widget)
#
#         self.loop = asyncio.get_event_loop()
#         self.run()
#
#     def run(self):
#         for i in range(5):
#             self.loop.run_until_complete(self.hello())
#
#     async def hello(self):
#         await asyncio.sleep(1)
#         print("Helo World:%s" % time.time())

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     home = Window()
#     home.show()
#
#     sys.exit(app.exec_())

'''
测试线程结合协程解决阻塞问题实现
'''

# from qtpy.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGridLayout, QTextEdit
# import asyncio, threading, time, sys
#
# class Window(QMainWindow):
#     def __init__(self, parent=None):
#         QMainWindow.__init__(self, parent)
#
#         widget = QWidget(self)
#         layout = QVBoxLayout(widget)
#         button = QPushButton("hello")
#         layout.addWidget(button)
#         self.setCentralWidget(widget)
#
#         coroutine1 = self.func(3)
#         coroutine2 = self.func(2)
#         coroutine3 = self.func(1)
#
#         new_loop = asyncio.new_event_loop()  # 在当前线程下创建时间循环，（未启用），在start_loop里面启动它
#         t = threading.Thread(target=self.start_loop, args=(new_loop,))  # 通过当前线程开启新的线程去启动事件循环
#         t.start()
#
#         asyncio.run_coroutine_threadsafe(coroutine1, new_loop)  # 这几个是关键，代表在新线程中事件循环不断“游走”执行
#         asyncio.run_coroutine_threadsafe(coroutine2, new_loop)
#         asyncio.run_coroutine_threadsafe(coroutine3, new_loop)
#
#         for i in "iloveu":
#             print(str(i) + "    ")
#
#     # 定义一个专门创建事件循环loop的函数，在另一个线程中启动它
#     def start_loop(self, loop):
#         asyncio.set_event_loop(loop)
#         loop.run_forever()
#
#     # 需要执行的耗时异步任务
#     async def func(self, num):
#         print(f'准备调用func,大约耗时{num}')
#         await asyncio.sleep(num)
#         print(f'耗时{num}之后,func函数运行结束')
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     home = Window()
#     home.show()
#
#     sys.exit(app.exec_())

# 输入如下:
# i
# l
# o
# v
# e
# u
# 准备调用func,大约耗时3
# 准备调用func,大约耗时2
# 准备调用func,大约耗时1
# 耗时1之后,func函数运行结束
# 耗时2之后,func函数运行结束
# 耗时3之后,func函数运行结束

