import qtawesome
from PyQt5.QtCore import QStringListModel, QModelIndex, Qt, QAbstractItemModel, QVariant, QSize, pyqtSignal, QTimer, \
    QRect, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QWidget

from common.loader.resource import ResourceLoader
from common.util.func import calculate_text_rect, calculate_middle_rect
from common.util.worker import Worker

'''
QListView模型，配合ListDelegate使用
'''

class ListState:
    IDLE = 0
    LOADING = 1
    NOMORE = 2

class ListModel(QStringListModel):
    m_dataList = []  # 存储数据的容器
    m_pageSize = 20  # 每页显示的数据量
    m_pageNum = 0    # 当前页数

    def __init__(self, *args, api, **kwargs):
        super(ListModel, self).__init__(*args, **kwargs)

        self.api = api

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        '''
        列表不可编辑
        '''
        if not index.isValid():
            return QAbstractItemModel.flags(index)

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        return flags

    def rowCount(self, parent: QModelIndex = ...):
        return len(self.m_dataList)

    def updateData(self, data):
        # 1).隐藏更多数据项
        self.hideLoadMore()
        # 2).状态更新
        self.m_state = ListState.IDLE
        if len(data) == 0:
            self.m_state = ListState.NOMORE
            # 3).显示没有更多
            self.showNoMore()
        else:
            self.m_dataList.extend(data)
        self.beginResetModel()
        self.endResetModel()

    def loadMore(self):
        if self.m_state == ListState.IDLE:
            # 1).显示加载栏
            self.showLoadMore()
            # 2).更新状态
            self.m_state = ListState.LOADING
            # 3).加载数据
            self.fetchData(self.m_pageNum+1)

    def showLoadMore(self):
        self.m_dataList.append({ 'type': 'load_more', 'value': None })
        self.beginResetModel()
        self.endResetModel()

    def showNoMore(self):
        self.m_dataList.append({'type': 'no_more', 'value': None})
        self.beginResetModel()
        self.endResetModel()

    def hideLoadMore(self):
        if len(self.m_dataList) == 0:
            return
        item = self.m_dataList[-1]
        if item['type'] == 'load_more':
            self.m_dataList.remove(item)

    def data(self, index: QModelIndex, role: int = ...):
        '''
        用来显示数据，根据角色（颜色、文本、对齐方式、选中状态等）判断需要显示的内容
        '''
        if not index or len(self.m_dataList) == 0:
            return QVariant()

        data = self.m_dataList

        if Qt.DisplayRole == role:
            i = index.row()
            if i >= len(data):
                return QVariant()
            type = data[i]['type']
            value = data[i]['value']
            if type == 'string':
                return value
        if Qt.UserRole == role:
            i = index.row()
            if i >= len(data):
                return QVariant()
            return data[i]
        if Qt.TextAlignmentRole == role:
            return Qt.AlignCenter

        return QVariant()

    def fetchData(self, page=0):
        if not self.api:
            return
        # 1).更新页数
        self.m_pageNum = page
        if page == 0:
            self.m_dataList = []
        # 2).查询数据
        coroutine = self.api({'page': page, 'pagesize': self.m_pageSize}, callback=self.updateData)
        Worker().run_task(coroutine)

'''
QListWidget模型
'''

class ListWidgetModel(QStringListModel):
    m_dataList = []  # 存储数据的容器
    m_pageSize = 20  # 每页显示的数据量
    m_pageNum = 0    # 当前页数

    on_data_update = pyqtSignal(list)

    def __init__(self, *args, view:QListWidget, api, **kwargs):
        super(ListWidgetModel, self).__init__(*args, **kwargs)

        self.view = view
        self.api = api

        self.on_data_update.connect(self.updateData)

    def updateData(self, data):
        # 1).隐藏更多数据项
        self.hideLoadMore()
        # 2).状态更新
        self.m_state = ListState.IDLE
        if len(data) == 0:
            self.m_state = ListState.NOMORE
            # 3).显示没有更多
            self.showNoMore()
        else:
            for index, _item in enumerate(data):
                value = _item['value']
                widget = _item['item_cell'](data=value)
                item = QListWidgetItem()
                size = _item['size']
                item.setSizeHint(size)
                self.view.addItem(item)
                self.view.setItemWidget(item, widget)
                # # 保存默认列表项用于操作
                _item['item'] = item
            self.m_dataList.extend(data)
        self.beginResetModel()
        self.endResetModel()

    def loadMore(self):
        if self.m_state == ListState.IDLE:
            # 1).显示加载栏
            self.showLoadMore()
            # 2).更新状态
            self.m_state = ListState.LOADING
            # 3).加载数据
            self.fetchData(self.m_pageNum+1)

    def showLoadMore(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 50))
        self.view.addItem(item)
        self.view.setItemWidget(item, LoadMore())
        self.m_dataList.append({ 'type': 'load_more', 'value': None, 'item': item })
        self.beginResetModel()
        self.endResetModel()

    def showNoMore(self):
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 50))
        self.view.addItem(item)
        self.view.setItemWidget(item, NoMore())
        self.m_dataList.append({'type': 'no_more', 'value': None, 'item': item})
        self.beginResetModel()
        self.endResetModel()

    def hideLoadMore(self):
        if len(self.m_dataList) == 0:
            return
        item = self.m_dataList[-1]
        if item['type'] == 'load_more':
            self.view.takeItem(self.view.indexFromItem(item['item']).row())
            self.m_dataList.remove(item)

    def data(self, index: QModelIndex, role: int = ...):
        '''
        用来显示数据，根据角色（颜色、文本、对齐方式、选中状态等）判断需要显示的内容
        '''
        if not index or len(self.m_dataList) == 0:
            return QVariant()

        data = self.m_dataList

        if Qt.UserRole == role:
            i = index.row()
            if i >= len(data):
                return QVariant()
            return data[i]
        if Qt.TextAlignmentRole == role:
            return Qt.AlignCenter

        return QVariant()

    def fetchData(self, page=0):
        if not self.api:
            return
        # 1).更新页数
        self.m_pageNum = page
        if page == 0:
            self.m_dataList = []
        # 2).查询数据
        coroutine = self.api({'page': page, 'pagesize': self.m_pageSize})
        Worker().run_task(coroutine)

'''
没有更多组件
'''

class LoadMore(QWidget):
    def __init__(self, *args, **kwargs):
        super(LoadMore, self).__init__(*args, **kwargs)

        self.loading_rotate = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda :self.update())
        self.timer.start(40)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)

        rect = self.rect()
        w = rect.width()
        h = rect.height()

        # 绘制加载信息
        painter.save()
        painter.setFont(ResourceLoader().qt_font_text_xs)
        painter.setPen(ResourceLoader().qt_color_sub_text)
        _text_rect = calculate_text_rect('正在努力加载', painter=painter)
        text_rect = calculate_middle_rect(rect, width=_text_rect.width(), height=_text_rect.height())
        painter.translate(QPoint(12, 0))
        painter.drawText(text_rect, Qt.TextSingleLine, '正在努力加载')
        painter.restore()
        # 绘制加载图标
        x2 = w/2-text_rect.width()/2-16
        y2 = h/2
        painter.save()
        painter.translate(x2, y2)
        self.loading_rotate += 14
        painter.rotate(self.loading_rotate%360)
        # icon = qtawesome.icon('fa5s.spinner', color=ResourceLoader().qt_color_sub_text)
        icon = qtawesome.icon('mdi.loading', color=ResourceLoader().qt_color_sub_text)
        icon_pixmap = icon.pixmap(QSize(24, 24))
        painter.drawPixmap(QRect(-12, -12, 24, 24), icon_pixmap)
        painter.restore()

        QWidget.paintEvent(self, event)

'''
没有更多组件
'''

class NoMore(QWidget):
    def __init__(self, *args, **kwargs):
        super(NoMore, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)

        rect = self.rect()

        # 绘制文本
        painter.save()
        painter.setFont(ResourceLoader().qt_font_text_xs)
        painter.setPen(ResourceLoader().qt_color_sub_text)
        _text_rect = calculate_text_rect('--- 我是有底线的 ---', painter=painter)
        text_rect = calculate_middle_rect(rect, width=_text_rect.width(), height=_text_rect.height())
        painter.drawText(text_rect, Qt.TextSingleLine, '--- 我是有底线的 ---')
        painter.restore()

        QWidget.paintEvent(self, event)