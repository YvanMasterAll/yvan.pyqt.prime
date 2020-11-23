import threading
import qtawesome
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import qGray, qRgba, qAlpha, QColor, QFont, QFontDatabase, QPixmap, QPainter
from six import unichr
from common.util.route import RouteManager
from config.route import routes, menus
from config.theme import Theme
from common.decorator.lazy_property import Lazy
from config.const import Config

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
    图标字体
    '''
    iconFontNames = {}

    '''
    字体资源
    '''
    @property
    def qt_font_yahei(self):
        return Config().font_path + '/Microsoft-YaHei.ttf'

    '''
    颜色资源
    '''
    @property
    def qt_color_background_light(self):
        return QColor(Theme.palette.COLOR_BACKGROUND_LIGHT)

    @property
    def qt_color_background(self):
        return QColor(Theme.palette.COLOR_BACKGROUND_NORMAL)

    @property
    def qt_color_background_dark(self):
        return QColor(Theme.palette.COLOR_BACKGROUND_DARK)

    @property
    def qt_color_primary_light(self):
        return QColor(Theme.palette.COLOR_PRIMARY_LIGHT)

    @property
    def qt_color_primary_normal(self):
        return QColor(Theme.palette.COLOR_PRIMARY_NORMAL)

    @property
    def qt_color_background_dark(self):
        return QColor(Theme.palette.COLOR_PRIMARY_DARK)

    @property
    def qt_color_gradient_primary(self):
        return QColor(Theme.palette.COLOR_GRADIENT_PRIMARY)

    @property
    def qt_color_text(self):
        return QColor(Theme.palette.COLOR_TEXT)

    @property
    def qt_color_sub_text(self):
        return QColor(Theme.palette.COLOR_SUB_TEXT)

    @property
    def qt_color_tag_online(self):
        return QColor(Theme.palette.COLOR_TAG_ONLINE)

    @property
    def qt_color_tag_offline(self):
        return QColor(Theme.palette.COLOR_TAG_OFFLINE)

    @property
    def qt_color_tag_warning(self):
        return QColor(Theme.palette.COLOR_TAG_WARNING)

    @property
    def qt_color_tag_success(self):
        return QColor(Theme.palette.COLOR_TAG_SUCCESS)

    @property
    def qt_color_label_link(self):
        return QColor(Theme.palette.COLOR_LABEL_LINK)

    ''' 
    字体资源
    '''

    @property
    def qt_font_text(self):
        # 一级正文，二级标题
        return self.make_font(14)

    @property
    def qt_font_text_sm(self):
        # 二级正文，三级标题
        return self.make_font(13)

    @property
    def qt_font_text_xs(self):
        # 三级正文
        return self.make_font(12)

    @property
    def qt_font_text_xss(self):
        return self.make_font(11)

    @property
    def qt_font_text_tag(self):
        return self.make_font(10)

    @property
    def qt_font_text_md(self):
        return self.make_font(15)

    @property
    def qt_font_text_lg(self):
        # 大标题headline2
        return self.make_font(16)

    @property
    def qt_font_text_xl(self):
        # 大标题headline1
        return self.make_font(20)

    '''
    图标资源
    '''

    @property
    def qt_icon_project_ico(self):
        # 项目图标
        return self.render_icon("logo_neat.png")

    @property
    def qt_icon_project_png(self) -> QtGui.QIcon:
        # 程序图标
        return self.render_icon("icon.png")

    @property
    def qt_icon_window_restore(self):
        return self.render_icon("window_restore.png")

    @property
    def qt_icon_window_close(self):
        return self.render_icon("window_close.png")

    @property
    def qt_icon_window_minimize(self):
        return self.render_icon("window_minimize.png")

    @property
    def qt_icon_window_maximize(self):
        return self.render_icon("window_maximize.png")

    '''
    通用函数
    '''

    # TODO: Microsoft YaHei
    @staticmethod
    def make_font(size: int, weight: int = 50, family: str = "Microsoft Yahei") -> QtGui.QFont:
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
        font.setPixelSize(size)
        font.setStyleStrategy(QFont.PreferAntialias)
        return font

    def icon_path(self, name):
        '''
        返回图标路径
        '''
        return Config().icon_path + '/' + name

    def render_pixmap(self, name: str) -> QtGui.QPixmap:
        '''
        渲染icon对象
        :param name: 文件名
        '''
        path = Config().icon_path + '/' + name
        return QtGui.QPixmap(path)

    def render_icon(self, name: str, convert=False) -> QtGui.QIcon:
        '''
        渲染icon对象
        :param convert: 是否需要灰度转换
        :param name: 文件名
        '''
        path = Config().icon_path + '/' + name
        return self.__render_icon_by_path(path) \
            if not convert else self.__render_icon_by_path_convert(path)

    @staticmethod
    def __render_icon_by_path(path: str) -> QtGui.QIcon:
        '''
        通过路径渲染出一个icon图像
        :param path: 图像地址
        :return: QtGui.QIcon
        '''
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.On)
        return icon

    @staticmethod
    def __render_icon_by_path_convert(path: str) -> QtGui.QIcon:
        '''
        返回灰度icon
        '''
        icon = QtGui.QIcon()
        image = QtGui.QPixmap(path).toImage()
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixel(x, y)
                gray = qGray(color)
                image.setPixel(x, y, qRgba(gray, gray, gray, qAlpha(color)))
        icon.addPixmap(QtGui.QPixmap.fromImage(image), QtGui.QIcon.Normal, QtGui.QIcon.On)
        return icon

    @classmethod
    def load_icon_font(cls):
        '''
        加载图标字体
        '''
        fontawesome_id = QFontDatabase().addApplicationFont(':font/fontawesome-webfont.ttf')
        fontawesome_name = QFontDatabase.applicationFontFamilies(fontawesome_id)[0]
        cls.iconFontNames['fontawesome'] = fontawesome_name

    @classmethod
    def make_iconfont(cls, widget, type, size=24):
        '''
        图标字体
        '''
        if len(cls.iconFontNames) == 0:
            cls.load_icon_font()

        font = QFont(cls.iconFontNames[type[0]], size)
        widget.setFont(font)
        widget.setText(unichr(type[1]))

    @classmethod
    def make_iconfont_pix(cls, type, color='#FFFEFE', size=24) -> QPixmap:
        '''
        图标字体转Pixmap
        '''
        if len(cls.iconFontNames) == 0:
            cls.load_icon_font()

        pix = QPixmap(size, size)
        pix.fill(Qt.transparent)

        painter = QPainter()
        painter.begin(pix)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setPen(QColor(color))
        painter.setBrush(QColor(color))
        font = QFont(cls.iconFontNames[type[0]], size)
        painter.setFont(font)

        painter.drawText(pix.rect(), Qt.AlignCenter, unichr(type[1]))

        return pix

    @classmethod
    def load_modules(cls):
        '''
        加载模块
        '''
        # 1).读取模块配置
        # 2).加载模块
        _routes = routes
        _menus = menus
        RouteManager().load_modules(_routes, _menus)