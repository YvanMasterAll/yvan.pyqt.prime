import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFrame, QApplication, QWidget, QVBoxLayout
from qtpy import QtWidgets


class Separator(QFrame):
    def __init__(self, *args, orientation='horizontal', **kwargs):
        super(Separator, self).__init__(*args, **kwargs)

        if orientation == 'horizontal':
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)

        self.setMinimumHeight(4)

        '''
        尺寸策略
        '''
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        # self.setSizePolicy(sizePolicy)
        # # 外线长度
        # self.setLineWidth(8)
        # # 内线长度
        # self.setMidLineWidth(2)
        # self.setMaximumHeight(10)

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(QSize(500, 500))
        self.setObjectName('Window')
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        spacerItem = QtWidgets.QSpacerItem(0, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout.addSpacerItem(spacerItem)
        separator = Separator(self)
        layout.addWidget(separator)
        spacerItem2 = QtWidgets.QSpacerItem(0, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout.addSpacerItem(spacerItem2)
        separator2 = QWidget(self, objectName='Separator2')
        separator2.setMinimumHeight(20)
        separator2.setMaximumHeight(20)
        layout.addWidget(separator2)
        spacerItem3 = QtWidgets.QSpacerItem(0, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout.addSpacerItem(spacerItem3)
        separator3 = QWidget(self, objectName='Separator3')
        separator3.setMinimumHeight(20)
        separator3.setMaximumHeight(20)
        layout.addWidget(separator3)
        bottomWidget = QWidget(self, objectName='bottomWidget')
        layout.addWidget(bottomWidget)
        self.setLayout(layout)

Style = '''
#Window {
    background-color: #1F2020;
}
#bottomWidget {
    background-color: #323338;
}
Separator {
    background-color: #323338;
}
#Separator2 {
    border-bottom: 8px solid qlineargradient(
        x1:0,y1:1,x2:0,y2:0,
        stop:0 #313237,
        stop:0.2 #323338,
        stop:0.4 #323338,
        stop:0.44 #5B5C60
        stop:0.54 #1F2020,
        stop:0.70 #1C1D1D,
        stop:0.80 #4C4D4D,
        stop:0.84 #1F2020,
        stop:0.98 #1F2020,
        stop:1 #1D1E1E
    );
}
#Separator3 {
    border-bottom: 4px solid qlineargradient(
        x1:0,y1:1,x2:0,y2:0,
        stop:0 #313237,
        stop:0.2 #323338,
        stop:0.4 #323338,
        stop:0.44 #5B5C60
        stop:0.52 #1F2020,
        stop:0.86 #131313,
        stop:0.98 #1F2020,
        stop:1 #1D1E1E
    );
}
'''
# #Separator2 {
#     border-bottom: 8px solid qlineargradient(
#         x1:0,y1:1,x2:0,y2:0,
#         stop:0 #313237,
#         stop:0.2 #323338,
#         stop:0.5 #323338,
#         stop:0.54 #5B5C60
#         stop:0.62 #1F2020,
#         stop:0.80 #1C1D1D,
#         stop:0.91 #46474C
#         stop:0.95 #1F2020,
#         stop:0.98 #1F2020
#         stop:1 #1D1E1E
#     );
# }
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Style)
    window = Window()
    window.show()

    sys.exit(app.exec_())

