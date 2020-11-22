import sys
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer, QRectF, QRect
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient, QPainter, \
    QPainterPath, QFontMetrics, QPen
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QLabel, \
    QSizePolicy
from idna import unichr
from qtpy import QtCore, QtWidgets
import resources.qss.theme.dark.style_rc
from common.loader.resource import ResourceLoader
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.tag.tag import Tag
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
QLabel {border: 2px solid red;border-radius: 8px;}
'''

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        tag = Tag(self)
        def test():
            tag.padding_h = 4
            tag.padding_v = 2
            tag.text = "在线"
            tag.text_color = QColor('#00FFA2')
            tag.border_color = QColor('#00FFA2')
            tag.update()
        QTimer.singleShot(0, lambda :test())
        layout.addWidget(tag)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    Theme.load()
    # fontDB = QFontDatabase()
    # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
    # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
    # app.setFont(QFont('Microsoft YaHei'))
    window = Window()
    window.show()

    sys.exit(app.exec_())