from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QHBoxLayout, QSpacerItem
from qtpy import QtWidgets
from bloc.home import Bloc_Navbar
from common.loader.resource import ResourceLoader
from common.util.func import clear_layout
from common.util.route import RouteManager
from widget.frame.button.navbutton import NavButton, TextAlign_Center, IconPosition_Top
from widget.frame.separator.separator import Separator
from widget.view import BaseView

'''
导航栏
'''

class NavBar(BaseView, Bloc_Navbar):
    style_name = 'home/navbar'
    navs = []
    _initial_nav = None
    _current_nav = None

    def __init__(self, *args, **kwargs):
        super(NavBar, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        self.create_navbutton()

    def create_navbutton(self):
        self.navbuttons = []
        separator = Separator(self, orientation='vertical')
        separator.setFixedHeight(48)
        separator.setFixedWidth(4)
        self.navbuttons.append(separator)
        for index, nav in enumerate(self.navs):
            navbutton = self.navbutton_factory(nav)
            self.navbuttons.append(navbutton)
            if index < len(self.navs)-1:
                separator = Separator(self, orientation='vertical')
                separator.setFixedHeight(48)
                separator.setFixedWidth(4)
                self.navbuttons.append(separator)

    def navbutton_factory(self, nav):
        navbutton = NavButton()
        navbutton.setObjectName('NavButton_{name}'.format(name=nav['name']))
        navbutton.setFixedHeight(70)
        navbutton.setFixedWidth(74)
        navbutton.setShowText(nav['label'])
        navbutton.setShowIcon(True)
        navbutton.setPaddingLeft(0)
        navbutton.setPaddingRight(0)
        navbutton.setPaddingTop(6)
        navbutton.setPaddingBottom(4)
        navbutton.setIconNormal(QPixmap(':icon/{icon}'.format(icon=nav['icon'])))
        navbutton.setIconCheck(QPixmap(':icon/{icon}'.format(icon=nav['icon'])))
        navbutton.setIconHover(QPixmap(':icon/{icon}'.format(icon=nav['icon'])))
        navbutton.setTextAlign(TextAlign_Center)
        navbutton.setFont(self.resource.qt_font_text_xs)
        navbutton.setIconSize(QSize(34, 34))
        navbutton.setIconPosition(IconPosition_Top)
        navbutton.setNormalBgColor(QColor('transparent'))
        navbutton.setHoverBgColor(QColor('transparent'))
        navbutton.setCheckBgColor(QColor('transparent'))
        navbutton.setNormalTextColor(self.resource.qt_color_sub_text)
        navbutton.setHoverTextColor(self.resource.qt_color_text)
        navbutton.setCheckTextColor(self.resource.qt_color_text)
        navbutton.clicked.connect(self.on_clicked)

        return navbutton

    def on_clicked(self, checked):
        button = self.sender()
        name = button.objectName().replace('NavButton_', '')
        if name != self._current_nav:
            # 重置所有选项
            buttons:[NavButton] = self.findChildren(NavButton)
            for b in buttons:
                b.setChecked(False)
            # 选中所选项
            button.setChecked(True)
            # 触发导航
            self.router.navigate_to(name)
        else:
            button.toggle()

        self._current_nav = name

    def place(self):
        layout = QHBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 4)
        for navbutton in self.navbuttons:
            layout.addWidget(navbutton)

        layout.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.setLayout(layout)

    def re_place(self):
        layout = self.layout()
        clear_layout(layout)
        self.create_navbutton()
        for navbutton in self.navbuttons:
            layout.addWidget(navbutton)

        layout.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

    def on_module_loaded(self, navs):
        self.navs = navs
        self.re_place()
        self.configure()

    def configure(self):
        if len(self.navs) == 0:
            return
        # 初始默认项
        if not self._initial_nav:
            self._initial_nav = self.navs[0]['name']
        button:NavButton = self.findChild(NavButton, 'NavButton_{name}'.format(name=self._initial_nav))
        button.click()