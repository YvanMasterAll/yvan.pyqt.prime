import sys
from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem
from qtpy import QtWidgets

import resource.qss.theme.dark.style_rc
from common.loader.resource import ResourceLoader
from widget.frame.button.navbutton import NavButton, TextAlign_Center, IconPosition_Top

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
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        navbutton = NavButton()
        navbutton.setObjectName('NavButton_{name}'.format(name='name'))
        navbutton.setFixedHeight(80)
        navbutton.setFixedWidth(94)
        navbutton.setShowText('你好')
        navbutton.setShowIcon(True)
        navbutton.setPaddingLeft(0)
        navbutton.setPaddingRight(0)
        navbutton.setPaddingTop(12)
        navbutton.setPaddingBottom(4)
        navbutton.setIconNormal(QPixmap(':icon/{icon}'.format(icon='navbar_home.png')))
        navbutton.setIconCheck(QPixmap(':icon/{icon}'.format(icon='navbar_home.png')))
        navbutton.setIconHover(QPixmap(':icon/{icon}'.format(icon='navbar_home.png')))
        navbutton.setTextAlign(TextAlign_Center)
        navbutton.setFont(ResourceLoader().qt_font_text_xs)
        navbutton.setIconSize(QSize(34, 34))
        navbutton.setIconPosition(IconPosition_Top)
        navbutton.setNormalBgColor(QColor('transparent'))
        navbutton.setHoverBgColor(QColor('transparent'))
        navbutton.setCheckBgColor(QColor('transparent'))
        navbutton.setNormalTextColor(QColor('#CDCDCD'))
        navbutton.setHoverTextColor(QColor('#FFFEFE'))
        navbutton.setCheckTextColor(QColor('#FFFEFE'))
        layout.addWidget(navbutton)
        navbutton = NavButton()
        navbutton.setObjectName('NavButton_{name}'.format(name='name'))
        navbutton.setFixedHeight(80)
        navbutton.setFixedWidth(94)
        navbutton.setShowText('你好')
        navbutton.setShowIcon(True)
        navbutton.setPaddingLeft(0)
        navbutton.setPaddingRight(0)
        navbutton.setPaddingTop(12)
        navbutton.setPaddingBottom(4)
        navbutton.setIconNormal(QPixmap(':icon/{icon}'.format(icon='navbar_home.png')))
        navbutton.setIconCheck(QPixmap(':icon/{icon}'.format(icon='navbar_home.png')))
        navbutton.setIconHover(QPixmap(':icon/{icon}'.format(icon='navbar_home.png')))
        navbutton.setTextAlign(TextAlign_Center)
        navbutton.setFont(ResourceLoader().qt_font_text_xs)
        navbutton.setIconSize(QSize(34, 34))
        navbutton.setIconPosition(IconPosition_Top)
        navbutton.setNormalBgColor(QColor('transparent'))
        navbutton.setHoverBgColor(QColor('transparent'))
        navbutton.setCheckBgColor(QColor('transparent'))
        navbutton.setNormalTextColor(QColor('#CDCDCD'))
        navbutton.setHoverTextColor(QColor('#FFFEFE'))
        navbutton.setCheckTextColor(QColor('#FFFEFE'))
        layout.addWidget(navbutton)
        spacerItem = QtWidgets.QSpacerItem(0, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addSpacerItem(spacerItem)

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