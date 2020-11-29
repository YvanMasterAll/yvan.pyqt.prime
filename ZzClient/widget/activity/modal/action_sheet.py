import qtawesome
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint, QPropertyAnimation, QEasingCurve, QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QSpacerItem, \
    QGridLayout, QListWidget, QListWidgetItem
from widget.activity.drawer import Drawer
from widget.view import BaseView

class ActionSheet(BaseView):
    on_item_clicked = pyqtSignal(str)

    def __init__(self, *args, parent, data=[], **kwargs):
        super(ActionSheet, self).__init__(*args, **kwargs)

        self.data = data
        self.parent = parent
        self.procedure()

    def set_ui(self):
        self.list_view = QListWidget()
        self.list_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dialog = PopupContainer(widget=self)

    def configure(self):
        for item in self.data:
            li = QListWidgetItem()
            li.setText(item)
            li.setSizeHint(QSize(0, 38))
            self.list_view.addItem(li)
        self.list_view.itemClicked.connect(self.__on_item_clicked)

    def place(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.list_view)

    def __on_item_clicked(self, item):
        self.drawer.hideSelf()
        self.on_item_clicked.emit(item.text())

    def showSelf(self):
        if not hasattr(self, 'drawer'):
            self.drawer = Drawer(self.parent, stretch=0.9, direction=Drawer.BOTTOM, popup=False)
            self.dialog.on_drop.connect(lambda: self.drawer.hideSelf())
            self.drawer.setWidget(self.dialog)
        self.drawer.show()

class PopupContainer(BaseView):
    on_drop = pyqtSignal()

    def __init__(self, *args, widget:QWidget, size_w=600, backdrop=True, **kwargs):
        super(PopupContainer, self).__init__(*args, **kwargs)

        self.backdrop = backdrop
        self.widget = widget
        self.size_w = size_w
        self.procedure()

    def set_ui(self):
        self.container = QWidget()
        self.container.setObjectName('Container')
        self.container.setFixedWidth(self.size_w)
        self.btn_close = QPushButton()
        self.btn_close.setText("关闭")

    def place(self):
        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout_container = QVBoxLayout()
        layout_container.setSpacing(0)
        layout_container.setContentsMargins(12, 12, 12, 12)
        self.layout_action = QHBoxLayout()
        self.layout_action.setContentsMargins(0, 10, 0, 0)

        layout.addItem(QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 0, 1, 1, 1)
        layout.addWidget(self.container, 2, 2, 1, 1)
        self.container.setLayout(layout_container)
        layout_container.addWidget(self.widget)
        self.layout_action.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.layout_action.addWidget(self.btn_close)
        layout_container.addLayout(self.layout_action)

    def configure(self):
        self.btn_close.clicked.connect(lambda :self.on_drop.emit())

    def add_action(self, data, callback):
        btn = QPushButton()
        btn.setText(data)
        self.layout_action.insertWidget(0, btn)
        btn.clicked.connect(callback)

    def mousePressEvent(self, event) -> None:
        pos = event.pos()
        if self.backdrop and self.childAt(pos) == None and pos.x() < self.container.x() or pos.x() > self.container.x() + self.size_w or pos.y() < self.container.y():
            self.on_drop.emit()
            return
        super(PopupContainer, self).mousePressEvent(event)