from qtpy.QtWidgets import QFrame, QVBoxLayout
from qtpy import uic
from os.path import join, dirname, abspath
from qtpy.QtCore import Slot
from ZzClient.widget.view import BaseView

_ui = join(dirname(abspath(__file__)), '../widget/ui/frame/test2page.ui')

class Test2Page(BaseView, QFrame):
    def __init__(self, *args, **kwargs):
        super(Test2Page, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        uic.loadUi(_ui, self)
        self.setObjectName('Test2Page')
        self.setStyleSheet("QFrame{background: 'yellow';}")
        self.layout = self.findChild(QVBoxLayout, "main")