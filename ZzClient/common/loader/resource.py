import threading
import qtawesome
from PyQt5 import QtGui
from PyQt5.QtGui import qGray, qRgba, qAlpha, QColor, QFont

from ZzClient.config.theme import Theme
from decorator.lazy_property import Lazy
from ZzClient.config.const import Config

'''
静态资源加载类避免重复实例化
'''

class ResourceLoader:
    '''
    静态资源加载器，可以使用lazy加载图像
    实现单例模式
    '''

    # 单例添加线程锁
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例
        '''
        if not hasattr(ResourceLoader, "_instance"):
            with ResourceLoader._instance_lock:
                if not hasattr(ResourceLoader, "_instance"):
                    ResourceLoader._instance = object.__new__(cls)
        return ResourceLoader._instance

    '''
    颜色资源
    '''

    @Lazy
    def qt_color_background_light(self):
        return QColor(Theme.palette.COLOR_BACKGROUND_LIGHT)

    @Lazy
    def qt_color_background(self):
        return QColor(Theme.palette.COLOR_BACKGROUND_NORMAL)

    @Lazy
    def qt_color_background_deep(self):
        return QColor(Theme.palette.COLOR_BACKGROUND_DARK)

    @Lazy
    def qt_color_text(self):
        return QColor(Theme.palette.COLOR_TEXT)

    @Lazy
    def qt_color_sub_text(self):
        return QColor(Theme.palette.COLOR_SUB_TEXT)

    '''
    字体资源
    '''

    @Lazy
    def qt_font_text(self):
        # 一级正文，二级标题
        return self.make_font(14)

    @Lazy
    def qt_font_text_xs(self):
        # 二级正文，三级标题
        return self.make_font(13)

    @Lazy
    def qt_font_text_sm(self):
        # 三级正文
        return self.make_font(12)

    @Lazy
    def qt_font_text_md(self):
        return self.make_font(15)

    @Lazy
    def qt_font_text_lg(self):
        # 大标题headline2
        return self.make_font(16)

    @Lazy
    def qt_font_text_xl(self):
        # 大标题headline1
        return self.make_font(20)

    '''
    图标资源
    '''

    @Lazy
    def qt_icon_project_ico(self):
        # 项目图标
        return self.render_icon("app.ico")

    @Lazy
    def qt_icon_project_png(self) -> QtGui.QIcon:
        # 程序图标
        return self.render_icon("icon.png")

    @Lazy
    def qt_icon_window_restore(self):
        return self.render_icon("window_restore.png")

    @Lazy
    def qt_icon_window_close(self):
        return self.render_icon("window_close.png")

    @Lazy
    def qt_icon_window_minimize(self):
        return self.render_icon("window_minimize.png")

    @Lazy
    def qt_icon_window_maximize(self):
        return self.render_icon("window_maximize.png")

    '''
    通用函数
    '''

    @staticmethod
    def make_font(size: int, weight: int = 2, family: str = "微软雅黑") -> QtGui.QFont:
        '''
        创建一个字体，如此不必重复的
        实例化-设置-调用
        :param size: 大小
        :param weight: 权重
        :param family: 字体族
        '''
        font = QtGui.QFont()
        font.setWeight(weight)
        font.setFamily(family)
        font.setPointSize(size)
        font.setStyleStrategy(QFont.PreferAntialias)
        return font

    def render_icon(self, name: str, convert=False) -> QtGui.QIcon:
        """
        渲染icon对象
        :param convert: 是否需要灰度转换
        :param name: 文件名
        """
        path = Config().icon_path + '/' + name
        return self.__render_icon_by_path(path) \
            if not convert else self.__render_icon_by_path_convert(path)

    @staticmethod
    def __render_icon_by_path(path: str) -> QtGui.QIcon:
        """
        通过路径渲染出一个icon图像
        :param path: 图像地址
        :return: QtGui.QIcon
        """
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.On)
        return icon

    @staticmethod
    def __render_icon_by_path_convert(path: str) -> QtGui.QIcon:
        """
        返回灰度icon
        """
        icon = QtGui.QIcon()
        image = QtGui.QPixmap(path).toImage()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixel(x, y)
                gray = qGray(color)
                image.setPixel(x, y, qRgba(gray, gray, gray, qAlpha(color)))
        icon.addPixmap(QtGui.QPixmap.fromImage(image), QtGui.QIcon.Normal, QtGui.QIcon.On)
        return icon