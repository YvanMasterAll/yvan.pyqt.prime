import os
import threading
from os.path import join, dirname, abspath
from qtpy.QtGui import QPalette, QColor, QFont
from quamash import QApplication
from config.const import Config
from common.util.storage import LocalStorage
import importlib

'''
主题样式
'''

COMMON_STYLE = Config().qss_path + '/common.qss'

class Theme:

    # 单例添加线程锁
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        '''
        实现单例
        '''
        if not hasattr(Theme, "_instance"):
            with Theme._instance_lock:
                if not hasattr(Theme, "_instance"):
                    Theme._instance = object.__new__(cls)
        return Theme._instance

    # 调色板
    palette = None

    @classmethod
    def load(cls):
        app = QApplication.instance()
        theme = LocalStorage.themeGet()
        skin_qss = '{qss_path}/theme/{theme}/skin.qss'.format(qss_path=Config().qss_path, theme=theme)
        style_qss = '{qss_path}/theme/{theme}/style.qss'.format(qss_path=Config().qss_path, theme=theme)
        qss_string = ''
        # 0).资源文件
        skin_rc = importlib.import_module('resources.qss.theme.{theme}.skin_rc'.format(theme=theme))
        style_rc = importlib.import_module('resources.qss.theme.{theme}.style_rc'.format(theme=theme))
        skin_rc.qInitResources()
        style_rc.qInitResources()
        # 1).自带皮肤
        app.setStyle('Fusion')
        # 2).调色板
        palette_module = importlib.import_module('resources.qss.theme.{theme}.palette'.format(theme=theme))
        cls.palette = getattr(palette_module, 'Palette')
        cls.palette.render(app)
        # 3).通用样式表
        with open(COMMON_STYLE) as stylesheet:
            qss_string += stylesheet.read()
        # 4).皮肤样式表
        with open(skin_qss) as stylesheet:
            qss_string += stylesheet.read()
        # 5).界面样式表
        with open(style_qss) as stylesheet:
            qss_string += stylesheet.read()
        # 6).设置样式
        app.setStyleSheet(qss_string)
        # 7).抗锯齿
        font = app.font();
        font.setStyleStrategy(QFont.PreferAntialias);
        app.setFont(font);

    @classmethod
    def toggle(cls, theme):
        themes = LocalStorage.themeAllGet()
        if theme not in themes:
            return
        # 0).卸载资源
        current_theme = LocalStorage.themeGet()
        skin_rc = importlib.import_module('resources.qss.theme.{theme}.skin_rc'.format(theme=current_theme))
        style_rc = importlib.import_module('resources.qss.theme.{theme}.style_rc'.format(theme=current_theme))
        skin_rc.qCleanupResources()
        style_rc.qCleanupResources()
        # 1).改变主题
        LocalStorage.themeSet(theme)
        # 2).重载主题
        Theme.load()

        print('主题更换：{theme}'.format(theme=theme))

'''
颜色面板
'''

class ColorPalette:
    '''主色, 淡绿色'''
    green50 = QColor("#CCFFEF")
    green100 = QColor("#A3FFE1")
    green200 = QColor("#7AFFD2")
    green300 = QColor("#52FFC3")
    green400 = QColor("#29FFB3")
    green500 = QColor("#00FFA2")
    green600 = QColor("#00EC98")
    green700 = QColor("#00D98E")
    green800 = QColor("#00C684")
    green900 = QColor("#00B379")

    '''辅色, 蓝色'''
    blue50 = QColor("#CCE1FF")
    blue100 = QColor("#A5C9FC")
    blue200 = QColor("#80B1F8")
    blue300 = QColor("#5D9AF2")
    blue400 = QColor("#3C84EA")
    blue500 = QColor("#1D6DE0")
    blue600 = QColor("#1464D6")
    blue700 = QColor("#0C5ACB")
    blue800 = QColor("#0651BF")
    blue900 = QColor("#0049B1")

    '''辅色, 黄色'''
    yellow50 = QColor("#FFFAD2")
    yellow100 = QColor("#FFF5AF")
    yellow200 = QColor("#FFEF8F")
    yellow300 = QColor("#FFE870")
    yellow400 = QColor("#FFE054")
    yellow500 = QColor("#FCD639")
    yellow600 = QColor("#ECCA2E")
    yellow700 = QColor("#D9BE24")
    yellow800 = QColor("#C6B01B")
    yellow900 = QColor("#B3A213")

    '''补色, 红色'''
    red50 = QColor("#FFCCE8")
    red100 = QColor("#FFA4D6")
    red200 = QColor("#FF7FC4")
    red300 = QColor("#FF5DB1")
    red400 = QColor("#FC3C9F")
    red500 = QColor("#F51D8C")
    red600 = QColor("#EA1382")
    red700 = QColor("#D90B77")
    red800 = QColor("#C6046D")
    red900 = QColor("#B30063")

    '''对比色, 青色'''
    cyan50 = QColor("#CCFBFF")
    cyan100 = QColor("#A3F6FF")
    cyan200 = QColor("#7AEFFF")
    cyan300 = QColor("#52E6FF")
    cyan400 = QColor("#29DDFF")
    cyan500 = QColor("#00D1FF")
    cyan600 = QColor("#00C7EC")
    cyan700 = QColor("#00BCD9")
    cyan800 = QColor("#00B0C6")
    cyan900 = QColor("#00A3B3")

    '''中性色, 黑色'''
    black50 = QColor("#F0F0F0")
    black100 = QColor("#D4D4D4")
    black200 = QColor("#B9B9B9")
    black300 = QColor("#9D9D9D")
    black400 = QColor("#828282")
    black500 = QColor("#666666")
    black600 = QColor("#595959")
    black700 = QColor("#4D4D4D")
    black800 = QColor("#333333")
    black900 = QColor("#2A2A2A")
