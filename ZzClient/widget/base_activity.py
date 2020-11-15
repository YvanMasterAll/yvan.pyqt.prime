from PyQt5.QtGui import QKeyEvent, QMouseEvent, QPainterPath, QPainter, QBrush, QPixmap, QWindowStateChangeEvent, \
    QColor, QPen, QEnterEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QDialog
from PyQt5.QtCore import Qt, QPoint, QEvent, QRect
from PyQt5.QtCore import QObject
from widget.dialog import waiting_dialog
from common.util.logger import logger, logger_err
from widget.view import BaseView
from widget.frame.bar.titlebar import TitleBar

'''
页面基类
0).日志记录              
1).静态资源管理           
2).遮盖层                
3).最大最小化标题栏                
4).窗体拉伸 > self.setMouseTracking(True)
5).文件拖拽
6).无边框拖动窗体
'''

class BaseActivity(QDialog, BaseView):
    '''
    自定义标题栏
    '''
    bar: TitleBar = None

    '''
    窗口拖动位置
    '''
    _right_rect = []
    _bottom_rect = []
    _corner_rect = []

    '''
    扳机默认值
    '''
    _move_drag = False
    _corner_drag = False
    _bottom_drag = False
    _right_drag = False

    '''
    拖拽位置记录
    '''
    _move_drag_position = None

    def __init__(self, flags=None, *args, **kwargs):
        super().__init__(flags, *args, **kwargs)

        self._configure()

    def _configure(self):
        # 边距
        self.margin = 0
        # 日志对象
        self.logger = logger
        self.logger_err = logger_err
        # 顶级窗口无边框
        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint |
            Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint)
        # 窗口尺寸控制
        self.minHeight = 768
        self.minWidth = 1024
        self.resize(self.minWidth, self.minHeight)
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 框架布局
        self._main_layout = QVBoxLayout()
        self._main_layout.setSpacing(0)
        # 如果设置零边距，在窗口状态变更时(如最大化)，边角会出现空白区域
        self._main_layout.setContentsMargins(self.margin, self.margin, self.margin, self.margin)
        self.setLayout(self._main_layout)
        # 默认的遮罩层
        self.waiting_dialog = waiting_dialog()

    def addLayout(self, layout):
        '''
        往主布局中添加子布局
        '''
        self._main_layout.addLayout(layout)

    def alert(info):
        '''
        提示弹出框
        '''
        pass

    def isResizable(self):
        """是否可调整
        """
        return self.minimumSize() != self.maximumSize()

    def resizeEvent(self, _event):
        '''
        自定义窗口调整大小事件
        采用三个列表生成式生成三个列表, 用以保存一个鼠标可以拖动的范围
        '''
        if not self.bar:
            return
        # 右侧边界
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self.config.window_zoom_critical, self.width() + 1)
                            for y in range(self.bar.height(), self.height() + self.config.window_zoom_critical)]
        # 下边界
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() + self.config.window_zoom_critical)
                             for y in range(self.height() - self.config.window_zoom_critical, self.height() + 1)]
        # 右下边界
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self.config.window_zoom_critical, self.width() + 1)
                             for y in range(self.height() - self.config.window_zoom_critical, self.height() + 1)]

        '''
        重新调整边界范围以备实现鼠标拖拽缩放窗口大小, 采用三个列表生成式生成三个列表
        '''
        # self._right_rect = [QPoint(x, y) for x in range(self.width() - self.config.window_zoom_critical, self.width() + 1)
        #                     for y in range(5, self.height() - self.config.window_zoom_critical)]
        # self._bottom_rect = [QPoint(x, y) for x in range(5, self.width() - self.config.window_zoom_critical)
        #                      for y in range(self.height() - self.config.window_zoom_critical, self.height() + 1)]
        # self._corner_rect = [QPoint(x, y) for x in range(self.width() - self.config.window_zoom_critical, self.width() + 1)
        #                      for y in range(self.height() - self.config.window_zoom_critical, self.height() + 1)]

    def mousePressEvent(self, event):
        '''
        重构鼠标点击事件
        '''
        if not self.bar:
            return
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() <= self.bar.height()):
            self._move_drag = True
            self._move_drag_position = event.globalPos() - self.pos()
            event.accept()

        '''
        重写鼠标点击的事件
        '''
        # if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
        #     self._corner_drag = True
        #     event.accept()
        # elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
        #     self._right_drag = True
        #     event.accept()
        # elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
        #     self._bottom_drag = True
        #     event.accept()
        # elif (event.button() == Qt.LeftButton) and (event.y() < 40):
        #     self._move_drag = True
        #     self._move_drag_position = event.globalPos() - self.pos()
        #     event.accept()

    def mouseMoveEvent(self, _):
        '''
        判断鼠标位置是否移动到了边界以便更换鼠标样式
        '''
        if self.isMaximized() or self.isFullScreen() or not self.isResizable():
            # 最大化时不可移动
            return
        if _.pos() in self._corner_rect:
            self.setCursor(Qt.SizeFDiagCursor)
        elif _.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif _.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if Qt.LeftButton and self._right_drag:
            self.resize(_.pos().x(), self.height())
            _.accept()
        elif Qt.LeftButton and self._bottom_drag:
            self.resize(self.width(), _.pos().y())
            _.accept()
        elif Qt.LeftButton and self._corner_drag:
            self.resize(_.pos().x(), _.pos().y())
            _.accept()
        elif Qt.LeftButton and self._move_drag:
            self.move(_.globalPos() - self._move_drag_position)
            _.accept()

    def mouseReleaseEvent(self, _):
        '''
        鼠标释放后，各扳机复位
        '''
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def dragEnterEvent(self, event):
        '''
        判断拖拽物体是否有路径，如果有则拖拽生效
        '''
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        '''
        拖拽移动
        '''
        if event.mimeData().hasUrls:
            try:
                event.setDropAction(Qt.CopyAction)
            except Exception as e:
                pass
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        '''
        如果需要监听文件拖拽则重构此方法
        获取拖拽文件
        '''
        try:
            if event.mimeData().hasUrls:
                event.setDropAction(Qt.CopyAction)
                event.accept()
                links = []
                for url in event.mimeData().urls():
                    links.append(str(url.toLocalFile()))
                print(links)
            else:
                event.ignore()
        except Exception as e:
            raise e

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        '''
        双击的坐标小于头部坐标时才最大化, 如果不需要这个功能，在继承子类时重构此方法即可
        '''
        if not self.bar:
            return
        if e.pos().y() < self.bar.y() + self.bar.height():
            self.bar.on_window_change()

    def keyPressEvent(self, a0: QKeyEvent):
        '''
        键盘监听事件
        '''
        if a0.key() == Qt.Key_Escape:
            a0.ignore()
        else:
            a0.accept()

    def eventFilter(self, target, event):
        if self.bar and isinstance(event, QWindowStateChangeEvent):
            if self.isVisible() and not self.isMinimized() and bool(self.windowFlags() & Qt.WindowMinMaxButtonsHint):
                # 如果当前是最大化则隐藏最大化按钮
                maximized = self.isMaximized()
                self.bar.showMaximizeButton(not maximized)
                self.bar.showNormalButton(maximized)
                # 修复最大化边距空白问题
                if maximized:
                    self._oldMargins = self._main_layout.getContentsMargins()
                    self._main_layout.setContentsMargins(0, 0, 0, 0)
                else:
                    if hasattr(self, '_oldMargins'):
                        self._main_layout.setContentsMargins(*self._oldMargins)
        return super(BaseActivity, self).eventFilter(target, event)


    def paintEvent(self, event):
        '''
        由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小
        '''
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.margin))
        painter.drawRect(self.rect())
