from os.path import join, dirname, abspath
from qtpy.QtGui import QPalette, QColor, QFont
from base import Const

# 主题样式

_STYLESHEET = join(dirname(abspath(__file__)), '../qss/style.qss')
""" str: Main stylesheet. """

def _apply_base_theme(app):
    """ Apply base theme to the application.

        Args:
            app (QApplication): QApplication instance.
    """
    if Const.qt_version < (5,):
        app.setStyle('plastique')
    else:
        app.setStyle('Fusion')

    with open(_STYLESHEET) as stylesheet:
        app.setStyleSheet(stylesheet.read())

def dark(app):
    """ Apply Dark Theme to the Qt application instance.

        Args:
            app (QApplication): QApplication instance.
    """
    _apply_base_theme(app)

    darkPalette = QPalette()

    # base
    darkPalette.setColor(QPalette.WindowText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.Light, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Midlight, QColor(90, 90, 90))
    darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
    darkPalette.setColor(QPalette.Text, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.BrightText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.ButtonText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    darkPalette.setColor(QPalette.HighlightedText, QColor(180, 180, 180))
    darkPalette.setColor(QPalette.Link, QColor(56, 252, 196))
    darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    darkPalette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
    darkPalette.setColor(QPalette.ToolTipText, QColor(180, 180, 180))

    # disabled
    darkPalette.setColor(QPalette.Disabled, QPalette.WindowText,
                         QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Disabled, QPalette.Text,
                         QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText,
                         QColor(127, 127, 127))
    darkPalette.setColor(QPalette.Disabled, QPalette.Highlight,
                         QColor(80, 80, 80))
    darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText,
                         QColor(127, 127, 127))

    app.setPalette(darkPalette)

# 主题颜色

class Color:
    # 主色, 淡绿色
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

    # 辅色, 蓝色
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

    # 辅色, 黄色
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

    # 补色, 红色
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

    # 对比色, 青色
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

    # 中性色, 黑色
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

# 字体大小

class Font:
    """在苹果和微软系统上字体大小是否有差异呢"""
    # font_36_m = QFont("Microsoft YaHei", 36, 60)  # 导航/大标题/结果和空状态等单一页面
    # font_32_m = QFont("Microsoft YaHei", 32, 60)  # 大按钮
    # font_30_m = QFont("Microsoft YaHei", 30, 60)  # 一级标题
    # font_28_r = QFont("Microsoft YaHei", 28, 50)  # 一级正文/列表正文
    # font_26_m = QFont("Microsoft YaHei", 26, 60)  # 二级标题
    # font_26_r = QFont("Microsoft YaHei", 26, 50)  # 二级正文
    # font_24_r = QFont("Microsoft YaHei", 24, 50)  # 三级正文
    # font_22_r = QFont("Microsoft YaHei", 22, 50)  # 四级正文
    # font_20_r = QFont("Microsoft YaHei", 20, 50)  # 说明文本/版权信息/不需要用户关注的信息
    # font_12_r = QFont("Microsoft YaHei", 12, 50)  # 网页文本

    font_18_m = QFont("Microsoft YaHei", 18, 60)  # 导航/大标题/结果和空状态等单一页面
    font_16_m = QFont("Microsoft YaHei", 16, 60)  # 大按钮
    font_15_m = QFont("Microsoft YaHei", 15, 60)  # 一级标题
    font_14_r = QFont("Microsoft YaHei", 14, 60)  # 一级正文/列表正文
    font_13_m = QFont("Microsoft YaHei", 13, 60)  # 二级标题
    font_13_r = QFont("Microsoft YaHei", 13, 50)  # 二级正文
    font_12_r = QFont("Microsoft YaHei", 12, 50)  # 三级正文
    font_11_r = QFont("Microsoft YaHei", 11, 50)  # 四级正文
    font_10_r = QFont("Microsoft YaHei", 10, 50)  # 说明文本/版权信息/不需要用户关注的信息
    font_6_r = QFont("Microsoft YaHei", 6, 50)  # 网页文本