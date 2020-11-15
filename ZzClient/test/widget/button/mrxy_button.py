import sys

from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.button.mrxy.pointmenu_button import PointMenuButton
from widget.frame.button.mrxy.threedimen_button import ThreeDimenButton
from widget.frame.button.mrxy.watercircle_button import WaterCircleButton
from widget.frame.button.mrxy.waterfloat_button import WaterFloatButton
from widget.frame.button.mrxy.waterzoom_button import WaterZoomButton
from widget.frame.button.mrxy.winclose_button import WinCloseButton
from widget.frame.button.mrxy.winmax_button import WinMaxButton
from widget.frame.button.mrxy.winmenu_button import WinMenuButton
from widget.frame.button.mrxy.winmin_button import WinMinButton
from widget.frame.button.mrxy.winrestore_button import WinRestoreButton
import resource.qss.theme.dark.style_rc

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(560, 500)
        self.setMouseTracking(True)

        # layout = QVBoxLayout()
        # self.setLayout(layout)
        # btn = MrxyButton.by_text("hello", self)
        # btn.setGeometry(300, 300, 100, 100)
        # layout.addWidget(btn)

        btn = MrxyButton(self)
        btn.setGeometry(110, 100, 100, 100)
        btn.setBgColor(QColor(128, 0, 0, 100))
        btn.setRadius(5)

        menu_btn = WinMenuButton(self)
        menu_btn.setGeometry(368, 10, 32, 32)

        min_btn = WinMinButton(self)
        min_btn.setGeometry(400, 10, 32, 32)

        max_btn = WinMaxButton(self)
        max_btn.setGeometry(432, 10, 32, 32)

        res_btn = WinRestoreButton(self)
        res_btn.setGeometry(464, 10, 32, 32)

        close_btn = WinCloseButton(self)
        close_btn.setGeometry(496, 10, 32, 32)
        close_btn.setBgColor2(QColor('#000000'), QColor('#FF0000'))

        cir_btn = WaterCircleButton(self)
        cir_btn.setGeometry(528, 10, 32, 32)

        text_btn = MrxyButton.by_text("text", self)
        text_btn.setGeometry(0, 50, 100, 32)
        text_btn.setHoverAniDuration(5000)

        self.icon_btn = WaterCircleButton.by_icon(QIcon(":icon/window_maximize.png"), self)
        self.icon_btn.setGeometry(100, 50, 32, 32)
        self.icon_btn.setShowAni(True)
        self.icon_btn.setFixedForePos(True) # 和上面结合，即从中心开始出现和消失

        pixmap_btn = MrxyButton.by_pixmap(QPixmap(":icon/window_maximize.png"), self)
        pixmap_btn.setGeometry(132, 50, 32, 32)
        pixmap_btn.setDisabled(True)

        float_btn = WaterFloatButton.by_text("abcdefg", self)
        float_btn.setGeometry(164, 50, 100, 32)
        float_btn.setBgColor2(QColor(102,51,204,192), QColor(102,51,204,255))
        float_btn.setIconColor(QColor(102,51,204,192))

        par_btn = MrxyButton.by_text("abcdefg", self)
        par_btn.setGeometry(270, 50, 100, 32)
        par_btn.setParentEnabled(True)
        par_btn.setForeEnabled(False)
        par_btn.setStyleSheet('QPushButton{color: red;}')

        push_btn = QPushButton("parent", self)
        push_btn.setGeometry(370, 50, 100, 32)

        pm_btn = PointMenuButton(self)
        pm_btn.setGeometry(0, 100, 100, 100)
        pm_btn.radius_x = pm_btn.radius_y = 10
        pm_btn.border_bg = QColor('#FF0000')
        pm_btn.border_width = 3

        tdb = ThreeDimenButton(self)
        tdb.setGeometry(220, 100, 200, 100)
        tdb.setBgColor(QColor('#888888'))
        tdb.clicked.connect(lambda :print("3D按钮clicked"))
        tdb.signalMouseEnter.connect(lambda :print("mouseEnter"))
        tdb.signalMouseLeave.connect(lambda :print("mouseLeave"))
        tdb.signalMouseEnterLater.connect(lambda :print("mouseEnterLater"))
        tdb.signalMouseLeaveLater.connect(lambda :print("mouseLeaveLater"))
        tdb.signalMousePress.connect(lambda :print("mousePress"))
        tdb.signalMouseRelease.connect(lambda :print("mouseRelease"))
        tdb.signalMousePressLater.connect(lambda :print("mousePressLater"))
        tdb.signalMouseReleaseLater.connect(lambda :print("mouseReleaseLater"))

        zoom_btn1 = WaterZoomButton.by_text("tttttttttt", self)
        zoom_btn1.setGeometry(300, 200, 200, 50)
        zoom_btn1.setBgColor(QColor(240,128,128))
        zoom_btn1.setBgColor2(Qt.transparent, QColor(0x88, 0x88, 0x88, 0x64))
        zoom_btn1.setRadius(10, 5)
        zoom_btn1.setChokingProp(0.18)

        double_btn = MrxyButton(self)
        double_btn.setGeometry(510, 200, 50, 50)
        double_btn.setDoubleClicked(True)
        double_btn.setBgColor(QColor(102,51,204,192))
        double_btn.clicked.connect(lambda :print("单击"))
        double_btn.doubleClicked.connect(lambda :print("双击"))

        icon_text_btn = MrxyButton.by_icon_with_text("菜单", QIcon(":icon/window_maximize.png"), self)
        icon_text_btn.setGeometry(100, 300, 100, 40)

    def enterEvent(self, event):
        self.icon_btn.showForeground2()

        return super(Window, self).enterEvent(event)

    def leaveEvent(self, event):
        self.icon_btn.hideForeground()

        return super(Window, self).leaveEvent(event)

Style = '''

'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    window = Window()
    window.show()

    sys.exit(app.exec_())