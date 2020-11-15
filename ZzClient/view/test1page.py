from qtpy.QtWidgets import QFrame
from qtpy import uic
from os.path import join, dirname, abspath
from qtpy.QtCore import Slot
from widget.view import BaseView
from common.util.storage import LocalStorage

_ui = join(dirname(abspath(__file__)), '../widget/ui/frame/test1page.ui')

class Test1Page(BaseView, QFrame):
    def __init__(self, *args, **kwargs):
        super(Test1Page, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        uic.loadUi(_ui, self)
        self.setObjectName("Test1Page")
        self.setStyleSheet("QFrame{background: 'red';}")

    @Slot()
    def on_pushButton_clicked(self):
        theme = LocalStorage.themeGet()
        if theme == 'dark':
            self.theme.toggle('light')
        else:
            self.theme.toggle('dark')