from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout, QApplication, QScrollArea
from PyQt5.QtCore import Qt, QPoint, QEvent, QRect, QRectF
from navbar import Navigation
from qtpy.QtGui import QPainter, QColor, QPen
import math

# 无边框Widget, 可拖拽拉伸

class QUnFrameWindow(QWidget):
    def __init__(self, parent=None):
        super(QUnFrameWindow, self).__init__(None, Qt.FramelessWindowHint)  # 设置为顶级窗口无边框

        self._setupUI()
        self._setupLayouts()
        self._setupDrags()  # 设置鼠标跟踪判断默认值

    def _setupUI(self):
        self.minHeight = 768
        self.minWidth = 1024
        self.setMinimumSize(self.minWidth, self.minHeight)

    def _setupLayouts(self):
        # 设置框架布局
        self._MainLayout = QVBoxLayout()
        self._MainLayout.setSpacing(0)
        self._MainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._MainLayout)

    def addLayout(self, QLayout):
        # 给widget定义一个addLayout函数，以实现往竖放框架的正确内容区内嵌套Layout框架
        self._MainLayout.addLayout(QLayout)

    def _setupDrags(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._right_bottom_corner_drag = False
        self._left_bottom_corner_drag = False
        self._drag_critical = 5

    def resizeEvent(self, QResizeEvent):
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小, 采用三个列表生成式生成三个列表
        self._left_rect = [QPoint(x, y) for x in range(0, self._drag_critical)
                           for y in range(5, self.height() - self._drag_critical)]
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._drag_critical, self.width() + 1)
                            for y in range(5, self.height() - self._drag_critical)]
        self._bottom_rect = [QPoint(x, y) for x in range(5, self.width() - self._drag_critical)
                             for y in range(self.height() - self._drag_critical, self.height() + 1)]
        self._right_bottom_corner_rect = [QPoint(x, y) for x in range(self.width() - self._drag_critical, self.width() + 1)
                                          for y in range(self.height() - self._drag_critical, self.height() + 1)]
        self._left_bottom_corner_rect = [QPoint(x, y) for x in range(0, self._drag_critical)
                                         for y in range(self.height() - self._drag_critical, self.height() + 1)]

    def _mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._right_bottom_corner_rect):
            # 鼠标左键点击右下角边界区域
            self._right_bottom_corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._left_bottom_corner_rect):
            # 鼠标左键点击左下角边界区域
            self._left_bottom_corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._left_rect):
            # 鼠标左键点击左侧边界区域
            self._left_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < 40):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def _mouseMoveEvent(self, QMouseEvent):
        #x = QMouseEvent.globalPos().x() - self.pos().x()
        #y = QMouseEvent.globalPos().y() - self.pos().y()
        x = QMouseEvent.pos().x()
        y = QMouseEvent.pos().y()
        # 判断鼠标位置切换鼠标手势
        if QMouseEvent.pos() in self._right_bottom_corner_rect:
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._left_bottom_corner_rect:
            QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            QApplication.setOverrideCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
        elif QMouseEvent.pos() in self._left_rect:
            QApplication.setOverrideCursor(Qt.SizeHorCursor)
        else:
            QApplication.restoreOverrideCursor()
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        if Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(x, self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._left_drag:
            # 左侧调整窗口高度
            if self.width() - x > self.minWidth:
                self.resize(self.width() - x, self.height())
                self.move(self.x() + x, self.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), y)
            QMouseEvent.accept()
        elif Qt.LeftButton and self._right_bottom_corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(x, y)
            QMouseEvent.accept()
        elif Qt.LeftButton and self._left_bottom_corner_drag:
            # 左下角同时调整高度和宽度
            if self.width() - x > self.minWidth:
                self.resize(self.width() - x, y)
                self.move(self.x() + x, self.y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def _setMouseTracking(self):
        def recursive_set(parent):
            for child in parent.findChildren(QFrame):
                try:
                    if type(child) is Navigation: # 管理子控件的鼠标跟踪事件, 如果不这么做, 主窗口的鼠标跟踪事件会被子控制器遮盖
                        child.installEventFilter(self)
                    child.setMouseTracking(True)
                except:
                    pass
                recursive_set(child)

        self.installEventFilter(self)
        self.setMouseTracking(True)
        recursive_set(self)

    def eventFilter(self, obj, event):
        if type(obj) is Navigation: # 将鼠标跟踪事件传递给子控件, 让子控件不会因为鼠标跟踪事件被接管而无法处理自身的事务
            if event.type() == QEvent.MouseButtonPress:
                obj._mousePressEvent(event)
        elif event.type() == QEvent.MouseMove:
            self._mouseMoveEvent(event)
        elif event.type() == QEvent.MouseButtonPress:
            self._mousePressEvent(event)

        return False

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._right_bottom_corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self._left_drag = False
        self._left_bottom_corner_drag = False

    # def paintEvent(self, event):
        # 绘制圆角方法一
        # path = QPainterPath()
        # rect = QRectF(0, 0, self.width(), self.height())
        # path.addRoundedRect(rect, 5, 5)
        # polygon = path.toFillPolygon().toPolygon() # 获得这个路径上的所有点
        # region = QRegion(polygon) # 根据这些点构造这个区域
        #
        # self.setMask(region)

        # 绘制圆角方法二
        # self.bitmap = QBitmap(self.size())  # 生成一张位图
        # painter = QPainter(self.bitmap)  # QPainter用于在位图上绘画
        #
        # painter.fillRect(self.rect(), Qt.white)  # 填充位图矩形框(用白色填充)
        # painter.setBrush(QColor(0, 0, 0))  # 黑色Brush
        # painter.setRenderHint(QPainter.Antialiasing, True) # 抗锯齿
        # painter.drawRoundedRect(self.rect(), 5, 5)  # 在位图上画圆角矩形(用黑色填充)
        #
        # self.setMask(self.bitmap)  # 使用setmask过滤即可