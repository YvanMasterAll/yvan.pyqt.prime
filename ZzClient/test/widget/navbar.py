import sys
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem
import resource.qss.theme.dark.style_rc
from view.home.navbar import NavBar

Style = '''
Window {
    background-color: #333842;   
}
NavBar > NavButton {
    background-color: #333842;
    border-radius: 6px;
}
NavBar > NavButton:hover {
    border: 1px solid #2354B3;
}
NavBar > NavButton:checked {
    background-color: #282C34;
}
NavBar > Separator {
    background-color: #333842;
}
'''

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        layout = QVBoxLayout()
        self.setLayout(layout)
        navbar = NavBar(self)
        layout.addWidget(navbar)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    fontDB = QFontDatabase()
    font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
    fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont('Microsoft YaHei'))
    window = Window()
    window.show()

    sys.exit(app.exec_())