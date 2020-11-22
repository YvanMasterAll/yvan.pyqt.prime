import sys
from PyQt5.QtCore import pyqtSignal, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtGui import QPaintEvent, QWheelEvent
from PyQt5.QtWidgets import QWidget
from qtpy import QtWidgets, QtCore
from common.loader.resource import ResourceLoader
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetAnimation import StackedWidgetAnimation
from widget.frame.label.clickable_label import ClickableLabel

'''
FlatTabWidget，扁平选项卡，带底部指示器
'''

class CustomTabBar(QWidget):

    scrolledUp = pyqtSignal()
    scrolledDown = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(CustomTabBar, self).__init__(*args, **kwargs)

    def wheelEvent(self, event:QWheelEvent):
        if event.pixelDelta().y() > 5:
            self.scrolledUp.emit()
        elif event.pixelDelta().y() < -5:
            self.scrolledDown.emit()

class ColorRole:
    Active = 0
    Inactive = 1

class InsertPosition:
    InsertBefore = 0
    InsertAfter = 1

class FlatTabItem:
    def __init__(self, _label=None, _widget=None):
        self.label = _label
        self.widget = _widget
        self.fadeIn = QPropertyAnimation()
        self.fadeOut = QPropertyAnimation()

    def isValid(self):
        if self.label == None or self.widget == None:
            return False
        return True

class FlatTabWidget(QWidget):
    tabClicked = pyqtSignal(int)
    scrolledUp = pyqtSignal()
    scrolledDown = pyqtSignal()
    fadein = True # 是否添加淡入效果，默认True，注意需要设置边框为none，不然会变形

    def __init__(self, *args, **kwargs):
        super(FlatTabWidget, self).__init__(*args, **kwargs)

        self.setupUi()

        self.normal_color = ResourceLoader().qt_color_sub_text
        self.active_color = ResourceLoader().qt_color_text

        self.currentSelection = 0
        self.lineMorph = QPropertyAnimation()
        self.pages = []
        self.enqueueSeparatorRepaint = True
        self.animatePageChange = True
        self.customSW = None
        self.detachCustomStackedWidget = False

        def scrolledUp():
            if self.currentSelection - 1 < 0 or len(self.pages) == 0:
                return

            self.scrolledUp.emit()
            item = self.pages[self.currentSelection - 1]
            if item.label != None:
                self.setCurrentTab(self.currentSelection - 1)
        self.TabBarContainer.scrolledUp.connect(scrolledUp)

        def scrolledDown():
            if self.currentSelection + 1 >= len(self.pages) or len(self.pages) == 0:
                return

            self.scrolledDown.emit()
            item = self.pages[self.currentSelection + 1]
            if item.label != None:
                self.setCurrentTab(self.currentSelection + 1)
        self.TabBarContainer.scrolledDown.connect(scrolledDown)

    def setupUi(self):
        self.setObjectName("FlatTabWidget")
        self.resize(601, 352)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MasterLayout = QtWidgets.QVBoxLayout()
        self.MasterLayout.setContentsMargins(-1, 0, -1, -1)
        self.MasterLayout.setSpacing(1)
        self.MasterLayout.setObjectName("MasterLayout")
        self.TabBarContainer = CustomTabBar(self)
        self.TabBarContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.TabBarContainer.setObjectName("TabBarContainer")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.TabBarContainer)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.MasterLayout.addWidget(self.TabBarContainer)
        self.SeparatorContainer = QtWidgets.QWidget(self)
        self.SeparatorContainer.setMinimumSize(QtCore.QSize(0, 5))
        self.SeparatorContainer.setMaximumSize(QtCore.QSize(16777215, 5))
        self.SeparatorContainer.setObjectName("SeparatorContainer")
        self.SeparatorLine = QtWidgets.QLabel(self.SeparatorContainer)
        self.SeparatorLine.setGeometry(QtCore.QRect(0, 0, 100, 1))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SeparatorLine.sizePolicy().hasHeightForWidth())
        self.SeparatorLine.setSizePolicy(sizePolicy)
        self.SeparatorLine.setMaximumSize(QtCore.QSize(16777215, 1))
        self.SeparatorLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.SeparatorLine.setText("")
        self.SeparatorLine.setObjectName("SeparatorLine")
        self.MasterLayout.addWidget(self.SeparatorContainer)
        self.Content = QtWidgets.QStackedWidget(self)
        self.Content.setObjectName("Content")
        self.MasterLayout.addWidget(self.Content)
        self.horizontalLayout.addLayout(self.MasterLayout)

        self.retranslateUi()
        self.Content.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("FlatTabWidget", "FlatTabWidget"))

    def insertWidget(self, layout, reference, widget, pos=InsertPosition.InsertBefore, stretch=0, alignment=0):
        index = -1
        for i, item in enumerate(layout.count()):
            if item.widget() == reference:
                index = i
                break
        if index < 0:
            return False
        if pos == InsertPosition.InsertAfter:
            return False
        layout.insertWidget(index, widget, stretch, alignment)
        return True

    def addPage(self, title, page, index = -1):
        textcolor_active = self.getColor(ColorRole.Active)
        textcolor_disabled = self.getColor(ColorRole.Inactive)

        lbl = ClickableLabel()
        lbl.setText(title)
        if len(self.pages) == 0:
            lbl.setColor(textcolor_active)
            self.currentSelection = 0
        else:
            lbl.setColor(textcolor_disabled)
        lbl.clicked.connect(self.lblHandler)

        if index < 0:
            self.pages.append(FlatTabItem(lbl, page))
        else:
            self.pages.insert(index, FlatTabItem(lbl, page))
        self.updatePages()

    def updatePages(self, overrideSeparator=False):
        activeContainer = self.getActiveStackedWidget()
        spacer = self.TabBarContainer.layout().takeAt(len(self.TabBarContainer.layout()) - 1)
        wItem = self.TabBarContainer.layout().takeAt(0)
        while wItem:
            wItem.widget().hide()
            del wItem
            wItem = self.TabBarContainer.layout().takeAt(0)
        if not self.detachCustomStackedWidget:
            while len(activeContainer) > 0:
                widget = activeContainer.widget(0)
                activeContainer.removeWidget(widget)
        self.TabBarContainer.repaint()

        for page in self.pages:
            self.TabBarContainer.layout().addWidget(page.label)
            if not self.detachCustomStackedWidget:
                activeContainer.addWidget(page.widget)
            page.label.show()

        self.TabBarContainer.layout().addItem(spacer)

        if overrideSeparator:
            self.repaintDivider()

        self.setCurrentTab(self.currentSelection)

    def paintEvent(self, event):
        if self.enqueueSeparatorRepaint:
            if len(self.pages) == 0 or self.currentSelection < 0 or self.currentSelection >= len(self.pages):
                return

            button = self.pages[self.currentSelection].label
            rect = QRect(button.x(), 0, button.width(), button.height())
            self.lineMorph.stop()
            self.SeparatorLine.setGeometry(rect)
            self.enqueueSeparatorRepaint = False

        if event.type() == QPaintEvent.PaletteChange:
            self.redrawTabBar()

        QWidget.paintEvent(self, event)

    def showEvent(self, event):
        self.repaintDivider()
        self.setPalette(self.palette())
        QWidget.showEvent(self, event)

    def redrawTabBar(self):
        for page in self.pages:
            page.label.setColor(self.getColor(ColorRole.Inactive))
        temp = self.currentSelection
        self.setCurrentTab(temp)

    def removePage(self, id):
        textcolor_disabled = self.getColor(ColorRole.Inactive)

        if len(self.pages) != 0 and id >= 0 and id < len(self.pages):
            if id < len(self.pages) - 1:
                self.pages[id + 1].label.setColor(textcolor_disabled)
            self.pages.remove(id)
        self.updatePages()

    def setCurrentTab(self, id):
        if len(self.pages) == 0:
            return
        if id < 0:
            id = 0
        if id >= len(self.pages):
            id = len(self.pages) - 1

        textcolor_active = self.getColor(ColorRole.Active)
        textcolor_disabled = self.getColor(ColorRole.Inactive)
        button = self.pages[id].label
        rect = QRect(button.x(), 0, button.width(), button.height())
        if id == self.currentSelection:
            self.pages[id].label.setColor(textcolor_active)
            self.lineMorph.stop()
            self.SeparatorLine.setGeometry(rect)
        else:
            self.pages[id].fadeIn.stop()
            self.pages[id].fadeOut.stop()
            self.pages[id].fadeIn = QPropertyAnimation(self.pages[id].label, b"_color")
            self.pages[id].fadeIn.setDuration(300)
            self.pages[id].fadeIn.setStartValue(textcolor_disabled)
            self.pages[id].fadeIn.setEndValue(textcolor_active)

            if len(self.pages) > self.currentSelection:
                self.pages[self.currentSelection].fadeIn.stop()
                self.pages[self.currentSelection].fadeOut.stop()
                self.pages[self.currentSelection].fadeOut = QPropertyAnimation(self.pages[self.currentSelection].label, b"_color")
                self.pages[self.currentSelection].fadeOut.setDuration(300)
                self.pages[self.currentSelection].fadeOut.setStartValue(textcolor_active)
                self.pages[self.currentSelection].fadeOut.setEndValue(textcolor_disabled)
                self.pages[self.currentSelection].fadeOut.start()
            self.pages[id].fadeIn.start()

        self.lineMorph.stop()
        self.lineMorph = QPropertyAnimation(self.SeparatorLine, b"geometry")
        self.lineMorph.setDuration(300)
        self.lineMorph.setEasingCurve(QEasingCurve.OutCirc)
        self.lineMorph.setStartValue(self.SeparatorLine.geometry())
        self.lineMorph.setEndValue(rect)
        self.lineMorph.start()

        if self.animatePageChange:
            widget = self.getActiveStackedWidget().widget(id)
            if widget != None:
                if self.fadein:
                    StackedWidgetAnimation.fadeIn(self.getActiveStackedWidget(), widget)
                else:
                    self.getActiveStackedWidget().setCurrentWidget(widget)
        else:
            self.getActiveStackedWidget().setCurrentIndex(id)
        self.currentSelection = id

    def getCurrentTab(self):
        return self.currentSelection

    def repaintDivider(self):
        self.enqueueSeparatorRepaint = True
        self.repaint()

    def getActiveStackedWidget(self):
        if self.customSW != None:
            return self.customSW
        else:
            return self.Content

    def getColor(self, role):
        if role == ColorRole.Active:
            return self.active_color
        else:
            return self.normal_color

        # pal = self.palette()
        # textcolor_active = pal.color(QPalette.ButtonText).darker(0)
        # textcolor_disabled_light = pal.color(QPalette.Disabled, QPalette.WindowText).darker(150)
        # textcolor_disabled_dark = pal.color(QPalette.Disabled, QPalette.WindowText).lighter(150)
        #
        # if role == ColorRole.Active:
        #     return textcolor_active
        # else:
        #     return textcolor_disabled_dark

    def getItem(self, id):
        if id >= 0 and id < len(self.pages):
            return self.pages[id]
        return FlatTabItem()

    def getItem(self, title):
        id = self.getId(title)
        if id < 0:
            return FlatTabItem()
        else:
            return self.getItem(id)

    def getId(self, title):
        for index, page in enumerate(self.pages):
            if page.label.text() == title:
                return index
        return -1

    def lblHandler(self):
        id = self.getId(self.sender().text())
        if id >= 0:
            self.setCurrentTab(id)
            self.tabClicked.emit(id)

    def getDetachCustomStackedWidget(self):
        return self.detachCustomStackedWidget

    def setDetachCustomStackedWidget(self, value):
        self.detachCustomStackedWidget = value

    def getCustomStackWidget(self):
        return self.customSW

    def setCustomStackWidget(self, value):
        self.customSW = value
        if value == None:
            self.Content.show()
        else:
            self.Content.hide()

    def getAnimatePageChange(self):
        return self.animatePageChange

    def setAnimatePageChange(self, value):
        self.animatePageChange = value