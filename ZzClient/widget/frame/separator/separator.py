from PyQt5.QtWidgets import QFrame


class Separator(QFrame):
    def __init__(self, *args, orientation='horizontal', **kwargs):
        super(Separator, self).__init__(*args, **kwargs)

        if orientation == 'horizontal':
            self.setFrameShape(QFrame.HLine)
            self.setMinimumHeight(4)
        else:
            self.setFrameShape(QFrame.VLine)
            self.setMinimumWidth(4)
        self.setFrameShadow(QFrame.Sunken)


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