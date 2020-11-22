# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flattabwidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FlatTabWidget(object):
    def setupUi(self, FlatTabWidget):
        FlatTabWidget.setObjectName("FlatTabWidget")
        FlatTabWidget.resize(601, 352)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FlatTabWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MasterLayout = QtWidgets.QVBoxLayout()
        self.MasterLayout.setContentsMargins(-1, 0, -1, -1)
        self.MasterLayout.setSpacing(1)
        self.MasterLayout.setObjectName("MasterLayout")
        self.TabBarContainer = CustomTabBar(FlatTabWidget)
        self.TabBarContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.TabBarContainer.setObjectName("TabBarContainer")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.TabBarContainer)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.MasterLayout.addWidget(self.TabBarContainer)
        self.SeparatorContainer = QtWidgets.QWidget(FlatTabWidget)
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
        self.Content = QtWidgets.QStackedWidget(FlatTabWidget)
        self.Content.setObjectName("Content")
        self.MasterLayout.addWidget(self.Content)
        self.horizontalLayout.addLayout(self.MasterLayout)

        self.retranslateUi(FlatTabWidget)
        self.Content.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(FlatTabWidget)

    def retranslateUi(self, FlatTabWidget):
        _translate = QtCore.QCoreApplication.translate
        FlatTabWidget.setWindowTitle(_translate("FlatTabWidget", "FlatTabWidget"))

from customtabbar import CustomTabBar
