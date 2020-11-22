from PyQt5.QtWidgets import QListWidget

class BaseListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super(BaseListWidget, self).__init__(*args, **kwargs)

        self.isMoved = False
        self.originPosX = 0
        self.originPosY = 0

    def mousePressEvent(self, event):
        # 鼠标按住拖动
        self.originPosY = event.globalY()
        self.originPosX = event.globalX()
        QListWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        # 鼠标按住拖动
        varDiff = 0
        if self.flow() == QListWidget.TopToBottom:
            varDiff = self.verticalScrollBar().sliderPosition() - (event.globalY() - self.originPosY)
            self.verticalScrollBar().setSliderPosition(varDiff)
        else:
            varDiff = self.horizontalScrollBar().sliderPosition() - (event.globalX() - self.originPosX)
            self.horizontalScrollBar().setSliderPosition(varDiff)
        self.originPosY = event.globalY()
        self.originPosX = event.globalX()
        self.isMoved = True
        QListWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        # 鼠标按住拖动
        varDiff = 0
        if self.flow() == QListWidget.TopToBottom:
            varDiff = self.verticalScrollBar().sliderPosition() - (event.globalY() - self.originPosY)
            self.verticalScrollBar().setSliderPosition(varDiff)
        else:
            varDiff = self.horizontalScrollBar().sliderPosition() - (event.globalX() - self.originPosX)
            self.horizontalScrollBar().setSliderPosition(varDiff)
        if self.isMoved:
            if varDiff <= 0:
                print("已经到达顶部")
            elif varDiff >= self.verticalScrollBar().maximum():
                print("已经到达底部")

        self.isMoved = False
        self.originPosY = event.globalY()
        self.originPosX = event.globalX()
        QListWidget.mouseReleaseEvent(self, event)
