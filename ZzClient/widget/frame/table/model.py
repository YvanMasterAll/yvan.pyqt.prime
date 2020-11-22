import typing
from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex, Qt, QAbstractItemModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem

'''
数据格式
data = {
    'head': [
        {'key': 'sn', 'label': '编号'},
        {'key': 'type', 'label': '类型'},
        {'key': 'time', 'label': '时间'},
        {'key': 'content', 'label': '类容'},
    ],
    'data': [
        {
            'sn': {'value': '001', 'type': 'string'},
            'type': {'value': '警告', 'type': 'widget'},
            'time': {'value': '2020-11-19 11:03', 'type': 'string'},
            'content': {'value': '设备离线', 'type': 'string'},
        }
    ]
}
'''

'''
QTableView模型，配置TableDelegate使用
'''

class TableModel(QAbstractTableModel):
    m_dataList = {}     # 存储数据的容器
    m_pageSize = 20     # 每页显示的数据量
    m_pageNum = 0       # 当前页数
    m_totalCount = 0    # 数据总量

    def __init__(self, *args, api, pagination=None, **kwargs):
        super(TableModel, self).__init__(*args, **kwargs)

        self.api = api
        self.pagination = pagination

    def columnCount(self, parent: QModelIndex = ...):
        if len(self.m_dataList) == 0:
            return 0
        return len(self.m_dataList['head']) # 以一列为示例, 如果是多列, 则data list保存的应该是对象

    def rowCount(self, parent: QModelIndex = ...):
        return self.m_pageSize

    def updateData(self, data):
        self.m_dataList = data
        self.beginResetModel()
        self.endResetModel()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        '''
        表格可选中、可复选
        '''
        if not index.isValid():
            return QAbstractItemModel.flags(index)

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        return flags

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        '''
        用来设置数据，根据角色（颜色、文本、对齐方式、选中状态等）判断需要设置的内容
        '''
        if not index.isValid():
            return False

        i = index.row()
        j = index.column()
        head = self.m_dataList['head']
        data = self.m_dataList['data']

        if Qt.DisplayRole == role:
            key = head[j]['key']
            item = data[i][key]
            item['value'] = value
            self.dataChanged.emit(index, index)
            return True
        if Qt.UserRole == role:
            pass

        return False

    def data(self, index: QModelIndex, role: int = ...):
        '''
        用来显示数据，根据角色（颜色、文本、对齐方式、选中状态等）判断需要显示的内容
        '''
        if not index or len(self.m_dataList) == 0:
            return QVariant()

        head = self.m_dataList['head']
        data = self.m_dataList['data']

        if Qt.DisplayRole == role:
            i = index.row()
            j = index.column()
            key = head[j]['key']
            if i >= len(data):
                return QVariant()
            item = data[i][key]
            value = item['value']
            type = item['type']
            if type == 'string':
                return value
        if Qt.UserRole == role:
            i = index.row()
            j = index.column()
            key = head[j]['key']
            if i >= len(data):
                return QVariant()
            item = data[i][key]
            return item
        if Qt.TextAlignmentRole == role:
            return Qt.AlignCenter

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if orientation == Qt.Horizontal: # 水平表头
            if role == Qt.DisplayRole: # 角色为显示
                return self.m_dataList['head'][section]['label'] # 返回指定位置表头
        return QAbstractTableModel.headerData(self, section, orientation, role);

    def fetchData(self, page=0):
        if not self.api:
            return
        # 1).更新页数
        self.m_pageNum = page
        # 2).查询数据
        result = self.api({'page': page, 'pagesize': self.m_pageSize})
        # 3).更新总数量
        totalCount = result['total']
        pages = int(totalCount/self.m_pageSize)
        data = result['data']
        self.m_totalCount = totalCount
        self.updateData(data)
        # 4).更新分页栏
        if self.pagination:
            self.pagination.setCurrentPage(page+1)
            self.pagination.setTotalPages(pages)
            self.pagination.setInfos('共 {count} 条'.format(count=totalCount))


