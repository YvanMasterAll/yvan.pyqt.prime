import asyncio
import datetime
import random
import sys
import threading
import time

import typing

import qtawesome
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer, QModelIndex, QAbstractItemModel, QAbstractTableModel, \
    QVariant, QRectF, QRect, QEvent, QSortFilterProxyModel, QStringListModel, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient, \
    QStandardItemModel, QPainter, QPainterPath, QFontMetrics, QPen, QStandardItem, QImage
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QListWidget, \
    QStyledItemDelegate, QStyleOptionViewItem, QStyleOptionButton, QCheckBox, QStyle, QAbstractItemView, QLabel, \
    QListWidgetItem
from qtpy import QtCore, QtWidgets, QtGui
import resources.qss.theme.dark.style_rc
from bloc.app import Bloc_App
from common.loader.resource import ResourceLoader
from common.util.func import calculate_middle_rect, calculate_text_rect, toDateStr
from common.util.worker import Worker
from config.theme import Theme
from test.widget.list.list_cell import ListCell
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.list.base_list_view import BaseListView
from widget.frame.list.base_list_widget import BaseListWidget
from widget.frame.list.model import ListWidgetModel
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
LoadMore {
    font-size: 12px;
}
DeviceActivityCell QLabel {
    font-size: 12px;
}
DeviceActivityCell #label_name {
    color: #29FFB3;
}
DeviceActivityCell #label_content {
    color: #CDCDCD;
}
'''

class DeviceActivityCell(QWidget, ListCell):

    def __init__(self, *args, data, **kwargs):
        super(DeviceActivityCell, self).__init__(*args, **kwargs)

        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.data = data

        self.icon_device.setText("")
        self.icon_device.setPixmap(QPixmap(data['icon']).scaled(QSize(44, 44), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_name.setText('设备    {name}'.format(name=data['device']))
        self.label_content.setText(data['content'] + '，' + toDateStr())
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 4, 0, 4)
        self.verticalLayout.setSpacing(0)


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        self.setStyleSheet(Style)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.lv = BaseListWidget()
        self.model = ListWidgetModel(view=self.lv, api=self.api)
        self.lv.verticalScrollBar().valueChanged.connect(self.scrollChanged)

        # item = QListWidgetItem()
        # item.setSizeHint(QSize(0, 80))
        # test_widget = QWidget()
        # test_widget.setLayout(QVBoxLayout())
        # test_widget.layout().addWidget(QLabel("hello44"))
        # self.lv.addItem(item)
        # self.lv.setItemWidget(item, test_widget)

        layout.addWidget(self.lv)

        self.model.fetchData()

    def scrollChanged(self, value):
        if self.lv.verticalScrollBar().maximum() == value:
            self.model.loadMore()

    async def api(self, params):
        # 参数准备
        page = params['page']
        # 数据请求
        if page != 0:
            await asyncio.sleep(1)
        data = []
        if page == 2:
            self.model.on_data_update.emit(data)
            return
        # 列表项函数
        def get_item_cell(data):
            return DeviceActivityCell(data=data)
        for i in range(20):
            item = {
                'type': 'device_activity',
                'value': {
                    'icon': ':icon/device_list_current.png',
                    'device': '00{id}'.format(id=random.randint(1, 10)),
                    'content': ['设备上线', '设备预热中', '工作准备ing', '工作中ing', '设备下线'][random.randint(0, 4)],
                    'date': '11-20 08:11'
                },
                'size': QSize(0, 70),
                'item_cell': get_item_cell
            }
            data.append(item)

        self.model.on_data_update.emit(data)

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