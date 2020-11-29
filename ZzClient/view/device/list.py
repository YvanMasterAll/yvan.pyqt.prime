import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QApplication, QHBoxLayout

from common.loader.resource import ResourceLoader
from view.device.device_drawer import DeviceDrawer
from widget.activity.drawer import Drawer
from widget.activity.layout.grid_layout import GridLayout
from widget.frame.card.device_card import CardModel, State, DeviceCard
from widget.view import BaseView

class DeviceList(BaseView):
    devices = [
        CardModel(icon=ResourceLoader().render_pixmap('device_list_current.png'), sn='007', name='MM-370C', state=State.on, active='2020/11/16 11:24'),
        CardModel(icon=ResourceLoader().render_pixmap('device_list_current.png'), sn='011', name='MM-370C', state=State.off, active='2020/11/15 10:24'),
        CardModel(icon=ResourceLoader().render_pixmap('device_list_current.png'), sn='020', name='MM-370C', state=State.off, active='2020/11/15 15:24'),
    ]

    def __init__(self, *args, **kwargs):
        super(DeviceList, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        self.grid = GridLayout()
        self.grid.fixed_width = DeviceCard.fixed_width
        self.grid.fixed_height = DeviceCard.fixed_height
        cards = self.create_cards()
        QTimer.singleShot(0, lambda: self.grid.load(cards))

    def create_cards(self):
        cards = []
        for device in self.devices:
            card = DeviceCard(self.grid.center_widget, model=device)
            card.clicked.connect(self.open_drawer)
            cards.append(card)
        return cards

    def place(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.grid)

    def open_drawer(self):
        if not hasattr(self, 'drawer'):
            # 编写一个可以查找最外层的BaseActivity实例
            self.drawer = Drawer(self.parent().parent(), stretch=0.5, direction=Drawer.RIGHT, popup=False)
            self.drawer_widget = DeviceDrawer(self.drawer)
            self.drawer.setWidget(self.drawer_widget)
        QTimer.singleShot(0, lambda :self.drawer.show())