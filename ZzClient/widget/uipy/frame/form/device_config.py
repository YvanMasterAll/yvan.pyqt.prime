# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '_form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class DeviceConfigForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(594, 449)
        Form.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.input_device_name = QtWidgets.QLineEdit(self.widget)
        self.input_device_name.setObjectName("input_device_name")
        self.gridLayout_2.addWidget(self.input_device_name, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 3, 1, 1)
        self.combo_lead = QtWidgets.QComboBox(self.widget)
        self.combo_lead.setObjectName("combo_lead")
        self.gridLayout_2.addWidget(self.combo_lead, 1, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.radio_state_on = QtWidgets.QRadioButton(self.widget)
        self.radio_state_on.setObjectName("radio_state_on")
        self.horizontalLayout.addWidget(self.radio_state_on)
        self.radio_state_off = QtWidgets.QRadioButton(self.widget)
        self.radio_state_off.setObjectName("radio_state_off")
        self.horizontalLayout.addWidget(self.radio_state_off)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.input_company_name = QtWidgets.QLineEdit(self.widget)
        self.input_company_name.setObjectName("input_company_name")
        self.gridLayout_2.addWidget(self.input_company_name, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 3, 1, 1)
        self.date_maintain = QtWidgets.QDateTimeEdit(self.widget)
        self.date_maintain.setMinimumSize(QtCore.QSize(0, 0))
        self.date_maintain.setCalendarPopup(True)
        self.date_maintain.setObjectName("date_maintain")
        self.gridLayout_2.addWidget(self.date_maintain, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayout_2.setColumnMinimumWidth(1, 200)
        self.gridLayout_2.setColumnMinimumWidth(4, 200)
        self.gridLayout_2.setRowMinimumHeight(0, 38)
        self.gridLayout_2.setRowMinimumHeight(1, 38)
        self.gridLayout_2.setRowMinimumHeight(2, 38)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "设备名称"))
        self.input_device_name.setPlaceholderText(_translate("Form", "输入设备名称"))
        self.label_4.setText(_translate("Form", "维护日期"))
        self.label_3.setText(_translate("Form", "设备状态"))
        self.radio_state_on.setText(_translate("Form", "激活"))
        self.radio_state_off.setText(_translate("Form", "禁用"))
        self.input_company_name.setPlaceholderText(_translate("Form", "输入公司名称"))
        self.label_5.setText(_translate("Form", "负责人"))
        self.label_2.setText(_translate("Form", "公司名称"))
        self.pushButton_2.setText(_translate("Form", "提交"))
        self.pushButton.setText(_translate("Form", "保存"))
        self.pushButton_3.setText(_translate("Form", "关闭"))

