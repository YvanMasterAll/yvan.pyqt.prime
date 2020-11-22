import os
import sys
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolButton, QVBoxLayout, QWidget, QPushButton
from qtpy import QtGui, QtCore
from six import unichr
import qtawesome as qta

class Window(QMainWindow):
    css = """
        QToolButton#btn1{{
            border: None;
            color: red;
        }}
        QToolButton#btn2{{
            border: None;
            color: blue;
        }}
        QPushButton#btn3{{
            background: red;
            color: orange;
        }}
    """

    def __init__(self):
        super(Window, self).__init__()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "../../resources/font/fontawesome-webfont.ttf"))
        if font_id is not -1:
            fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(fontName, 32)
        self.home()

    def home(self):
        self.setStyleSheet(self.css.format())

        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QVBoxLayout()
        wid.setLayout(layout)

        btn = QToolButton(self)
        btn.setObjectName('btn1')
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        btn.setFont(self.font)
        btn.setText(unichr(0xf241))
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)

        btn2 = QToolButton(self)
        btn2.setObjectName('btn2')
        btn2.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        btn2.setFont(self.font)
        btn2.setText(unichr(0xf241))
        btn2.clicked.connect(QtCore.QCoreApplication.instance().quit)

        styling_icon = qta.icon('fa5s.music',
                        active='fa5s.balance-scale',
                        color='blue',
                        color_active='orange')
        music_button = QPushButton(styling_icon, 'Styling')
        music_button.setObjectName('btn3')
        music_button.clicked.connect(QtCore.QCoreApplication.instance().quit)

        layout.setSpacing(0)
        layout.addWidget(btn)
        layout.addWidget(btn2)
        layout.addWidget(music_button)

        self.show()

def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()