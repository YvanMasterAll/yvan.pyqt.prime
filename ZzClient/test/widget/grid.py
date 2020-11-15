# import sys
# from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
# from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
# from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem
# from qtpy import QtCore, QtWidgets
# import resource.qss.theme.dark.style_rc
# from config.theme import Theme
# from view.home.sidebar import SideBar
# from widget.activity.layout.grid_layout import GridLayout
# from widget.frame.button.mrxy.mrxy_button import MrxyButton
# from widget.frame.card.zoom_card import CardModel, ZoomCard
# from widget.view import BaseView
#
# Style = '''
# Window {
#     background-color: #282C34;
# }
# '''
#
# class Window(QWidget):
#     def __init__(self, *args, **kwargs):
#         super(Window, self).__init__(*args, **kwargs)
#
#         self.resize(800, 600)
#
#         layout = QHBoxLayout(self)
#         grid = GridLayout()
#         layout.addWidget(grid)
#         cards = []
#         for i in range(10):
#             pixmap = QPixmap(':icon/logo.png')
#             title = '凤翎谱' + str(i)
#             subTitle = "作者：北宫懒懒" + str(i)
#             cardModel = CardModel(pixmap, title, subTitle)
#             card = ZoomCard(grid.center_widget, model=cardModel)
#             cards.append(card)
#         grid.fixed_width = ZoomCard.fixed_width
#         grid.fixed_height = ZoomCard.fixed_height
#         QTimer.singleShot(0, lambda :grid.load(cards))
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setStyleSheet(Style)
#     # fontDB = QFontDatabase()
#     # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
#     # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
#     # app.setFont(QFont('Microsoft YaHei'))
#     window = Window()
#     window.show()
#
#     sys.exit(app.exec_())

import sys
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem
from qtpy import QtCore, QtWidgets
import resource.qss.theme.dark.style_rc
from config.theme import Theme
from view.home.sidebar import SideBar
from widget.activity.layout.grid_layout import GridLayout
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.card.device_card import CardModel, DeviceCard, State
from widget.view import BaseView

Style = '''
Window {
    background-color: #282C34;   
}
'''

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(800, 600)

        layout = QHBoxLayout(self)
        grid = GridLayout()
        layout.addWidget(grid)
        cards = []
        for i in range(2):
            icon= QPixmap(':icon/logo.png')
            sn = '007'
            state = State.on
            active = '2020-11-15'
            CardModel(icon, sn, state, active)
            cardModel = CardModel(icon, sn, state, active)
            card = DeviceCard(grid.center_widget, model=cardModel)
            cards.append(card)
        grid.fixed_width = DeviceCard.fixed_width
        grid.fixed_height = DeviceCard.fixed_height
        QTimer.singleShot(0, lambda :grid.load(cards))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    # fontDB = QFontDatabase()
    # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
    # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
    # app.setFont(QFont('Microsoft YaHei'))
    window = Window()
    window.show()

    sys.exit(app.exec_())