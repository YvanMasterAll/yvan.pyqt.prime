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
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QListView, \
    QStyledItemDelegate, QStyleOptionViewItem, QStyleOptionButton, QCheckBox, QStyle, QAbstractItemView, QLabel
from qtpy import QtCore, QtWidgets, QtGui
import resources.qss.theme.dark.style_rc
from bloc.app import Bloc_App
from common.loader.resource import ResourceLoader
from common.util.func import calculate_middle_rect, calculate_text_rect, toDateStr
from common.util.worker import Worker
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.list.base_list_view import BaseListView
from widget.frame.list.delegate import ListDelegate
from widget.frame.list.model import ListModel
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
'''

class ListDelegate1(QStyledItemDelegate):

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        painter.drawText(QPoint(option.rect.x(), option.rect.y()), 'hello')

    def sizeHint(self, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtCore.QSize:
        return QSize(100, 60)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        self.setStyleSheet(Style)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 图标模式，多行多列
        # lv = QListView()
        # model = QStandardItemModel()
        # model.setRowCount(20)
        # proxyModel = QSortFilterProxyModel(lv)
        # proxyModel.setSourceModel(model)
        # proxyModel.setDynamicSortFilter(True)
        # lv.setModel(proxyModel)
        # lv.setItemDelegate(ListDelegate1())
        # lv.setViewMode(QListView.IconMode)
        # lv.setDragEnabled(False)
        # layout.addWidget(lv)
        # item = QStandardItem()
        # item.setData("hello")
        # model.appendRow(item)
        # item = QStandardItem()
        # item.setData("hello2")
        # model.appendRow(item)
        # item = QStandardItem()
        # item.setData("hello3")
        # model.appendRow(item)

        # 单行模式
        self.lv = BaseListView()
        model = ListModel(api=self.api)
        self.lv.setModel(model)
        self.lv.setItemDelegate(ListDelegate())
        self.lv.verticalScrollBar().valueChanged.connect(self.scrollChanged)
        layout.addWidget(self.lv)

        model.fetchData()

    def scrollChanged(self, value):
        if self.lv.verticalScrollBar().maximum() == value:
            self.lv.model().loadMore()

    async def api(self, params, callback):
        # 参数准备
        page = params['page']
        # 数据请求
        if page != 0:
            await asyncio.sleep(1)
        data = []
        if page == 2:
            return callback(data)
        for i in range(20):
            item = {
                'type': 'device_activity',
                'value': {
                    'icon': 'device_list_current.png',
                    'device': '00{id}'.format(id=random.randint(1, 10)),
                    'content': ['设备上线', '设备预热中', '工作准备ing', '工作中ing', '设备下线'][random.randint(0, 4)],
                    'date': '11-20 08:11'
                }
            }
            # item = {
            #     'type': 'string',
            #     'value': 'hello'
            # }
            data.append(item)
        callback(data)

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