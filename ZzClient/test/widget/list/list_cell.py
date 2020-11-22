# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list_cell.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class ListCell(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(669, 99)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(20, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon_device = QtWidgets.QLabel(Form)
        self.icon_device.setObjectName("icon_device")
        self.horizontalLayout.addWidget(self.icon_device)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setObjectName("label_name")
        self.verticalLayout.addWidget(self.label_name)
        self.label_content = QtWidgets.QLabel(Form)
        self.label_content.setObjectName("label_content")
        self.verticalLayout.addWidget(self.label_content)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.icon_device.setText(_translate("Form", "设备图标"))
        self.label_name.setText(_translate("Form", "设备名称"))
        self.label_content.setText(_translate("Form", "设备事件"))

