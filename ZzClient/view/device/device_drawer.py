import asyncio
import random
import qtawesome
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, \
    QLineEdit, QLabel, QHBoxLayout, QSpacerItem, QToolButton, QMenu, QGroupBox, QListView, QScrollArea, QAction
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication
from qtpy import QtWidgets, QtCore, QtGui
from common.loader.resource import ResourceLoader
from widget.activity.modal.action_sheet import ActionSheet
from widget.frame.form.baselineedit import BaseLineEdit
from widget.frame.list.base_list_view import BaseListView
from widget.frame.list.delegate import ListDelegate
from widget.frame.list.model import ListModel
from widget.frame.separator.separator import Separator
from widget.frame.tab.flat_tab import FlatTabWidget
from widget.frame.table.base_table import BaseTableView
from widget.frame.table.delegate import TableDelegate
from widget.frame.table.model import TableModel
from widget.frame.table.pagination import CPaginationBar
from widget.uipy.frame.form.device_config import DeviceConfigForm
from widget.view import BaseView

class TabPage2(QWidget, DeviceConfigForm):
    def __init__(self, *args, **kwargs):
        super(TabPage2, self).__init__(*args, **kwargs)

        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setupUi(self)

        # 验证器
        # self.input_company_name.setValidator(QIntValidator(0, 100))
        # 下拉选项框
        view = QListView(self.combo_lead)
        view.setStyleSheet("QListView::item{height: 32px}")
        self.combo_lead.setView(view)
        self.combo_lead.addItem("沈建")
        self.combo_lead.addItem("亿强")
        # 复选框
        self.radio_state_on.setChecked(True)


class TabPage1(BaseView):
    def __init__(self, *args, **kwargs):
        super(TabPage1, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        # 搜索栏
        label_icon_search = QLabel()
        label_icon_search.setPixmap(qtawesome.icon('fa5s.search', color=ResourceLoader().qt_color_sub_text).pixmap(QSize(18, 18)))
        label_icon_search.setFixedSize(20, 20)
        self.input_search = BaseLineEdit(leftWidget=label_icon_search)
        self.input_search.setFixedHeight(32)
        self.input_search.setLeftRightLayoutMargin(10, 10)
        self.input_search.setPlaceholderText("输入查询条件")
        self.btn_search = QPushButton()
        self.btn_search.setProperty("type", 1)
        self.btn_search.setText("查询")
        self.btn_search.clicked.connect(self.search)
        self.btn_reset = QPushButton()
        self.btn_reset.setProperty("type", 1)
        self.btn_reset.setText("重置")
        self.btn_reset.clicked.connect(self.reset)
        self.separator1 = Separator(self)
        self.separator1.setFixedHeight(2)
        # 表格
        self.tableView = BaseTableView(self)
        self.tableView.setObjectName("tableView")
        self.separator2 = Separator(self)
        self.separator2.setFixedHeight(2)
        # 分页栏
        self.paginationBar1 = CPaginationBar(self, totalPages=20)
        self.paginationBar1.setInfos('共 400 条')
        self.paginationBar1.setJumpWidget(True)
        self.paginationBar1.pageChanged.connect(lambda page: self.model.fetchData(page=page - 1))

    def place(self):
        gridLayout = QtWidgets.QGridLayout(self)
        gridLayout.setContentsMargins(11, 11, 11, 11)
        gridLayout.setSpacing(6)

        gridLayout.addWidget(self.input_search, 0, 0, 1, 1)
        gridLayout.addWidget(self.btn_search, 0, 1, 1, 1)
        gridLayout.addWidget(self.btn_reset, 0, 2, 1, 1)
        gridLayout.addWidget(self.separator1, 1, 0, 1, 10)
        gridLayout.addWidget(self.tableView, 2, 0, 1, 10)
        gridLayout.addWidget(self.separator2, 3, 0, 1, 10)
        gridLayout.addWidget(self.paginationBar1, 4, 0, 1, 10)

    def configure(self):
        # 表格模型
        self.model = TableModel(self, api=self.api, pagination=self.paginationBar1)
        self.tableView.setSelfMode(self.model)
        self.tableView.setDelegate(TableDelegate())
        self.tableView.setMenus(['编辑', '删除'])
        self.tableView.on_action_triggered.connect(self.on_action_triggered)
        # 加载数据
        self.model.fetchData()

    def on_action_triggered(self, action, data):
        print(action)
        print(data)

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
                    'type': {'value': '警告', 'text_color': ResourceLoader().qt_color_warning, 'border_color': ResourceLoader().qt_color_warning, 'font': ResourceLoader().qt_font_text_tag, 'type': 'tag'},
                    'check': {'value': 1, 'type': 'checkbox', 'size': 20 },
                    'content': {'value': '设备离线', 'type': 'string'},
                },
                {
                    'sn': {'value': '002', 'type': 'string'},
                    'type': {'value': '正常', 'text_color': ResourceLoader().qt_color_success,
                             'border_color': ResourceLoader().qt_color_success,
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

class DeviceDrawer(BaseView):
    def __init__(self, *args, **kwargs):
        super(DeviceDrawer, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        # 头部内容
        self.icon_header = QLabel()
        self.icon_header.setObjectName("Icon_Header")
        self.label_title = QLabel()
        self.label_title.setObjectName("Label_Title")
        self.label_title.setText("电流检测仪(MM-370C)")
        self.btn_edit = QPushButton()
        self.btn_edit.setObjectName("Btn_Edit")
        self.btn_edit.setProperty("type", 1)
        self.btn_edit.setIcon(qtawesome.icon('ei.edit', color=self.resource.qt_color_text))
        self.btn_edit.setText("编辑")
        self.btn_del = QPushButton()
        self.btn_del.setObjectName("Btn_Del")
        self.btn_del.setProperty("type", 3)
        self.btn_del.setIcon(qtawesome.icon('ei.trash', color=self.resource.qt_color_text))
        self.btn_del.setText("移除")
        self.btn_menu = QToolButton()
        self.btn_menu.setText("菜单")
        self.btn_menu.setObjectName("Btn_Menu")
        menu = QMenu()
        for action in ['弹出选项', '菜单项二', '菜单项三']:
            menu.addAction(action)
        menu.triggered.connect(self.on_menu_clicked)
        self.btn_menu.setMenu(menu)
        self.btn_menu.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.sep_header = Separator(self)
        self.sep_header.setObjectName("Sep_Header")
        self.sep_header.setFixedHeight(4)
        # 信息卡片
        self.gbox_info = QGroupBox()
        self.layout_info_grid = QGridLayout()
        self.layout_info_grid.setContentsMargins(10, 10, 10, 10)
        for index, info in enumerate([['型号', 'MM-370C'], ['公司', '中正智控'], ['负责人', '沈建'], ['状态', '在保']]):
            label = QLabel()
            label.setProperty("type", 100)
            label.setText(info[0])
            self.layout_info_grid.addWidget(label, index*2, 0, 1, 1)
            label = QLabel()
            label.setProperty("type", 101)
            label.setText(info[1])
            self.layout_info_grid.addWidget(label, index*2, 1, 1, 3)
            separator = Separator(self)
            separator.setFixedHeight(1)
            self.layout_info_grid.addWidget(separator, index*2+1, 0, 1, 4)
            self.layout_info_grid.setRowMinimumHeight(index*2, 30)
        self.gbox_info.setLayout(self.layout_info_grid)
        self.gbox_info.setTitle("设备信息")
        # 选项卡
        self.tab_pager = FlatTabWidget()
        self.tab_pager.fadein = False
        self.tab_pager.addPage("报警", TabPage1())
        self.tab_pager.addPage("配置", TabPage2())
        # 活动列表
        self.gbox_activity = QGroupBox()
        self.layout_gbox_activity = QVBoxLayout()
        self.gbox_activity.setLayout(self.layout_gbox_activity)
        self.list_activity = BaseListView()
        self.lv_model = ListModel(api=self.api)
        self.list_activity.setModel(self.lv_model)
        self.list_activity.setItemDelegate(ListDelegate())
        self.list_activity.verticalScrollBar().valueChanged.connect(self.scrollChanged)
        self.gbox_activity.setTitle("活动列表")
        self.gbox_activity.layout().addWidget(self.list_activity)
        self.lv_model.fetchData()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.scroll_widget.setMaximumWidth(self.width())

    def place(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_wrap = QVBoxLayout(self)
        scroll_wrap.setSpacing(0)
        scroll_wrap.setContentsMargins(0, 0, 0, 0)
        scroll_wrap.addWidget(self.scroll_area)
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        layout = QVBoxLayout(self.scroll_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout_title = QHBoxLayout()
        layout_title.setContentsMargins(10, 10, 10, 4)
        layout_info = QHBoxLayout()
        layout_info.setContentsMargins(10, 0, 10, 0)
        layout_tab = QHBoxLayout()
        layout_tab.setContentsMargins(10, 10, 10, 0)
        layout_activity = QHBoxLayout()
        layout_activity.setContentsMargins(10, 10, 10, 0)

        # 头部内容
        layout_title.addWidget(self.icon_header)
        layout_title.addWidget(self.label_title)
        layout_title.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        layout_title.addWidget(self.btn_edit)
        layout_title.addWidget(self.btn_del)
        layout_title.addWidget(self.btn_menu)
        layout.addLayout(layout_title)
        # 头部分隔线
        layout.addWidget(self.sep_header)
        # 信息卡片
        layout_info.addWidget(self.gbox_info)
        layout.addLayout(layout_info)
        # 选项卡
        layout_tab.addWidget(self.tab_pager)
        layout.addLayout(layout_tab)
        # 活动列表
        layout_activity.addWidget(self.gbox_activity)
        layout.addLayout(layout_activity)
        # 间隔
        layout.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def scrollChanged(self, value):
        if self.list_activity.verticalScrollBar().maximum() == value:
            self.list_activity.model().loadMore()

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

    def on_menu_clicked(self, action:QAction):
        text = action.text()
        if text == '弹出选项':
            self.show_sheet()
    #
    def show_sheet(self):
        if not hasattr(self, 'action_sheet'):
            self.action_sheet = ActionSheet(data=['电流检测', '电压检测', '电阻检测'], parent=self.parent())
            self.action_sheet.on_item_clicked.connect(lambda item:print('选中了{item}'.format(item=item)))
        self.action_sheet.showSelf()
