import asyncio
import random
import sys

import qtawesome
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint, QPropertyAnimation, QEasingCurve, QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QSpacerItem, \
    QGridLayout, QListWidget, QListWidgetItem
from qtpy import QtWidgets, QtCore, QtGui
from bloc.app import Bloc_App
from config.theme import Theme
from view.device.device_drawer import DeviceDrawer
from widget.activity.drawer import Drawer
from widget.activity.modal.action_sheet import ActionSheet
from widget.frame.list.base_list_widget import BaseListWidget
from widget.view import BaseView

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
        self.sheet = ActionSheet(data=['电流', '电压', '电阻'], parent=self)
        self.sheet.on_item_clicked.connect(lambda item:print('选中了{item}'.format(item=item)))
        self.sheet.dialog.add_action('重置', lambda :print("点击了重置按钮"))
        # self.popup = PopupContainer(self, widget=sheet)
        self.open_drawer()

    def open_drawer(self):
        QTimer.singleShot(100, lambda :self.sheet.showSelf())

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