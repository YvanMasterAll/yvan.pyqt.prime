import qtawesome
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QLabel, QStyle, \
    QSizePolicy
from qtpy import QtCore, QtWidgets, QtGui
from widget.base_activity import BaseActivity
from widget.frame.bar.dialog_titlebar import DialogTitleBar

'''
自定义提示框，支持自定义控件
'''

class CustomDialog(BaseActivity):
    PROMOT, CUSTOM = range(2)

    on_confirm = pyqtSignal()
    on_cancel = pyqtSignal()

    __promot_padding = 20
    __action_height = 44

    def __init__(self, *args, widget=None, msg='确认信息', type=0, width=400, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.__widget = widget
        self.__width = width
        self.__msg = msg
        self.__type = type
        self.procedure()
        self._drag_ignore_fixed = True
        self.setMouseTracking(True)  # 设置鼠标跟踪，激活窗体拉伸和拖拽

    def set_ui(self):
        # 标题栏
        self.titlebar = DialogTitleBar(self, title="自定义对话框")
        self.bar = self.titlebar
        # 容器
        self.container = QWidget()
        self.container.setObjectName("Container")
        # 主要内容
        if self.__type == CustomDialog.PROMOT:
            self.body = QWidget()
            self.label = QLabel(self.__msg)
            self.label.setWordWrap(True)
            self.label.setFont(self.resource.qt_font_text_sm)
        elif self.__type == CustomDialog.CUSTOM:
            self.body = self.__widget
        # 操作栏
        self.widget_action = QWidget()
        self.widget_action.setObjectName("Action")
        self.widget_action.setFixedHeight(self.__action_height)
        self.btn_cancel = QPushButton()
        self.btn_cancel.setProperty("type", 1)
        self.btn_cancel.setText("取消")
        self.btn_cancel.clicked.connect(self.__on_cancel)
        self.btn_confirm = QPushButton()
        self.btn_confirm.setProperty("type", 1)
        self.btn_confirm.setIcon(qtawesome.icon('mdi.check', color=self.resource.qt_color_text))
        self.btn_confirm.setIconSize(QSize(18, 14))
        self.btn_confirm.setText("确认")
        self.btn_confirm.clicked.connect(self.__on_confirm)

    def place(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 标题栏
        self.layout.addWidget(self.titlebar)
        # 内容容器
        self.layout_container = QVBoxLayout()
        self.layout_container.setSpacing(0)
        self.layout_container.setContentsMargins(0, 0, 0, 0)
        self.container.setLayout(self.layout_container)
        self.layout.addWidget(self.container)
        # 主要内容
        if self.__type == CustomDialog.PROMOT:
            self.layout_body = QVBoxLayout()
            self.body.setLayout(self.layout_body)
            self.layout_body.setContentsMargins(self.__promot_padding, self.__promot_padding, self.__promot_padding, self.__promot_padding)
            self.layout_container.addWidget(self.body)
            self.layout_body.addWidget(self.label)
        elif self.__type == CustomDialog.CUSTOM:
            self.layout_container.addWidget(self.body)
        # 操作栏
        self.layout_action = QHBoxLayout()
        self.widget_action.setLayout(self.layout_action)
        self.layout_action.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.layout_action.addWidget(self.btn_cancel)
        self.layout_action.addWidget(self.btn_confirm)
        self.layout_container.addWidget(self.widget_action)

        self.addLayout(self.layout)

    def resizeEvent(self, _event):
        self.updateSize()
        super(CustomDialog, self).resizeEvent(_event)

    def updateSize(self):
        # 计算高度
        # height = self.titlebar.height() + self.widget_action.height()
        # if self.__type == CustomDialog.PROMOT:
        #     fm = QFontMetrics(self.label.font())
        #     body_height = fm.boundingRect(QRect(self.__promot_padding, self.__promot_padding, self.__width, self.__width*10), Qt.TextWordWrap, self.__msg).height()
        #     body_height += self.__promot_padding*2
        #     height += body_height
        #     self.body.setFixedHeight(body_height)
        # else:
        #     height += self.body.height()
        # self.setFixedSize(self.__width, height)
        #
        # self.setFixedSize(self.__width, self.titlebar.height() + self.body.height() + self.widget_action.height())

        # 使用首选(preferred)高度
        self.setFixedSize(self.__width, self.sizeHint().height())

    def __on_cancel(self):
        self.close()
        self.on_cancel.emit()

    def __on_confirm(self):
        if self.__type == CustomDialog.PROMOT:
            self.close()
        self.on_confirm.emit()

    def show(self):
        self.exec_()