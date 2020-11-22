from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QLabel


class BaseLineEdit(QLineEdit):
    editSig = pyqtSignal()

    def __init__(self, *args, leftWidget=None, rightWidget=None, **kwargs):
        super(BaseLineEdit, self).__init__(*args, **kwargs)

        self.textSelectionEnabled = True
        self.leftRightLayout = None
        self.leftWidget = leftWidget
        self.rightWidget = rightWidget

        if self.leftWidget or self.rightWidget:
            # 对行编辑框内的部件进行布局
            self.leftRightLayout = QHBoxLayout(self)
            self.leftRightLayout.setContentsMargins(2, 2, 2, 2)
            self.leftRightLayout.setSpacing(0)
            if self.leftWidget:
                self.leftRightLayout.addWidget(leftWidget)
            self.leftRightLayout.addStretch()
            if self.rightWidget:
                self.leftRightLayout.addWidget(rightWidget)

    def emitEditSig(self):
        '''
        @brief:   主动发射编辑信号editSig()
        因为Qt4中signals是protected权限，无法类外调用，所以这里设置一个public权限接口，实现在类外
        调用主动发射编辑信号
        @author:  缪庆瑞
        @date:    2020.05.26
        '''
        self.setFocus()
        self.editSig.emit()

    def setLeftRightLayoutMargin(self, left=0, right=0, top=0, bottom=0):
        '''
        *@brief:   设置行编辑框左右布局margin，主要为了方便调整左右侧部件的位置
        *@author:  缪庆瑞
        *@date:    2020.04.11
        *@param:   left:左边间距 right:右边间距
        *@param:   top:上边间距 bottom:下边间距 默认0,一般不需要调整
        '''
        if self.leftRightLayout:
            self.leftRightLayout.setContentsMargins(left, top, right, bottom)
            '''
            在编辑框显示之前左右部件的大小如果没有fixed，那么默认将采用部件自身的推荐大小。所以
            这里只在部件显示(内部已完成布局)的情况下才自动调整文本的margin，避免按照部件推荐大小
            设置margin导致编辑框的大小策略受到不良影响。
            '''
            if self.isVisible():
                self.autoAdjustTextMargins()

    def mouseMoveEvent(self, event):
        '''
        *@brief:   鼠标移动事件处理
        *@author:  缪庆瑞
        *@date:    2020.05.20
        *@param:   event:鼠标事件
        '''
        if self.textSelectionEnabled:
            QLineEdit.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        '''
        *@brief:   鼠标释放事件处理
        *@author:  缪庆瑞
        *@date:    2020.04.11
        *@param:   event:鼠标事件
        '''
        # 左键释放并且非只读模式
        if event.button() == Qt.LeftButton and not self.isReadOnly():
            self.editSig.emit()  # 发射编辑信号
        QLineEdit.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        '''
        *@brief:   鼠标双击事件处理
        *@author:  缪庆瑞
        *@date:    2020.05.20
        *@param:   event:鼠标事件
        '''
        if self.textSelectionEnabled:
            QLineEdit.mouseDoubleClickEvent(self, event)

    def resizeEvent(self, event):
        '''
        *@brief:   部件大小调整事件处理 (用来自动调整编辑框文本的margins)
        *@author:  缪庆瑞
        *@date:    2020.04.11
        *@param:   event:大小事件
        '''
        QLineEdit.resizeEvent(self, event)
        self.autoAdjustTextMargins()

    def autoAdjustTextMargins(self):
        '''
        *@brief:   根据布局的边距和部件的宽度，自动调整编辑框文本的margins
        *@author:  缪庆瑞
        *@date:    2020.04.11
        '''
        if self.leftRightLayout:
            leftMargin = self.leftWidget.width() if self.leftWidget else 0
            rightMargin = self.rightWidget.width() if self.rightWidget else 0
            leftMargin += self.leftRightLayout.contentsMargins().left()
            rightMargin += self.leftRightLayout.contentsMargins().right()
            # 设置编辑框的margin 确保文本不会被部件遮挡
            self.setTextMargins(leftMargin, 0, rightMargin, 0)
