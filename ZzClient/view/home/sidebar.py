import sys
from PyQt5.QtCore import QPoint, QTimer, QSize
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QSpacerItem, QGraphicsBlurEffect, QGraphicsDropShadowEffect
from qtpy import QtCore, QtWidgets
from bloc.home import Bloc_SideBar
from common.util.func import clear_layout
from common.util.route import Navigation
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.button.navbutton import NavButton, TextAlign_Center, IconPosition_Top
from widget.view import BaseView
import qtawesome

'''
侧边菜单栏
'''

class SideBar(BaseView, Bloc_SideBar):
    style_name = 'home/sidebar'
    menu = None
    menu_height = 40
    empty_menu_height = 80
    _current_menu = ''

    def __init__(self, *args, **kwargs):
        super(SideBar, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        self.setFixedWidth(self.config.sidebar_width)

        self.create_menubutton()
        self.create_empty_menubutton()

    def create_menubutton(self):
        self.menubuttons = []
        if not self.menu:
            return
        menus = self.menu['children']
        for index, menu in enumerate(menus):
            menubutton = MrxyButton.by_icon_with_text(menu['label'], qtawesome.icon(menu['icon'], color=self.resource.qt_color_text), self)
            menubutton.setObjectName('MenuButton_{name}'.format(name=menu['name']))
            # 文本颜色
            menubutton.setTextColor(self.resource.qt_color_text)
            # 锁定前景
            menubutton.setFixedForePos(True)
            menubutton.setFixedHeight(self.menu_height)
            # 设置字体和间距
            menubutton.setFont(self.resource.qt_font_text_sm)
            menubutton.fore_paddings.left = 20
            menubutton.icon_text_padding = 14
            # 设置颜色
            menubutton.setNormalColor(QColor('transparent'))
            hover_color = self.resource.qt_color_background_light
            hover_color.setAlpha(160)
            menubutton.setHoverColor(hover_color)
            press_color = self.resource.qt_color_background_light
            press_color.setAlpha(40)
            menubutton.setPressColor(press_color)
            # 设置选中颜色
            menubutton.setCheckable(True)
            def getCheckedGradient(button):
                gradient = QLinearGradient(QPoint(button.rect().left(), self.menu_height/2), QPoint(button.rect().right(), self.menu_height/2))
                gradient.setSpread(QGradient.PadSpread)
                gradient.setColorAt(0, self.resource.qt_color_primary_light)
                gradient.setColorAt(1, self.resource.qt_color_gradient_primary)
                return gradient
            menubutton.checked_gradient_func = getCheckedGradient
            # 水波完成延时
            menubutton.water_finish_duration = 100
            menubutton.clicked.connect(self.on_clicked)
            self.menubuttons.append(menubutton)

    def create_empty_menubutton(self):
        self.empty_menubutton = NavButton()
        self.empty_menubutton.setObjectName('MenuButton_Empty')
        self.empty_menubutton.setFixedHeight(120)
        self.empty_menubutton.setFixedWidth(150)
        self.empty_menubutton.setShowText('没有侧栏菜单')
        self.empty_menubutton.setShowIcon(True)
        self.empty_menubutton.setPaddingLeft(0)
        self.empty_menubutton.setPaddingRight(0)
        self.empty_menubutton.setPaddingTop(34)
        self.empty_menubutton.setPaddingBottom(20)
        self.empty_menubutton.setIconNormal(qtawesome.icon('fa5s.inbox', color=self.resource.qt_color_text).pixmap(QSize(24, 24)))
        self.empty_menubutton.setIconCheck(qtawesome.icon('fa5s.inbox', color=self.resource.qt_color_text).pixmap(QSize(24, 24)))
        self.empty_menubutton.setIconHover(qtawesome.icon('fa5s.inbox', color=self.resource.qt_color_text).pixmap(QSize(24, 24)))
        self.empty_menubutton.setTextAlign(TextAlign_Center)
        self.empty_menubutton.setFont(self.resource.qt_font_text_xs)
        self.empty_menubutton.setIconSize(QSize(24, 24))
        self.empty_menubutton.setIconPosition(IconPosition_Top)
        self.empty_menubutton.setNormalBgColor(QColor('transparent'))
        self.empty_menubutton.setHoverBgColor(QColor('transparent'))
        self.empty_menubutton.setCheckable(False)
        self.empty_menubutton.setNormalTextColor(self.resource.qt_color_sub_text)
        self.empty_menubutton.setHoverTextColor(self.resource.qt_color_text)
        self.empty_menubutton.setCheckTextColor(self.resource.qt_color_text)

    def place(self):
        layout = QVBoxLayout()
        # TODO: 为什么这里不设置间隔，按钮会重叠
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 3, 0)
        for menubutton in self.menubuttons:
            layout.addWidget(menubutton)
        if len(self.menubuttons) == 0:
            self.layout2 = QVBoxLayout()
            self.layout2.setContentsMargins(10, 10, 10, 0)
            self.layout2.addWidget(self.empty_menubutton)
            layout.addLayout(self.layout2)
        # 添加间隔
        layout.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        self.setLayout(layout)

    def re_place(self):
        layout = self.layout()
        clear_layout(layout)
        self.create_menubutton()
        self.create_empty_menubutton()
        for menubutton in self.menubuttons:
            layout.addWidget(menubutton)
        if len(self.menubuttons) == 0:
            self.layout2 = QVBoxLayout()
            self.layout2.setContentsMargins(10, 10, 10, 0)
            self.layout2.addWidget(self.empty_menubutton)
            layout.addLayout(self.layout2)
        # 添加间隔
        layout.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def on_navigation_changed(self, navigation: Navigation, menu=None, reload=False):
        # 重载菜单
        self.menu = menu
        if reload:
            self.re_place()
        if not self.menu:
            return
        button:MrxyButton = self.findChild(MrxyButton, 'MenuButton_{name}'.format(name=navigation.name))
        self.on_clicked2(button, native=False)

    def on_clicked(self):
        button = self.sender()
        self.on_clicked2(button)

    def on_clicked2(self, button, native=True):
        name = button.objectName().replace('MenuButton_', '')
        if name != self._current_menu:
            # 重置所有选项
            buttons:[MrxyButton] = self.findChildren(MrxyButton)
            for b in buttons:
                b.setChecked(False)
            # 选中所选项
            button.setChecked(True)
            if native:
                # 发起导航
                self.router.navigate_to(name)
        else:
            button.toggle()

        self._current_menu = name