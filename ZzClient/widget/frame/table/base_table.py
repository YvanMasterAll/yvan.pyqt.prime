from PyQt5.QtCore import Qt, QVariant, pyqtSignal
from PyQt5.QtWidgets import QTableView, QFrame, QMenu, QAbstractItemView
from qtpy import QtGui

'''
QTableView基类
'''

class BaseTableView(QTableView):
    on_action_triggered = pyqtSignal(str, list)

    def __init__(self, *args, model=None, delegate=None, menus=None, **kwargs):
        super(BaseTableView, self).__init__(*args, **kwargs)

        # 表格模型
        self.setSelfMode(model)
        self.setDelegate(delegate)
        # 设置单行选中、最后一列拉伸、表头不高亮、无边框等
        self.horizontalHeader().setStretchLastSection(True)  # 自动拉伸
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setFrameShape(QFrame.NoFrame)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 菜单
        self.setMenus(menus)

    def setSelfMode(self, model):
        self.mode = model
        if model:
            self.setModel(model)

    def setDelegate(self, delegate):
        self.delegate = delegate
        if delegate:
            self.setItemDelegate(delegate)

    def setMenus(self, menus):
        # 菜单
        self.menus = menus
        if menus:
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.menu = QMenu(self)
            for action in menus:
                self.menu.addAction(action)
            self.menu.triggered.connect(self.on_menu_clicked)
            self.customContextMenuRequested.connect(self.on_menu_requested)

    def on_menu_clicked(self, action):
        indexs = self.selectionModel().selectedRows()
        data = []
        for index in indexs:
            item = index.model().data(index, Qt.UserRole)
            if not isinstance(item, QVariant):
                data.append(item)
        self.on_action_triggered.emit(action.text(), data)

    def on_menu_requested(self, pos):
        _pos = self.mapFrom(self.window(), pos)
        index = self.indexAt(_pos)
        if not index.isValid():
            self.tableView.clearSelection()
            return
        self.menu.exec_(QtGui.QCursor.pos())