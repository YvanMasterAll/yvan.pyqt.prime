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
# from ZzClient.widget.view import BaseView
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

