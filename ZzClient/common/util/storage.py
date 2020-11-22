from qtpy.QtCore import QSettings, QTextCodec
import os

'''
本地存储
'''

__class_path__ = os.path.abspath(os.path.dirname(__file__))
__root_path__ = os.path.abspath(os.path.join(__class_path__, os.path.pardir))
__config_path__ = os.path.join(__root_path__, '../config/config.ini')

class Storage:

    instance = None

    @classmethod
    def init(cls, parent=None):
        '''
        初始化配置实例
        :param cls:
        :param parent:
        '''
        if not cls.instance:
            cls.instance = QSettings(__config_path__, QSettings.IniFormat, parent)
            cls.instance.setIniCodec(QTextCodec.codecForName('utf-8'))

    @classmethod
    def value(cls, key, default=None, typ=None):
        '''
        获取配置中的值
        :param cls:
        :param key:        键名
        :param default:    默认值
        :param typ:        类型
        '''
        cls.init()
        if default != None and typ != None:
            return cls.instance.value(key, default, typ)
        if default != None:
            return cls.instance.value(key, default)
        return cls.instance.value(key)

    @classmethod
    def setValue(cls, key, value):
        '''
        更新配置中的值
        :param cls:
        :param key:        键名
        :param value:      键值
        '''
        cls.init()
        cls.instance.setValue(key, value)
        cls.instance.sync()

class LocalStorage:
    @staticmethod
    def get(path, key, default=None):
        return Storage.value(key="{path}/{key}".format(path=path, key=key), default=default)

    @staticmethod
    def set(path, key, value):
        Storage.setValue(key="{path}/{key}".format(path=path, key=key), value=value)

    @staticmethod
    def themeGet():
        '''
        获取主题
        '''
        return LocalStorage.get('App', 'theme', 'dark')

    @staticmethod
    def themeSet(value):
        '''
        设置主题
        '''
        return LocalStorage.set('App', 'theme', value)

    @staticmethod
    def themeAllGet():
        '''
        获取所有主题
        '''
        return LocalStorage.get('App', 'all_theme', '')









