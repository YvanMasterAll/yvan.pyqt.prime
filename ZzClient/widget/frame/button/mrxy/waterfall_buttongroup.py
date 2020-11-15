from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget
from widget.frame.button.mrxy.mrxy_button import MrxyButton
from widget.frame.button.mrxy.waterfloatbutton import WaterFloatButton


class WaterFallButtonGroup(MrxyButton):
    signalSelected = pyqtSignal(str)
    signalUnselected = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(WaterFallButtonGroup, self).__init__(*args, **kwargs)

        self.btns: list = []
        self.normal_bg: QColor = QColor(128,128,128,32)
        self.hover_bg: QColor = QColor(100,149,237,128)
        self.press_bg: QColor = QColor(100,149,237)
        self.selected_bg: QColor = QColor(100,149,237,128)
        self.normal_ft: QColor = QColor(0,0,0)
        self.selected_ft: QColor = QColor(255,255,255)

    def initStringList(self, list, selected):
        for s in list:
            self.addButton(s, selected.contains(s))

    def setSelects(self, list):
        for btn in self.btns:
            if btn.getText() == '':
                continue
            if list.contains(btn.getText()) and not btn.getState():
                self.selectBtn(btn)
            elif not list.contains(btn.getText()) and btn.getState():
                self.selectBtn(btn)

    def addButton(self, s, selected):
        btn = WaterFloatButton(s, self)
        btn.setFixedForeSize()
        self.setBtnColors(btn)
        self.btns.append(btn)

        if selected:
            self.selectBtn(btn)

        btn.setAutoTextColor(False)
        def block():
            self.selectBtn(btn)
            if btn.getState():
                self.signalSelected.emit(s)
            else:
                self.signalUnselected.emit()
        btn.clicked.connect(block)

    def addButton(self, s, c, selected):
        btn = WaterFloatButton(s, self)
        btn.setFixedForeSize()
        self.setBtnColors(btn)
        self.btns.append(btn)

        if selected:
            self.selectBtn(btn)

        btn.setAutoTextColor(False)
        btn.setTextColor(c)
        def block():
            self.selectBtn(btn)
            if btn.getState():
                self.signalSelected.emit(s)
            else:
                self.signalUnselected.emit()
        btn.clicked.connect(block)

    def setColors(self, normal_bg, hover_bg, press_bg, selected_bg, normal_ft, selected_ft):
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.press_bg = press_bg
        self.selected_bg = selected_bg
        self.normal_ft = normal_ft
        if selected_ft != Qt.transparent:
            self.selected_ft = selected_ft
        else:
            self.selected_ft = self.getReverseColor(selected_bg)

    def updateButtonPositions(self, ):
        space_h = 3
        space_v = 3
        total_w = self.width()
        w = space_v
        total_h = 0
        # 自动调整位置
        for btn in self.btns:
            btn_w = btn.width()
            if w == 0 or w + btn_w <= total_w: # 开头，或者同一行
                btn.move(w, total_h)
                w += btn_w + space_h
            else: # 另起一行
                total_h += btn.height() + space_v
                w = space_h
                btn.move(w, total_h)
                w += btn_w + space_h
        if len(self.btns) > 0:
            total_h += self.btns[-1].height()
        self.setFixedHeight(total_h)

    def resizeEvent(self, event):
        self.updateButtonPositions()

        QWidget.resizeEvent(self, event)

    def getReverseColor(self, color):
        return QColor(
                self.getReverseChannel(color.red()),
                self.getReverseChannel(color.green()),
                self.getReverseChannel(color.blue())
                    )

    def getReverseChannel(self, x):
        if x < 92 or x > 159:
            return 255 - x
        elif x < 128:
            return 255
        else: # if (x > 128)
            return 0

    def setBtnColors(self, btn):
        btn.setBgColor(self.normal_bg)
        btn.setBgColor(self.hover_bg, self.press_bg)

    def selectBtn(self, btn):
        btn.setState(not btn.getState())
        if btn.getState(): # 选中
            btn.setBgColor(self.selected_bg)
        else:
            btn.setBgColor(self.normal_bg)

