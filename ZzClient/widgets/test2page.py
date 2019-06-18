from qtpy.QtWidgets import QFrame, QVBoxLayout
from qtpy import uic
from os.path import join, dirname, abspath
from qtpy.QtCore import Slot

_ui = join(dirname(abspath(__file__)), '../resources/views/test2page.ui')

class Test2Page(QFrame):
    def __init__(self, parent=None):
        super(Test2Page, self).__init__()
        self.parent = parent

        uic.loadUi(_ui, self)
        self.setupUI()

    def setupUI(self):
        self.setObjectName('Test2Page')
        self.setStyleSheet("QFrame{background: 'yellow';}")
        self.layout = self.findChild(QVBoxLayout, "main")
