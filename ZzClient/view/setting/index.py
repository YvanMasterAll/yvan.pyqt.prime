import sys
from PyQt5.QtWidgets import QLabel, QApplication
from widget.view import BaseView

class SettingIndex(BaseView):
    def __init__(self, *args, **kwargs):
        super(SettingIndex, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        label = QLabel(self)
        label.setText("这是配置页面")