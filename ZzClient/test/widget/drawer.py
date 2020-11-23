# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
#
# """
# Created on 2019年7月24日
# @author: Irony
# @site: https://pyqt5.com https://github.com/892768447
# @email: 892768447@qq.com
# @file: TestDrawer
# @description:
# """
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout,\
#     QLineEdit
# from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QPointF
# from PyQt5.QtGui import QMouseEvent
# from PyQt5.QtWidgets import QWidget, QApplication
#
# from widget.activity.drawer import Drawer
#
# __Author__ = 'Irony'
# __Copyright__ = 'Copyright (c) 2019'
#
#
# class DrawerWidget(QWidget):
#
#     def __init__(self, *args, **kwargs):
#         super(DrawerWidget, self).__init__(*args, **kwargs)
#         self.setAttribute(Qt.WA_StyledBackground, True)
#         self.setStyleSheet('DrawerWidget{background:white;}')
#         layout = QVBoxLayout(self)
#         layout.addWidget(QLineEdit(self))
#         layout.addWidget(QPushButton('button', self))
#
#
# class Window(QWidget):
#
#     def __init__(self, *args, **kwargs):
#         super(Window, self).__init__(*args, **kwargs)
#         self.resize(400, 300)
#         layout = QGridLayout(self)
#         layout.addWidget(QPushButton('上', self, clicked=self.doOpenTop), 0, 1)
#         layout.addWidget(QPushButton('左', self, clicked=self.doOpenLeft), 1, 0)
#         layout.addWidget(QPushButton(
#             '右', self, clicked=self.doOpenRight), 1, 2)
#         layout.addWidget(QPushButton(
#             '下', self, clicked=self.doOpenBottom), 2, 1)
#
#     def doOpenTop(self):
#         if not hasattr(self, 'topDrawer'):
#             self.topDrawer = Drawer(self, stretch=0.5, direction=Drawer.TOP)
#             self.topDrawer.setWidget(DrawerWidget(self.topDrawer))
#         self.topDrawer.show()
#
#     def doOpenLeft(self):
#         if not hasattr(self, 'leftDrawer'):
#             self.leftDrawer = Drawer(self, direction=Drawer.LEFT)
#             self.leftDrawer.setWidget(DrawerWidget(self.leftDrawer))
#         self.leftDrawer.show()
#
#     def doOpenRight(self):
#         if not hasattr(self, 'rightDrawer'):
#             self.rightDrawer = Drawer(self, widget=DrawerWidget())
#             self.rightDrawer.setDirection(Drawer.RIGHT)
#         self.rightDrawer.show()
#
#     def doOpenBottom(self):
#         if not hasattr(self, 'bottomDrawer'):
#             self.bottomDrawer = Drawer(
#                 self, direction=Drawer.BOTTOM, widget=DrawerWidget())
#             self.bottomDrawer.setStretch(0.5)
#         self.bottomDrawer.show()
#
#
# if __name__ == '__main__':
#     import sys
#     import cgitb
#     sys.excepthook = cgitb.enable(1, None, 5, '')
#     from PyQt5.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     w = Window()
#     w.show()
#     sys.exit(app.exec_())


# class Person(object):
#     country = '中国'
#     @classmethod
#     def countryinfo(cls):
#         print(cls.country)
#
#     @classmethod
#     def changecountry(cls,newcountry):
#         cls.country = newcountry
#         # print('此时的国籍是:',cls.country)
#
#     def init(self,name,age,gender):
#         self.name = name
#         self.age = age
#         self.gender = gender
#
# if __name__ == '__main__':
#     # 通过类对象进行调用
#     Person.countryinfo()
#     Person().changecountry('USA')
#     Person.countryinfo()
#     Person().countryinfo()
#     # # 通过实例对象进行调用
#     # zhang = Person
#     # Person.countryinfo()
#     # Person.changecountry('法国')

# import sys
# from PyQt5.QtWidgets import QLabel, QApplication
# from widget.view import BaseView
#
# class DeviceList(BaseView):
#     def __init__(self, *args, **kwargs):
#         super(DeviceList, self).__init__(*args, **kwargs)
#
#         self.procedure()
#
#     def set_ui(self):
#         label = QLabel(self)
#         label.setText("这是设备列表页面")
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = DeviceList()
#     window.show()
#
#     sys.exit(app.exec_())



import asyncio
import random
import sys

import qtawesome
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication
from qtpy import QtWidgets, QtCore, QtGui
from bloc.app import Bloc_App
from config.theme import Theme
from view.device.device_drawer import DeviceDrawer
from widget.activity.drawer import Drawer

Style = '''
Window {
    background-color: #333842;   
} 
DeviceDrawer {
    background-color: #212528;
    color: #AFAFAF;
}
DeviceDrawer #Icon_Header {
    min-width: 40px;
    min-height: 40px;
    border-image: url(:icon/device_list_current.png)
}
DeviceDrawer #Label_Title {
    font-size: 12px;
}
DeviceDrawer #Btn_Edit, DeviceDrawer #Btn_Del {
    qproperty-iconSize: 20px 12px;
    padding: 4px 0;
    font-size: 12px;
    margin-left: 6px;
}
DeviceDrawer #Btn_Menu {
    margin-left: 6px;
}
DeviceDrawer QLabel[type="100"] {
    font-size: 11px;
    color: #CDCDCD;
}
DeviceDrawer QLabel[type="101"] {
    font-size: 12px;
}
DeviceDrawer TabPage2 {
    background-color: #333842;
}
DeviceDrawer TabPage2 QLabel, DeviceDrawer TabPage2 QRadioButton {
    font-size: 12px;
}
DeviceDrawer QScrollArea {
    padding: 0;
    border: none;
}
DeviceDrawer BaseListView {
    min-height: 200px;
}
'''

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.setStyleSheet(Style)
        self.resize(1024, 768)
        self.open_drawer()

    def open_drawer(self):
        if not hasattr(self, 'drawer'):
            self.drawer = Drawer(self, stretch=0.5, direction=Drawer.RIGHT)
            self.drawer_widget = DeviceDrawer(self.drawer)
            self.drawer.setWidget(self.drawer_widget)
        QTimer.singleShot(0, lambda :self.drawer.show())

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        Bloc_App().app_closed.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    # fontDB = QFontDatabase()
    # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
    # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
    # app.setFont(QFont('Microsoft YaHei'))
    window = Window()
    window.show()

    sys.exit(app.exec_())


