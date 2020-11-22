from PyQt5.QtCore import QTimer
from qtpy.QtWidgets import QFrame, QVBoxLayout, QPushButton
from qtpy import uic
from os.path import join, dirname, abspath
from widget.view import BaseView
from common.loader.resource import ResourceLoader

_ui = join(dirname(abspath(__file__)), '../widget/ui/frame/test2page.ui')

class Test2Page(BaseView, QFrame):
    def __init__(self, *args, **kwargs):
        super(Test2Page, self).__init__(*args, **kwargs)

        self.procedure()

    def set_ui(self):
        uic.loadUi(_ui, self)
        self.setObjectName('Test2Page')
        self.setStyleSheet("#Test2Page{background-color: 'yellow'; border-image: url(:icon/window_maximize.png); max-height:100px;}")
        self.layout = self.findChild(QVBoxLayout, "main")
        self.button = self.findChild(QPushButton, 'pushButton')
        self.resource.make_iconfont(self.button, self.fontawesome.icon_align_center, 24)
