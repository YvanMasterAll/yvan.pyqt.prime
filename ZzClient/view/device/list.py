import sys
from PyQt5.QtWidgets import QLabel, QApplication
from widget.view import BaseView

class DeviceList(BaseView):
    def __init__(self, *args, **kwargs):
        super(DeviceList, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        label = QLabel(self)
        label.setText("这是设备列表页面")