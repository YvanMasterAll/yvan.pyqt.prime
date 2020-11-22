import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QCheckBox, QRadioButton, QVBoxLayout, QLabel
from qtpy import QtWidgets, QtCore
from config.theme import Theme
from widget.frame.tab.flat_tab import FlatTabWidget


class demopage(QWidget):
    def __init__(self, *args, text, **kwargs):
        super(demopage, self).__init__(*args, **kwargs)

        self.setupUi()

        widgets = []
        widgets.append(QPushButton("Test Button"))
        widgets.append(QPushButton("Click me!"))
        widgets.append(QLineEdit("Some random input field"))
        widgets.append(QLineEdit("Type here..."))
        widgets.append(QCheckBox("I'm a checkbox"))
        widgets.append(QCheckBox("Tick me!"))
        widgets.append(QRadioButton("I'm a radiobutton"))
        widgets.append(QRadioButton("Select me!"))

        self.textBrowser.setText(text)
        for i in range(8):
            self.layout().addWidget(widgets[i])

    def setupUi(self):
        self.setObjectName("demopage")
        self.resize(356, 217)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Form"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    # fontDB = QFontDatabase()
    # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
    # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
    # app.setFont(QFont('Microsoft YaHei'))

    w = FlatTabWidget()
    w.setContentsMargins(9, 9, 9, 9)

    w.addPage("Tab 1", demopage(text="This is the first tab!"), 0)
    w.addPage("Tab 2", demopage(text="This is the second tab!"), 1)
    w.addPage("Tab 3", demopage(text="This is the third tab!"), 2)
    w.addPage("Tab 4", demopage(text="This is the fourth tab!"), 3)
    # w.addPage("Tab 5", demopage(text="This is the fifth tab!"), 4)
    # w.addPage("Tab 6", demopage(text="This is the fifth tab!"), 5)
    # w.addPage("Tab 7", demopage(text="This is the fifth tab!"), 6)
    w.addPage("Tab 8", demopage(text="This is the fifth tab!"), 7)
    w.addPage("Extremely long title", demopage(text="This is the sixth tab!"), 8)
    w.addPage("Long title", demopage(text="This is the seventh tab!"), 9)
    # w.addPage("Long title", demopage(text="This is the seventh tab!"), 10)
    # w.addPage("Long title", demopage(text="This is the seventh tab!"), 11)
    # w.addPage("Long title", demopage(text="This is the seventh tab!"), 12)

    w.show()

    w.setFixedSize(500, 500)

    w.setStyleSheet('''
    QStackedWidget {
        border: none;
        padding: 0;
    }
    #SeparatorLine {
        background-color: #FFFEFE;
    }
    ''')

    sys.exit(app.exec_())



