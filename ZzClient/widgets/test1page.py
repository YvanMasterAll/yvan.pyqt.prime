from qtpy.QtWidgets import QFrame
from qtpy import uic
from os.path import join, dirname, abspath
from qtpy.QtCore import Slot

_ui = join(dirname(abspath(__file__)), '../resources/views/test1page.ui')

class Test1Page(QFrame):
    def __init__(self, parent=None):
        super(Test1Page, self).__init__()
        self.parent = parent

        uic.loadUi(_ui, self)
        self.setupUI()

    def setupUI(self):
        self.setObjectName("Test1Page")
        self.setStyleSheet("QFrame{background: 'red';}")

    @Slot()
    def on_pushButton_clicked(self):
        print("hello")