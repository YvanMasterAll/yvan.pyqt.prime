import sys

import qtawesome
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer, QAbstractTableModel, QVariant, qDebug, QModelIndex
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QTableWidget, \
    QLabel
from qtpy import QtCore, QtWidgets
import resources.qss.theme.dark.style_rc
from common.loader.resource import ResourceLoader
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.form.baselineedit import BaseLineEdit
from widget.frame.separator.separator import Separator
from widget.frame.table.model import TableModel
from widget.frame.table.pagination import CPaginationBar
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
'''

class TableModel3(QAbstractTableModel):
    m_pageHash = {} # key是页码值, value是此页的第一项数据在dataList中的下标值
    m_dataList = [] # 存储数据的容器

    m_pageSize = 0 # 每页显示的数据量
    m_rowCount = 0 # 要显示的行数

    def __init__(self, rowCount, pageSize, *args, **kwargs):
        super(TableModel3, self).__init__(*args, **kwargs)

        self.m_pageSize = pageSize
        self.m_rowCount = rowCount

    def columnCount(self, parent: QModelIndex = ...):
        return 1  # 以一列为示例, 如果是多列, 则data list保存的应该是对象

    def rowCount(self, parent: QModelIndex = ...):
        return self.m_rowCount

    def data(self, index: QModelIndex, role: int = ...):
        if not index:
            return QVariant()

        if Qt.DisplayRole == role:
            i = self.indexOfRow(index.row())
            if i >= len(self.m_dataList):
                return QVariant()
            return self.m_dataList[i]

        return QVariant()

    def indexOfRow(self, row):
        page = row / self.m_pageSize  # 每页显示pageSize条记录

        if not self.m_pageHash.__contains__(page):
            # 如果此面的数据不存在, 则读取数据到 data list里
            self.fetchData(page)

        return self.m_pageHash[page] + row % self.m_pageSize

    def fetchData(self, page):
        '''
        每次加载数据时,如果是耗时任务, 可以使用进度条显示加载进度
        也可以取消加载, 但是这个时候data()函数中返回一个非有效的index
        '''
        pageStartIndex = len(self.m_dataList) # 存储此页码与其所对应的开始下标值
        self.m_pageHash[page] = pageStartIndex

        # 例如在这里使用分页查询, 从数据库里读取数据
        for i in range(self.m_pageSize):
            data = page * self.m_pageSize + i
            self.m_dataList.append(data)


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        self.setStyleSheet(Style)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(layout)

        '''
        QTableWidget
        '''
        # table = QTableWidget(self)
        # table.setMinimumSize(QtCore.QSize(500, 500))
        # table.setMaximumSize(QtCore.QSize(16777215, 16777215))
        # table.setObjectName("tableWidget")
        # table.setColumnCount(2)
        # table.setRowCount(3)
        # item = QtWidgets.QTableWidgetItem()
        # table.setVerticalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setVerticalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setVerticalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setHorizontalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setHorizontalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setItem(0, 0, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setItem(0, 1, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setItem(1, 0, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setItem(1, 1, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setItem(2, 0, item)
        # item = QtWidgets.QTableWidgetItem()
        # table.setItem(2, 1, item)
        #
        # table.setToolTip("This is a tool tip")
        # table.setStatusTip("This is a status tip")
        # table.setWhatsThis("This is \"what is this\"")
        # item = table.verticalHeaderItem(0)
        # item.setText("New Row")
        # item = table.verticalHeaderItem(1)
        # item.setText("New Row")
        # item = table.verticalHeaderItem(2)
        # item.setText("New Row")
        # item = table.horizontalHeaderItem(0)
        # item.setText("New Column")
        # item = table.horizontalHeaderItem(1)
        # item.setText("New Column")
        # __sortingEnabled = table.isSortingEnabled()
        # table.setSortingEnabled(False)
        # item = table.item(0, 0)
        # item.setText("1.23")
        # item = table.item(0, 1)
        # item.setText("Hello")
        # item = table.item(1, 0)
        # item.setText("1,45")
        # item = table.item(1, 1)
        # item.setText("Olá")
        # item = table.item(2, 0)
        # item.setText("12/12/2012")
        # item = table.item(2, 1)
        # item.setText("Oui")
        # table.setSortingEnabled(__sortingEnabled)

        '''
        QTableView
        '''
        # self.resize(400, 390)
        # self.gridLayout = QtWidgets.QGridLayout(self)
        # self.gridLayout.setContentsMargins(11, 11, 11, 11)
        # self.gridLayout.setSpacing(6)
        # self.gridLayout.setObjectName("gridLayout")
        # self.tableView = QtWidgets.QTableView(self)
        # self.tableView.setObjectName("tableView")
        # self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)
        #
        # model = TableModel(rowCount=1000, pageSize=20)
        # self.tableView.setModel(model)
        # self.tableView.horizontalHeader().setStretchLastSection(True)

        '''
        QTableView With Pagination
        '''
        self.setFixedSize(600, 450)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        # 头部
        label_icon_search = QLabel()
        label_icon_search.setPixmap(qtawesome.icon('fa5s.search', color=ResourceLoader().qt_color_sub_text).pixmap(QSize(18, 18)))
        label_icon_search.setFixedSize(20, 20)
        self.input_search = BaseLineEdit(leftWidget=label_icon_search)
        self.input_search.setFixedHeight(32)
        self.input_search.setLeftRightLayoutMargin(10, 10)
        self.input_search.setPlaceholderText("输入查询条件")
        self.gridLayout.addWidget(self.input_search, 0, 0, 1, 1)
        btn_search = QPushButton()
        btn_search.setProperty("type", 1)
        btn_search.setText("查询")
        btn_search.clicked.connect(self.search)
        self.gridLayout.addWidget(btn_search, 0, 1, 1, 1)
        btn_reset = QPushButton()
        btn_reset.setProperty("type", 1)
        btn_reset.setText("重置")
        btn_reset.clicked.connect(self.reset)
        self.gridLayout.addWidget(btn_reset, 0, 2, 1, 1)
        separator = Separator(self)
        separator.setFixedHeight(2)
        self.gridLayout.addWidget(separator, 1, 0, 1, 10)
        # 表格
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 0, 1, 10)
        separator = Separator(self)
        separator.setFixedHeight(2)
        self.gridLayout.addWidget(separator, 3, 0, 1, 10)
        # 分页栏
        self.paginationBar1 = CPaginationBar(self, totalPages=20)
        self.paginationBar1.setInfos('共 400 条')
        self.paginationBar1.setJumpWidget(True)
        self.paginationBar1.pageChanged.connect(lambda page: self.model.fetchData(page=page-1))
        self.gridLayout.addWidget(self.paginationBar1, 4, 0, 1, 10)

        self.model = TableModel(self, api=self.api, pagination=self.paginationBar1)
        # self.model.setHeaderData(0, Qt.Horizontal, "姓名")
        # self.model.setHeaderData(1, Qt.Horizontal, "姓名")
        # self.model.setHeaderData(2, Qt.Horizontal, "姓名")
        # self.model.setHeaderData(0, Qt.Vertical, "姓名")
        # self.model.setHeaderData(1, Qt.Vertical, "姓名")
        # self.model.setHeaderData(2, Qt.Vertical, "姓名")
        def mock():
            # self.model.fetchData(0)
            self.model.fetchData()
        QTimer.singleShot(2000, mock)
        self.model.m_headData = ['hello', 'Then']
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

    def api(self, params):
        # 1).获取查询参数
        param = self.input_search.text()
        # 2).查询数据
        page = params['page']
        data = {
            'head': [
                {'key': 'sn', 'label': '编号'},
                {'key': 'type', 'label': '类型'},
                {'key': 'check', 'label': '审核'},
                {'key': 'content', 'label': '类容'},
            ],
            'data': [
                {
                    'sn': {'value': '001', 'type': 'string'},
                    'type': {'value': '警告', 'text_color': ResourceLoader().qt_color_tag_warning,
                             'border_color': ResourceLoader().qt_color_tag_warning,
                             'font': ResourceLoader().qt_font_text_tag, 'type': 'tag'},
                    'check': {'value': 1, 'type': 'checkbox', 'size': 20},
                    'content': {'value': '设备离线', 'type': 'string'},
                },
                {
                    'sn': {'value': '002', 'type': 'string'},
                    'type': {'value': '正常', 'text_color': ResourceLoader().qt_color_tag_success,
                             'border_color': ResourceLoader().qt_color_tag_success,
                             'font': ResourceLoader().qt_font_text_tag, 'type': 'tag'},
                    'check': {'value': 0, 'type': 'checkbox', 'size': 20},
                    'content': {'value': '设备正常', 'type': 'string'},
                }
            ]
        }
        return {'total': 100, 'data': data}

    def search(self):
        self.model.fetchData()

    def reset(self):
        self.input_search.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    # fontDB = QFontDatabase()
    # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
    # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
    # app.setFont(QFont('Microsoft YaHei'))
    window = Window()
    window.show()
    window.resize(500, 500)

    sys.exit(app.exec_())