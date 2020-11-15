import threading

import qtpy
import os

from common.util.storage import LocalStorage

__class_path__ = os.path.abspath(os.path.dirname(__file__))
__root_path__ = os.path.abspath(os.path.join(__class_path__, os.path.pardir))

class Config:
    # 单例添加线程锁
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例
        '''
        if not hasattr(Config, "_instance"):
            with Config._instance_lock:
                if not hasattr(Config, "_instance"):
                    Config._instance = object.__new__(cls)
        return Config._instance

    '''
    属性项
    '''
    sidebar_width    = 170          # 侧边栏宽度
    window_zoom_critical   = 5      # 窗口大小调整边界
    window_shadow_width = 5         # 窗口阴影宽度
    qt_version      = tuple(int(v) for v in qtpy.QT_VERSION.split('.')) # Qt版本

    @property
    def root_path(self) -> str:
        '''项目根路径'''
        return __root_path__

    @property
    def except_path(self):
        '''程序异常记录文件夹'''
        return os.path.join(__root_path__, '.except')

    @property
    def log_path(self):
        '''日志文件'''
        return os.path.join(__root_path__, '.log')

    @property
    def error_path(self):
        '''异常日志文件'''
        return os.path.join(__root_path__, '.error')

    @property
    def resource_path(self):
        '''资源文件夹'''
        return self.link(self.root_path, "resource", not_exists_create=True)

    @property
    def img_path(self):
        '''图片目录'''
        return self.link(self.resource_path, "img/{theme}".format(theme=LocalStorage.themeGet()), not_exists_create=True)

    @property
    def qss_path(self):
        '''样式表目录'''
        return self.link(self.resource_path, "qss", not_exists_create=True)

    @property
    def font_path(self):
        '''字体目录'''
        return self.link(self.resource_path, "font", not_exists_create=True)

    @property
    def icon_path(self):
        '''图标目录'''
        return self.link(self.img_path, "icon", not_exists_create=True)

    @property
    def shadow_path(self):
        '''获取边框阴影的目录所在（此处已经指定了上级目录img所在）'''
        return self.link(self.img_path, "shadow")

    def get_shadow_path(self, name: str) -> str:
        '''获取阴影'''
        return self.link(self.shadow_path, name)

    @staticmethod
    def link(source: str, point: str, not_exists_create=False) -> str:
        '''
        :param not_exists_create: 不存在创建
        :param source: 上级路径
        :param point: 连接路径
        '''
        return Config().path_exists(os.path.join(source, point)) if not_exists_create else os.path.join(source, point)

    @staticmethod
    def path_exists(path: str) -> str:
        '''不存在则创建'''
        if not os.path.exists(path) and "." not in path:
            os.makedirs(path)
        return path

