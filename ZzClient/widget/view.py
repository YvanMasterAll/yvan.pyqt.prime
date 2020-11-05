import abc
from PyQt5.QtWidgets import QWidget, QFrame
from qtpy import QtCore

from ZzClient.common.loader.resource import ResourceLoader
from ZzClient.bloc.app import Bloc_App
from ZzClient.config.const import Config
from ZzClient.config.theme import Theme

'''
页面基类
'''

class BaseView(QWidget):
    '''
    静态资源管理器
    '''
    resource: ResourceLoader = ResourceLoader()
    '''
    全局数据块
    '''
    global_bloc: Bloc_App = Bloc_App()
    '''
    配置对象
    '''
    config = Config()
    '''
    主题对象
    '''
    theme = Theme()

    def set_style(self, name):
        '''
        设置样式
        https://stackoverflow.com/questions/31178695/qt-stylesheet-not-working
        '''
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        with open(Config().qss_path + '/' + name + '.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def procedure(self):
        '''
        初始化流程，set_ui > place > configure > set_signal
        '''
        if hasattr(self, 'set_ui'):
            self.set_ui()
        if hasattr(self, 'place'):
            self.place()
        if hasattr(self, 'configure'):
            self.configure()
        if hasattr(self, 'set_bloc'):
            self.set_bloc()
