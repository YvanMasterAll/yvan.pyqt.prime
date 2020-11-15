import sys
from PyQt5.QtWidgets import QLabel, QApplication
from widget.view import BaseView

class DatumAnalysis(BaseView):
    def __init__(self, *args, **kwargs):
        super(DatumAnalysis, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        label = QLabel(self)
        label.setText("这是数据分析页面")