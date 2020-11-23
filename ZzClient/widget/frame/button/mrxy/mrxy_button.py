import math
from PyQt5.QtCore import QPoint, QTimer, QSize, Qt, QEvent, QPropertyAnimation, pyqtSignal, QRect, QDateTime, QRectF
from PyQt5.QtGui import QMouseEvent, QColor, QPixmap, QFontMetrics, QFont, QIcon, QCursor, QPainter, QPen, QPainterPath, \
    QBrush
from PyQt5.QtWidgets import QPushButton, QApplication

PI = 3.1415926
GOLDEN_RATIO = 0.618

DOUBLE_PRESS_INTERVAL = 500 # /* 300 */松开和按下的间隔。相等为双击
SINGLE_PRESS_INTERVAL = 200 # /* 150 */按下时间超过这个数就是单击。相等为单击

'''
前景额外的图标（可以多个）
可能是角标（比如展开箭头）
可能时前缀（图例）
'''
class PaintAddin:
    size: QSize
    enable: bool
    pixmap: QPixmap
    align: Qt.Alignment

    def __init__(self, pixmap: QPixmap, align: Qt.Alignment, size: QSize, enable=False):
        self.enable = enable
        self.pixmap = pixmap
        self.align = align
        self.size = size

'''
鼠标松开时抖动动画
松开的时候计算每一次抖动距离+时间，放入队列中
定时调整抖动的队列实体索引
'''
class Jitter:
    point: QPoint # 要运动到的目标坐标
    timestamp: int # 运动到目标坐标应该的时间戳，结束后删除本次抖动路径对象

    def __init__(self, point: QPoint, timestamp: int):
        self.point = point
        self.timestamp = timestamp

'''
鼠标按下/弹起水波纹动画
鼠标按下时动画速度慢（压住），松开后动画速度骤然加快
同样用队列记录所有的水波纹动画实体
'''
class Water:
    point: QPoint
    progress: int #水波纹进度100%（已弃用，当前使用时间戳）
    press_timestamp: int # 鼠标按下时间戳
    release_timestamp: int # 鼠标松开时间戳。与按下时间戳、现行时间戳一起成为水波纹进度计算参数
    finish_timestamp: int # 结束时间戳。与当前时间戳相减则为渐变消失经过的时间戳
    finished: bool # 是否结束。结束后改为渐变消失

    def __init__(self, point: QPoint, press_timestamp: int):
        self.point = point
        self.progress = 0
        self.press_timestamp = press_timestamp
        self.release_timestamp = 0
        self.finished = 0
        self.finished = False

'''
四周边界的padding
调整按钮大小时：宽度+左右、高度+上下
'''
class EdgeVal:
    left: int
    top: int
    left: int
    bottom: int

    def __init__(self, l, t, r, b):
        self.left = l
        self.top = t
        self.right = r
        self.bottom = b

'''
前景实体
'''
class PaintModel:
    Null = 0        # 无前景，仅使用背景
    Text = 1        # 纯文字（替代父类）
    Icon = 2        # 纯图标
    PixmapMask = 3  # 可变色图标（通过pixmap+遮罩实现），锯齿化明显
    IconText = 4    # 图标+文字（强制左对齐）
    PixmapText = 5  # 变色图标+文字（强制左对齐）

class NolinearType:
    Linear = 0
    SlowFaster = 1
    FastSlower = 2
    SlowFastSlower = 3
    SpringBack20 = 4
    SpringBack50 = 5

'''
带交互的按钮
https://github.com/MRXY001/Qt-InteractiveButtons
    - 所有颜色自定义
    - 鼠标悬浮渐变
    - 两种点击效果：鼠标点击渐变 / 水波纹动画（可多层波纹叠加）
    - 额外鼠标移入/移出/按下/弹起的实时/延迟共8种事件
    - 鼠标悬浮图标位置主动变化
    - 鼠标拖动图标抖动反弹效果
    - 鼠标进入父控件时开启出现效果，或启动时出现
    - 延迟出现的动画效果（多个按钮连续）
    - 记录开关状态
    - 直接设置 x、y 的圆角显示
    - 边框颜色设置
    - 禁用时半透明+点击穿透效果
    - 添加额外的边缘角标
    - 三种前景模式：图标、文字、带遮罩的图标（任意变色）
    - 支持QSS直接设置部分属性
    - 与父类 QPushButton 兼容
    - 时间准确性：根据时间戳计算动画进度，即使在低性能机器上也可准时完成动画
    - 稳定性：一按钮多功能，完美兼容多种情况下焦点事件
    - 极其强大的可扩展性，继承该按钮后可任意修改显示效果和动画效果
'''

class MrxyButton(QPushButton):
    '''
    信号量
    '''
    showAniFinished = pyqtSignal()
    hideAniFinished = pyqtSignal()
    pressAppearAniFinished = pyqtSignal()
    pressDisappearAniFinished = pyqtSignal()
    jitterAniFinished = pyqtSignal()
    doubleClicked = pyqtSignal()
    rightClicked = pyqtSignal()
    signalFocusIn = pyqtSignal()
    signalFocusOut = pyqtSignal()
    signalMouseEnter = pyqtSignal()
    signalMouseEnterLater = pyqtSignal() # 进入后延迟信号（以渐变动画完成为准，相当于可手动设置）
    signalMouseLeave = pyqtSignal()
    signalMouseLeaveLater = pyqtSignal() # 离开后延迟的信号（直至渐变动画完成（要是划过一下子离开，这个也会变快））
    signalMousePress = pyqtSignal(QMouseEvent)
    signalMousePressLater = pyqtSignal(QMouseEvent)
    signalMouseRelease = pyqtSignal(QMouseEvent)
    signalMouseReleaseLater = pyqtSignal(QMouseEvent)

    def __init__(self, *args, **kwargs):
        super(MrxyButton, self).__init__(*args, **kwargs)

        '''
        整体开关
        '''
        self.self_enabled = True # 是否启用子类
        self.parent_enabled = False # 是否启用父类
        self.fore_enabled = True # 是否绘制前景
        '''
        前景动画
        '''
        self.show_animation = False # 开启前景动画
        self.show_foreground = True # 显示前景扳机
        self.show_ani_appearing = False # 前景出现扳机
        self.show_ani_disappearing = False # 前景消失扳机
        self.show_duration = 300 # 前景动画延时
        self.show_timestamp = 0 # 前景动画时间戳
        self.hide_timestamp = 0 # 前景动画隐藏时间戳
        self.show_ani_progress = 0 # 前景动画进度
        self.show_ani_point = QPoint(0, 0) # 前景动画点位
        self.paint_rect:QRect = None
        '''
        鼠标开始悬浮、按下、松开、离开的坐标和时间戳
        鼠标锚点、目标锚点、当前锚点的坐标；当前XY的偏移量
        '''
        self.enter_pos = QPoint(-1, -1)
        self.press_pos = QPoint(-1, -1)
        self.release_pos = QPoint(-1, -1)
        self.mouse_pos = QPoint(-1, -1)
        self.anchor_pos = QPoint(-1, -1) # 目标锚点渐渐靠近鼠标
        self.offset_pos = QPoint(0, 0) # 当前偏移量
        self.effect_pos = QPoint(-1, -1) # 相对中心、相对左上角、弹起时的平方根偏移
        self.release_offset = QPoint(0, 0) # 相对中心、相对左上角、弹起时的平方根偏移
        self.hovering = False # 是否悬浮的状态机
        self.pressing = False # 是否按下的状态机
        self.hover_timestamp = 0 # 各种事件的时间戳
        self.leave_timestamp = 0 # 各种事件的时间戳
        self.press_timestamp = 0 # 各种事件的时间戳
        self.release_timestamp = 0 # 各种事件的时间戳
        self.hover_bg_duration = 300 # 各种动画时长
        self.press_bg_duration = 300 # 各种动画时长
        self.click_ani_duration = 300 # 各种动画时长
        '''
        定时刷新界面（保证动画持续）
        '''
        self.anchor_timer:QTimer = None
        self.move_speed = 5
        '''
        背景与前景
        '''
        self.icon_color = QColor(0, 0, 0) # 前景颜色
        self.text_color = QColor(0, 0, 0) # 前景颜色
        self.normal_bg = QColor(0xF2, 0XF2, 0xF2, 0) # 各种背景颜色
        self.checked_bg = QColor(128, 128, 128, 128) # 各种背景颜色
        self.checked_gradient_func = None # 各种背景颜色
        self.hover_bg = QColor(128, 128, 128, 32) # 各种背景颜色
        self.press_bg = QColor(128, 128, 128, 64) # 各种背景颜色
        self.border_bg = QColor(0, 0, 0, 0) # 各种背景颜色
        self.focus_bg = QColor(0, 0, 0, 0) # 有焦点的颜色
        self.focus_border = QColor(0, 0, 0, 0) # 有焦点的颜色
        self.hover_speed = 5 # 颜色渐变速度
        self.press_start = 40 # 颜色渐变速度
        self.press_speed = 5 # 颜色渐变速度
        self.hover_progress = 0 # 颜色渐变进度
        self.press_progress = 0 # 颜色渐变进度
        self.icon_padding_proper = 0.25 # 图标的大小比例
        self.icon_text_padding = 4 # 图标+文字模式共存时，两者间隔、图标大小
        self.icon_text_size = 16 # 图标+文字模式共存时，两者间隔、图标大小
        self.border_width = 1
        self.radius_x = 0
        self.radius_y = 0
        self.font_size = 0
        self.fixed_fore_pos = False # 鼠标进入时是否固定文字位置
        self.fixed_fore_size = False #  鼠标进入/点击时是否固定前景大小
        self.text_dynamic_size = False # 设置字体时自动调整最小宽高
        self.auto_text_color = True # 动画时是否自动调整文字颜色
        self.focusing = False # 是否获得了焦点
        '''
        鼠标单击动画
        '''
        self.click_ani_appearing = False # 是否正在按下的动画效果中
        self.click_ani_disappearing = False # 是否正在按下的动画效果中
        self.click_ani_progress = 0 # 按下的进度（使用时间差计算）
        self.mouse_press_event:QMouseEvent = None
        self.mouse_release_event:QMouseEvent = None
        '''
        统一绘制图标的区域（从整个按钮变为中心三分之二，并且根据偏移计算）
        '''
        self.unified_geometry = False # 上面用不到的话，这个也用不到……
        self._l = 0
        self._t = 0
        self._w = 0
        self._h = 0
        '''
        鼠标拖拽弹起来回抖动效果
        '''
        self.jitter_animation = True  # 是否开启鼠标松开时的抖动效果
        self.elastic_coefficient = 1.2 # 弹性系数
        self.jitters:list = []
        self.jitter_duration = 300 # 抖动一次，多次效果叠加
        '''
        鼠标按下水波纹动画效果
        '''
        self.water_animation = True # 是否开启水波纹动画
        self.waters:list = []
        self.water_press_duration = 800
        self.water_release_duration = 400
        self.water_finish_duration = 300
        self.water_radius:int = 0
        '''
        其他效果
        '''
        self.align = Qt.AlignCenter # 文字/图标对齐方向
        self._state = False # 一个记录状态的变量，比如是否持续
        self.leave_after_clicked = False # 鼠标单击松开后取消悬浮效果（针对菜单、弹窗），按钮必定失去焦点
        self._block_hover = False # 如果有出现动画，临时屏蔽hovering效果
        '''
        双击
        '''
        self.double_clicked = False # 开启双击
        self.double_time:QTimer = None # 双击时钟
        self.double_prevent = False # 双击阻止单击release的flag

        # 属性初始化
        self.paint_addin = PaintAddin(pixmap=None, align=None, size=None, enable=False)
        self.icon = None
        self.text = None
        self.pixmap = None
        self.fore_paddings = EdgeVal(0, 0, 0, 0)

        self.setMouseTracking(True) # 鼠标没有按下时也能捕获移动事件

        self.model = PaintModel.Null

        self.anchor_timer = QTimer(self)
        self.anchor_timer.setInterval(10)
        self.anchor_timer.timeout.connect(self.anchorTimeOut)

        self.clicked.connect(self.slotClicked)

        self.setFocusPolicy(Qt.NoFocus) # 避免一个按钮还获取Tab键焦点

    '''
    文字类型的按钮
    '''
    @classmethod
    def by_text(cls, text, parent):
        instance = cls(parent)
        instance.setText(text)

        return instance

    '''
    图标类型的按钮
    '''
    @classmethod
    def by_icon(cls, icon, parent):
        instance = cls(parent)
        instance.setIcon(icon)

        return instance

    '''
    变色图标类型的按钮
    '''
    @classmethod
    def by_pixmap(cls, pixmap, parent):
        instance = cls(parent)
        instance.setPixmap(pixmap)

        return instance

    '''
    文字图标类型的按钮
    '''
    @classmethod
    def by_icon_with_text(cls, text, icon, parent):
        instance = cls(parent)
        instance.setText(text)
        instance.setIcon(icon)

        return instance

    '''
    文字图标类型的按钮
    '''
    @classmethod
    def by_pixmap_with_text(cls, text, icon, parent):
        instance = cls(parent)
        instance.setText(text)
        instance.setPixmap(icon)

        return instance

    def setText(self, text):
        '''设置按钮文字'''
        self.text = text
        if self.model == PaintModel.Null:
            self.model = PaintModel.Text
        elif self.mode == PaintModel.PixmapMask:
            if self.pixmap.isNull():
                self.model = PaintModel.Text
            else:
                self.model = PaintModel.PixmapText
            self.setAlign(Qt.AlignLeft | Qt.AlignVCenter)
            fm = QFontMetrics(self.font())
            self.icon_text_size = fm.lineSpacing()
        elif self.model == PaintModel.Text:
            if self.icon.isNull():
                self.model = PaintModel.Text
            else:
                self.model = PaintModel.IconText
            self.setAlign(Qt.AlignLeft | Qt.AlignVCenter)
            fm = QFontMetrics(self.font())
            self.icon_text_size = fm.lineSpacing()

        if self.parent_enabled:
            QPushButton.setText(text)

        # 根据字体调整大小
        if self.text_dynamic_size:
            if self.font_size <= 0:
                fm = QFontMetrics(self.font())
                self.setMinimumSize(fm.horizontalAdvance(text)+self.fore_paddings.left+self.fore_paddings.right, fm.lineSpacing()+self.fore_paddings.top+self.fore_paddings.bottom)
            else:
                font = QFont()
                font.setPixelSize(self.font_size)
                fm = QFontMetrics(font)
                self.setMinimumSize(fm.horizontalAdvance(text)+self.fore_paddings.left+self.fore_paddings.right, fm.lineSpacing()+self.fore_paddings.top+self.fore_paddings.bottom)

        self.update()

    def setIconPath(self, path):
        '''设置icon图标'''
        self.setIcon(QIcon(path))

    def setPixmapPath(self, path):
        '''设置pixmap图标'''
        self.setPixmap(QPixmap(path))

    def setIcon(self, icon):
        '''设置icon'''
        if self.model == PaintModel.Null:
            self.model = PaintModel.Icon
        elif self.model == PaintModel.Text:
            if self.text == None or self.text == "":
                self.model = PaintModel.Icon
            else:
                self.model = PaintModel.IconText
            self.setAlign(Qt.AlignLeft | Qt.AlignVCenter)
            fm = QFontMetrics(self.font())
            self.icon_text_size = fm.lineSpacing()
        elif self.model == PaintModel.PixmapMask:
            self.pixmap = QPixmap()
            self.model = PaintModel.Icon
        elif self.model == PaintModel.PixmapText:
            self.pixmap = QPixmap()
            if self.text == '':
                self.model = PaintModel.Icon
            else:
                self.model = PaintModel.IconText
            self.setAlign(Qt.AlignLeft | Qt.AlignVCenter)
            fm = QFontMetrics(self.font())
            self.icon_text_size = fm.lineSpacing()
        self.icon = icon
        if self.parent_enabled:
            super(MrxyButton, self).setIcon(icon)
        self.update()

    def setPixmap(self, pixmap):
        '''设置Pixmap'''
        if self.model == PaintModel.Null:
            self.model = PaintModel.PixmapMask
        elif self.model == PaintModel.Text:
            if self.text == '':
                self.model = PaintModel.PixmapMask
            else:
                self.model = PaintModel.PixmapText
            self.setAlign(Qt.AlignLeft | Qt.AlignVCenter)
            fm = QFontMetrics(self.font())
            self.icon_text_size = fm.lineSpacing()
        elif self.model == PaintModel.Icon:
            self.icon = QIcon()
            self.model = PaintModel.PixmapMask
        elif self.model == PaintModel.IconText:
            self.icon = QIcon()
            if self.text == '':
                self.model = PaintModel.PixmapMask
            else:
                self.model = PaintModel.PixmapText
            self.setAlign(Qt.AlignLeft | Qt.AlignVCenter)
            fm = QFontMetrics(self.font())
            self.icon_text_size = fm.lineSpacing()
        self.pixmap = self.getMaskPixmap(pixmap, self.icon_color if self.isEnabled() else self.getOpacityColor(self.icon_color))
        if self.parent_enabled:
            QPushButton.setIcon(QIcon(pixmap))
        self.update()

    def setPaintAddin(self, pixmap, align, size):
        '''
        设置额外的图标，例如角标
        :param pixmap: 图标
        :param align: 对齐方式
        :param size: 图标尺寸
        '''
        mask = pixmap.mask()
        pixmap.fill(self.icon_color)
        pixmap.setMask(mask)
        self.paint_addin = PaintAddin(pixmap, align, size)
        self.update()

    def setSelfEnabled(self, e):
        '''设置子类功能是否开启，如果关闭，则相当于默认的QPushButton'''
        self.self_enabled = e

    def setParentEnabled(self, e):
        '''设置父类（QPushButton）功能是否开启，如果开启，则绘制父类背景、父类前景'''
        self.parent_enabled = e

        # 传递子类内容到父类去，避免子类关掉后不显示
        if self.model == PaintModel.Text or self.model == PaintModel.IconText or self.model == PaintModel.PixmapText:
            QPushButton.setText(self, self.text)
        if self.model == PaintModel.Icon or self.model == PaintModel.IconText:
            QPushButton.setIcon(self, self.icon)
        if self.model == PaintModel.PixmapMask or self.model == PaintModel.PixmapText:
            QPushButton.setIcon(self, QIcon(self.pixmap))

    def setForeEnabled(self, e):
        '''设置是否绘制前景图标/文字，关闭后则只绘制背景'''
        self.fore_enabled = e

    def setHoverAniDuration(self, d):
        '''
        设置鼠标悬浮背景渐变的动画时长
        :param d: 动画时长（毫秒）
        '''
        self.hover_bg_duration = d
        # hover_progress = 0 # 重置hover效果

    def setPressAniDuration(self, d):
        '''
        设置鼠标按下渐变效果的动画时长
        :param d: 动画时长（毫秒）
        '''
        self.press_bg_duration = d

    def setClickAniDuration(self, d):
        '''
        设置单击效果的动画时长
        :param d:
        '''
        self.click_ani_duration = d

    def setWaterAniDuration(self, press, release, finish):
        '''
        设置水波纹动画时长
        :param press: 按住时时长（时长毫秒）
        :param release: 松开后速度（时长毫秒）
        :param finish: 渐变消失速度（时长毫秒）
        '''
        self.water_press_duration = press
        self.water_release_duration = release
        self.water_finish_duration = finish

    def eventFilter(self, target, event):
        '''各种状态改变，主要是监控 可用 状态，不可用时设置为半透明'''
        if event.type() == QEvent.EnabledChange and self.model == PaintModel.PixmapMask: # 可用状态改变了
            if self.isEnabled(): # 恢复可用：透明度变回去
                color = self.icon_color
                color.setAlpha(color.alpha() * 2)
                self.setIconColor(color)
            else: # 变成不可用：透明度减半
                color = self.icon_color
                color.setAlpha(color.alpha() / 2)
                self.setIconColor(color)

        return super(MrxyButton, self).eventFilter(target, event)

    def setWaterRipple(self, enable):
        '''
        设置水波纹动画是否开启
        关闭时，将使用渐变动画
        :param enable: 开关
        :return:
        '''
        if self.water_animation == enable:
            return
        self.water_animation = enable

    def setJitterAni(self, enable):
        '''设置抖动效果是否开启，鼠标拖拽移动的距离越长，抖动距离越长、次数越多'''
        self.jitter_animation = enable

    def setUnifyGeomerey(self, enable):
        '''设置是否使用统一图标绘制区域，监听图标尺寸大小变化、中心点偏移，计算新的中心坐标位置'''
        self.unified_geometry = enable
        self._l = self._t = 0
        self._w = self.size().width()
        self._h = self.size().height()

    def setBgColor(self, bg):
        '''设置背景颜色'''
        self.setNormalColor(bg)
        self.update()

    def setBgColor2(self, hover, press):
        '''
        设置事件背景颜色
        :param hover: 鼠标悬浮时的背景颜色
        :param press: 鼠标按下时的背景颜色
        '''
        if hover != Qt.black:
            self.setHoverColor(hover)
        if press != Qt.black:
            self.setPressColor(press)
        self.update()

    def setNormalColor(self, color):
        '''设置按钮背景颜色'''
        self.normal_bg = color

    def setBorderColor(self, color):
        '''设置边框线条颜色'''
        self.border_bg = color

    def setHoverColor(self, color):
        '''设置鼠标悬浮时的背景颜色'''
        self.hover_bg = color

    def setPressColor(self, color):
        '''设置鼠标按住时的背景颜色'''
        self.press_bg = color

    def setIconColor(self, color):
        '''设置图标颜色（仅针对可变色的 pixmap 图标）'''
        self.icon_color = color

        # 绘制图标（如果有）
        if self.model == PaintModel.PixmapMask or self.model == PaintModel.PixmapText:
            self.pixmap = self.getMaskPixmap(self.pixmap, self.icon_color if self.isEnabled() else self.getOpacityColor(self.icon_color))

        # 绘制额外角标（如果有的话）
        if self.paint_addin.enable:
            self.paint_addin.pixmap = self.getMaskPixmap(self.paint_addin.pixmap, self.icon_color if self.isEnabled() else self.getOpacityColor(self.icon_color))

        self.update()

    def setTextColor(self, color):
        '''设置前景文字颜色'''
        self.text_color = color
        self.update()

    def setFocusBg(self, color):
        '''设置获取焦点时的背景颜色（默认关闭）'''
        self.setFocusPolicy(Qt.StrongFocus)
        self.focus_bg = color

    def setFocusBorder(self, color):
        '''设置获取焦点时的边框颜色（默认关闭）'''
        self.setFocusPolicy(Qt.StrongFocus)
        self.focus_border = color

    def setFontSize(self, f):
        '''设置文字大小（PointSize，覆盖 font() 字体大小） '''
        if not self.font_size: # 第一次设置字体大小，直接设置
            self.font_size = f
            self.font = QFont(self.font())
            self.font.setPixelSize(f)
            self.setFont(self.font)
            self.update()
        else: # 改变字体大小，使用字体缩放动画
            ani = QPropertyAnimation(self, "font_size")
            ani.setStartValue(self.font_size)
            ani.setEndValue(f)
            ani.setDuration(self.click_ani_duration)
            def animation_finish():
                fm = QFontMetrics(self.font())
                self.icon_text_size = fm.lineSpacing()
                ani.deleteLater()
            ani.finished.connect(animation_finish)
            ani.start()
        # 修改字体大小时调整按钮的最小尺寸，避免文字显示不全
        if self.text_dynamic_size:
            font = QFont()
            font.setPixelSize(f)
            fms = QFontMetrics(font)
            self.setMinimumSize(fms.horizontalAdvance(self.text)+self.fore_paddings.left+self.fore_paddings.right, fms.lineSpacing()+self.fore_paddings.top+self.self.fore_paddings.bottom)
        if self.model != PaintModel.Text:
            fm = QFontMetrics(self.font())
            self.icon_text_size = fm.lineSpacing()

    def getFontSizeT(self):
        '''获取字体大小，用来作为字体动画的属性参数'''
        return self.font_size

    def setFontSizeT(self, f):
        '''设置动画中的临时字体大小，用来作为字体动画的属性参数'''
        self.font_size = f
        font = self.font()
        font.setPixelSize(f)
        self.setFont(font)
        self.update()

    def setHover(self):
        '''如果点击失去焦点的话，即使鼠标移到上面，也不会出现背景，可以用这个方法继续保持悬浮状态'''
        if not self.hovering and self.inArea(self.mapFromGlobal(QCursor.pos())):
            super(MrxyButton, self).enterEvent(QEvent.None_)

    def setAlign(self, a):
        '''设置对齐方式'''
        self.align = a
        self.update()

    def setRadius(self, r):
        '''设置四个角的半径'''
        self.radius_x = self.radius_y = r

    def setRadius2(self, rx, ry):
        '''分开设置 X、Y 的半径'''
        self.radius_x = rx
        self.radius_y = ry

    def setBorderWidth(self, x):
        '''设置边框线条的粗细'''
        self.border_width = x

    def setDisabled(self, dis):
        '''设置不可用情况（默认为假）'''
        if dis != self.isEnabled():
            return

        self.setEnabled(not dis)

        if self.parentWidget() != None:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, dis) # 点击穿透

        if self.model == PaintModel.PixmapMask or self.model == PaintModel.PixmapText:
            self.pixmap = self.getMaskPixmap(self.pixmap, self.getOpacityColor(self.icon_color) if dis else self.icon_color)

        self.update() # 修改透明

    def setPaddings(self, l, r, t, b):
        '''设置前景和四条边的 paddings'''
        self.fore_paddings.left = l
        self.fore_paddings.right = r
        self.fore_paddings.top = t
        self.fore_paddings.bottom = b
        self.setFixedForeSize()

    def setPaddings(self, h, v):
        '''统一设置方向的 paddings'''
        self.fore_paddings.left = self.fore_paddings.right = (h+1) / 2
        self.fore_paddings.top = self.fore_paddings.bottom = (v+1) / 2
        self.setFixedForeSize()

    def setPaddings(self, x):
        '''统一设置前景和四条边的 paddings'''
        self.fore_paddings.left = x
        self.fore_paddings.right = x
        self.fore_paddings.top = x
        self.fore_paddings.bottom = x
        self.setFixedForeSize()

    def setIconPaddingProper(self, x):
        '''设置Icon模式旁边空多少，0~1.0，越大越空'''
        self.icon_padding_proper = x
        short_side = min(self.geometry().width(), self.geometry().height()) # 短边
        # 非固定的情况，尺寸大小变了之后所有 padding 都要变
        padding = short_side*self.icon_padding_proper #static_cast<int>(short_side * (1 - GOLDEN_RATIO) / 2)
        self.fore_paddings.left = self.fore_paddings.top = self.fore_paddings.right = self.fore_paddings.bottom = padding
        self.update()

    def setTextDynamicSize(self, d):
        '''设置字体大小时是否同步修改按钮的最小尺寸（避免按钮显示不全）'''
        self.text_dynamic_size = d

    def setFixedTextPos(self, f):
        self.fixed_fore_pos = f

    def setFixedForePos(self, f):
        '''
        设置前景是否固定，而不移动
        将去除鼠标移入靠近、抖动效果，统一图标区域大小不变
        只包括：鼠标进入/点击，均表现为缩放效果（默认）
        不影响任何其他功能
        '''
        self.fixed_fore_pos = f

    def setFixedForeSize(self, f=True, addin=0):
        '''固定按钮为适当尺寸，并且固定四周留白，前景应为文字/图标对应尺寸的最小尺寸'''
        self.fixed_fore_size = f

        if not f:
            return
        if self.model == PaintModel.Text or self.model == PaintModel.IconText or self.model == PaintModel.PixmapText:
            font = self.font()
            if self.font_size > 0:
                font.setPixelSize(self.font_size)
            fm = QFontMetrics(font)
            self.setMinimumSize(
                fm.horizontalAdvance(self.text)+self.fore_paddings.left+self.fore_paddings.right+addin,
                fm.lineSpacing()+self.fore_paddings.top+self.fore_paddings.bottom+addin
            )
        elif self.model == PaintModel.Icon or self.model == PaintModel.PixmapMask:
            size = self.height()
            self.setMinimumSize(size+addin, size+addin)

    def setSquareSize(self):
        self.setFixedWidth(self.height())
        self.setMinimumWidth(self.height())
        self.setMaximumWidth(self.height())

    def setLeaveAfterClick(self, l):
        '''
        设置鼠标单击松开后是否当做移开
        避免菜单、弹窗出现后，由于鼠标仍然留在按钮上面，导致依旧显示 hover 背景
        '''
        self.leave_after_clicked = l

    def setDoubleClicked(self, e):
        '''
        响应双击事件
        注意：会先触发单击事件、再触发双击事件(其实就是懒得做)
        建议在 QListWidget 等地方使用！
        '''
        self.double_clicked = e

        if not hasattr(self, 'double_timer'):
            self.double_timer = QTimer(self)
            self.double_timer.setInterval(DOUBLE_PRESS_INTERVAL)
            def block():
                self.double_timer.stop()
                self.clicked.emit() # 手动触发单击事件
            self.double_timer.timeout.connect(block)

    def setAutoTextColor(self, a):
        '''动画时是否自动设置文字的颜色'''
        self.self.auto_text_color = a

    def setPretendFocus(self, f):
        '''
        一开始没有聚焦时，假装获取焦点
        通过信号槽使其他控件（例如QLineEdit）按下enter键触发此按钮事件
        直到触发了焦点改变事件，此控件失去焦点（需要手动改变）
        '''
        self.focusing = f
        self.update()

    def setBlockHover(self, b):
        '''
        如果按钮被做成一个组合，在显示的时候开启动画
        一开始鼠标下的按钮一直在hover状态，移开也不会变
        开启后临时屏蔽，记得在动画结束后关闭
        '''
        self._block_hover = b
        if b and self.hovering:
            self.leaveEvent(self, None)

    def setShowAni(self, enable):
        '''是否开启出现动画，鼠标进入按钮区域，前景图标从对面方向缩放出现'''
        self.show_animation = enable

        if not self.show_animation: # 关闭隐藏前景
            self.show_foreground = True
        elif self.show_animation: # 开启隐藏前景
            if not self.hovering and not self.pressing: # 应该是隐藏状态
                self.show_ani_appearing = self.show_ani_disappearing = self.show_foreground = False
                self.show_ani_progress = 0
            else: # 应该是显示状态
                self.show_foreground = True
                self.show_ani_appearing = self.show_ani_disappearing = False
                self.show_ani_progress = 100

    def showForeground(self):
        '''按钮前景出现动画，从中心点出现的缩放动画'''
        if not self.show_animation:
            return
        self.waters.clear()
        if not self.anchor_timer.isActive():
            self.anchor_timer.start()
        if self.show_ani_disappearing:
            self.show_ani_disappearing = False
        self.show_ani_appearing = True
        self.show_timestamp = self.getTimestamp()
        self.show_foreground = True
        self.show_ani_point = QPoint(0,0)

    def showForeground2(self, point=QPoint(0, 0)):
        '''
        按钮前景出现动画2
        指定方向（笛卡尔坐标），从反方向至中心点
        :param point: 最开始出现的方向（大小不影响，只按 x、y 比例来）
        '''
        self.showForeground()
        if point == QPoint(0,0):
            point = self.mapFromGlobal(QCursor.pos()) - QPoint(self.size().width()/2, self.size().height()/2) # 相对于按钮中心
        self.show_ani_point = point

        if self.unified_geometry: # 统一出现动画
            self.updateUnifiedGeometry()

    def hideForeground(self):
        '''隐藏前景为下一次的出现动画做准备'''
        if not self.show_animation:
            return
        if not self.anchor_timer.isActive():
            self.anchor_timer.start()
        if self.show_ani_appearing:
            self.show_ani_appearing = False
        self.show_ani_disappearing = True
        self.hide_timestamp = self.getTimestamp()

    def delayShowed(self, time, point):
        '''
        延迟出现前景，适用于多个按钮连续出现的一套效果
        :param time: 延迟时长（毫秒
        @param point 出现方向）
        '''
        self.setShowAni(True)
        def block():
            self.showForeground2(point)
            def block2():
                self.setShowAni(False)
                self.showAniFinished.disconnect(None)
            self.showAniFinished.connect(block2)
        QTimer.singleShot(time, block)

    def setMenu(self, menu):
        '''设置菜单并解决菜单无法监听到 release 的问题'''
        # 默认设置了不获取焦点事件，所以如果设置了菜单的话，就不会有Release事件，水波纹动画会一直飘荡
        # 在 focusOut 事件中，模拟了 release 事件，
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        QPushButton.setMenu(menu)

    def setState(self, s):
        '''设置状态一个用来作为开关效果的属性'''
        self._state = s
        self.update()

    def simulateStatePress(self, s, a):
        '''
        模拟按下开关的效果，并改变状态
        如果不使用状态，则出现点击动画
        :param s: 目标状态（默认为false）
        :param a:  鼠标在区域内则点击无效（恐怕再次点击）
        '''
        if self._state == s:
            return

        # 鼠标悬浮在上方，有两种情况：
        # 1、点击按钮后触发，重复了
        # 2、需要假装触发，例如 Popup 类型，尽管悬浮在上面，但是无法点击到
        if a and self.inArea(self.mapFromGlobal(QCursor.pos())): # 点击当前按钮，不需要再模拟
            return

        self.mousePressEvent(QMouseEvent(QMouseEvent.None_, QPoint(self.size().width()/2,self.size().height()/2), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

        self.mouseReleaseEvent(QMouseEvent(QMouseEvent.None_, QPoint(self.size().width()/2,self.size().height()/2), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

        # if !inArea(mapFromGlobal(QCursor.pos()))) # 针对模拟release 后面 # 必定成立
        self.hovering = False

    def simulateHover(self):
        '''模拟鼠标悬浮的效果，适用于键盘操作时，模拟鼠标hover状态，用 discardHoverPress 取消状态'''
        if not self.hovering:
            if self._block_hover:
                self.setBlockHover(False) # 可能已经临时屏蔽掉鼠标 enter 事件，强制hover
            self.enterEvent(None)

    def discardHoverPress(self, force):
        '''
        强制丢弃hover、press状态
        适用于悬浮/点击后，弹出模态浮窗
        浮窗关闭后调用此方法
        :param force: 如果鼠标仍在此按钮内，是否强制取消hover/press状态
        '''
        if not force and self.inArea(self.mapFromGlobal(QCursor.pos())): # 鼠标还在这范围内
            return

        if self.hovering:
            self.leaveEvent(None)

        if self.pressing:
            self.mouseReleaseEvent(QMouseEvent(QMouseEvent.None_, QPoint(self.size().width()/2,self.size().height()/2), Qt.LeftButton, Qt.NoButton, Qt.NoModifier))

    def enterEvent(self, event):
        '''鼠标移入事件，触发 hover 时间戳'''
        if self._block_hover: # 临时屏蔽hover事件
            if event:
                event.accept()
            return

        if not self.anchor_timer.isActive():
            self.anchor_timer.start()
        self.hovering = True
        self.hover_timestamp = self.getTimestamp()
        self.leave_timestamp = 0
        if self.mouse_pos == QPoint(-1,-1):
            self.mouse_pos = self.mapFromGlobal(QCursor.pos())
        self.signalMouseEnter.emit()

        return super(MrxyButton, self).enterEvent(event)

    def leaveEvent(self, event):
        '''鼠标移开事件，触发 leave 时间戳'''
        self.hovering = False
        if not self.pressing:
            self.mouse_pos = QPoint(self.geometry().width()/2, self.geometry().height()/2)
        self.signalMouseLeave.emit()

        return super(MrxyButton, self).leaveEvent(event)

    def mousePressEvent(self, event):
        '''鼠标按下事件，触发 press 时间戳，添加水波纹动画 waters 队列'''
        self.mouse_pos = event.pos()

        if event.button() == Qt.LeftButton:
            if not self.hovering:
                super(MrxyButton, self).enterEvent(None)
                # TypeError: enterEvent(self, QEvent): argument 1 has unexpected type 'Type'
                # super(MrxyButton, self).enterEvent(QEvent.None_)

            self.pressing = True
            self.press_pos = self.mouse_pos
            # 判断双击事件
            if self.double_clicked:
                self.last_press_timestamp = self.press_timestamp
                self.press_timestamp = self.getTimestamp()
                if self.release_timestamp+DOUBLE_PRESS_INTERVAL>=self.press_timestamp \
                        and self.last_press_timestamp+SINGLE_PRESS_INTERVAL>self.release_timestamp \
                        and self.release_pos==self.press_pos: # 是双击(判断两次单击的间隔)
                    self.double_prevent = True # 阻止本次的release识别为单击
                    self.press_timestamp = 0   # 避免很可能出现的三击、四击...
                    self.double_timer.stop()  # 取消延迟一小会儿的单击信号
                    self.doubleClicked.emit()
                    return
                else:
                    self.double_prevent = False # 避免有额外的 bug
            else:
                self.press_timestamp = self.getTimestamp()

            if self.water_animation:
                if len(self.waters) > 0 and self.waters[-1].release_timestamp == 0: # 避免两个按键同时下
                    self.waters[-1].release_timestamp = self.getTimestamp()
                self.waters.append(Water(self.press_pos, self.press_timestamp))
            else: # 透明渐变
                if self.press_progress < self.press_start:
                    self.press_progress = self.press_start # 直接设置为按下效果初始值（避免按下反应慢）
        self.mouse_press_event = event
        self.signalMousePress.emit(event)

        return super(MrxyButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        '''鼠标松开事件，触发 release 时间戳，添加抖动动画 jitters 队列'''
        if self.pressing and event.button() == Qt.LeftButton:
            if not self.inArea(event.pos()) or self.leave_after_clicked:
                self.hovering = False
            self.pressing = False
            self.release_pos = event.pos()
            self.release_timestamp = self.getTimestamp()

            # 添加抖动效果
            if self.jitter_animation:
                self.setJitter()

            if self.water_animation and len(self.waters) > 0:
                self.waters[-1].release_timestamp = self.release_timestamp

            if self.double_clicked:
                if self.double_prevent: # 双击的当次release，不参与单击计算
                    self.double_prevent = False
                    return

                # 应该不是双击的操作
                if self.release_pos != self.press_pos or self.release_timestamp - self.press_timestamp >= SINGLE_PRESS_INTERVAL:
                    pass
                else: # 可能是双击，准备
                    self.double_timer.start()
                    return  # 禁止单击事件
        elif self.leave_after_clicked and not self.pressing and self.double_clicked and self.double_prevent: # 双击，失去焦点了，pressing 丢失
            return
        elif event.button() == Qt.RightButton and event.buttons() == Qt.NoButton:
            if (self.release_pos - self.press_pos).manhattanLength() < QApplication.startDragDistance():
                self.rightClicked.emit()
        self.mouse_release_event = event
        self.signalMouseRelease.emit(event)

        return super(MrxyButton, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        '''鼠标移动事件'''
        if self._block_hover: # 临时屏蔽hover事件
            if event:
                event.accept()
            return
        if self.hovering == False: # 失去焦点又回来了
            self.enterEvent(None)
        self.mouse_pos = self.mapFromGlobal(QCursor.pos())

        return super(MrxyButton, self).mouseMoveEvent(event)

    def resizeEvent(self, event):
        '''尺寸大小改变事件，同步调整和尺寸有关的所有属性'''
        if not self.pressing and not self.hovering:
            self.mouse_pos = QPoint(self.geometry().width()/2, self.geometry().height()/2)
            self.anchor_pos = self.mouse_pos
        self.water_radius = int(max(self.geometry().width(), self.geometry().height()) * 1.42) # 长边
        # 非固定的情况，尺寸大小变了之后所有 padding 都要变
        if self.model == PaintModel.Icon or self.model == PaintModel.PixmapMask:
            short_side = min(self.geometry().width(), self.geometry().height()) # 短边
            padding = short_side*self.icon_padding_proper #static_cast<int>(short_side * (1 - GOLDEN_RATIO) / 2)
            self.fore_paddings.left = self.fore_paddings.top = self.fore_paddings.right = self.fore_paddings.bottom = padding
        self._l = _t = 0
        self._w = self.size().width()
        self._h = self.size().height()

        return super(MrxyButton, self).resizeEvent(event)

    def focusInEvent(self, event):
        '''获得焦点事件，已经取消按钮获取焦点，focusIn和focusOut事件都不会触发'''
        if not self.hovering and self.inArea(self.mapFromGlobal(QCursor.pos())):
            super(MrxyButton, self).enterEvent(QEvent.None_)

        self.focusing = True
        self.signalFocusIn.emit()

        return super(MrxyButton, self).focusInEvent(event)

    def focusOutEvent(self, event):
        '''失去焦点事件，兼容按住时突然失去焦点（例如弹出菜单、被其他窗口抢走了）'''
        if self.hovering:
            self.hovering = False
        if self.pressing: # 鼠标一直按住，可能在click事件中移动了焦点
            self.pressing = False
            self.release_pos = self.mapFromGlobal(QCursor.pos())
            self.release_timestamp = self.getTimestamp()

            if self.water_animation and len(self.waters) > 0:
                self.waters[-1].self.release_timestamp = self.release_timestamp

        self.focusing = False
        self.signalFocusOut.emit()

        return super(MrxyButton, self).focusOutEvent(event)

    def paintEvent(self, event):
        '''重绘事件，绘制所有内容：背景、动画、前景、角标'''
        if self.parent_enabled: # 绘制父类（以便使用父类的QSS和各项属性:
            super(MrxyButton, self).paintEvent(event)
        if not self.self_enabled: # 不绘制自己
            return
        painter = QPainter(self)

        # ==== 绘制背景 ====
        path_back = self.getBgPainterPath()
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self.normal_bg.alpha() != 0: # 默认背景
            painter.fillPath(path_back, self.normal_bg if self.isEnabled() else self.getOpacityColor(self.normal_bg))
        if self.focusing and self.focus_bg.alpha() != 0: # 焦点背景
            painter.fillPath(path_back, self.focus_bg)
        if self.isChecked() and self.isEnabled():
            painter.fillPath(path_back, self.checked_gradient_func(self) if self.checked_gradient_func else self.checked_bg)

        if (self.border_bg.alpha() != 0 or (self.focusing and self.focus_border.alpha() != 0)) and self.border_width > 0:
            painter.save()
            pen = QPen()
            pen.setColor(self.focus_border if (self.focusing and self.focus_border.alpha()) else self.border_bg)
            pen.setWidth(self.border_width)
            painter.setPen(pen)
            painter.drawPath(path_back)
            painter.restore()

        if not self.isChecked() and self.hover_progress: # 悬浮背景
            painter.fillPath(path_back, self.getOpacityColor(self.hover_bg, self.hover_progress/100))

        if not self.isCheckable() and self.press_progress and not self.water_animation: # 按下渐变淡化消失
            painter.fillPath(path_back, self.getOpacityColor(self.press_bg, self.press_progress/100.0))
        elif self.water_animation and len(self.waters) > 0: # 水波纹，且至少有一个水波纹
            self.paintWaterRipple(painter)

        # ==== 绘制前景 ====
        if self.fore_enabled and self.show_foreground:
            painter.setPen(self.icon_color if self.isEnabled() else self.getOpacityColor(self.icon_color))

            # 绘制额外内容（可能被前景覆盖）
            if self.paint_addin.enable:
                l = self.fore_paddings.left
                t = self.fore_paddings.top
                r = self.size().width()-self.fore_paddings.right
                b = self.size().height()-self.fore_paddings.bottom
                small_edge = min(self.size().height(), self.size().width())
                pw = self.paint_addin.size.width() if self.paint_addin.size.width() else small_edge-self.fore_paddings.left-self.fore_paddings.right
                ph = self.paint_addin.size.height() if self.paint_addin.size.height() else small_edge-self.fore_paddings.top-self.fore_paddings.bottom
                if self.paint_addin.align & Qt.AlignLeft:
                    r = l + pw
                elif self.paint_addin.align & Qt.AlignRight:
                    l = r - pw
                elif self.paint_addin.align & Qt.AlignHCenter:
                    l = self.size().width()/2-pw/2
                    r = l+pw
                if self.paint_addin.align & Qt.AlignTop:
                    b = t + ph
                elif self.paint_addin.align & Qt.AlignBottom:
                    t = b - ph
                elif self.paint_addin.align & Qt.AlignVCenter:
                    t = self.size().height()/2-ph/2
                    b = t+ph
                painter.drawPixmap(QRect(l,t,r-l,b-t), self.paint_addin.pixmap)

            rect = self.paint_rect
            rect = QRect(self.fore_paddings.left+(0 if self.fixed_fore_pos else self.offset_pos.x()), self.fore_paddings.top+(0 if self.fixed_fore_pos else self.offset_pos.y()), # 原来的位置，不包含点击、出现效果
                       (self.size().width()-self.fore_paddings.left-self.fore_paddings.right),
                       self.size().height()-self.fore_paddings.top-self.fore_paddings.bottom)

            # 抖动出现动画
            if (self.show_ani_appearing or self.show_ani_disappearing) and self.show_ani_point != QPoint( 0, 0 ) and not self.fixed_fore_pos:
                # w = self.size().width()
                # h = self.size().height()
                pro = self.getSpringBackProgress(self.show_ani_progress, 50)

                # show_ani_point 是鼠标进入的点，那么起始方向应该是相反的
                x = self.show_ani_point.x()
                y = self.show_ani_point.y()
                gen = self.quick_sqrt(x*x + y*y)
                x = self.water_radius * x / gen # 动画起始中心点横坐标 反向
                y = self.water_radius * y / gen # 动画起始中心点纵坐标 反向

                rect = QRect(
                    rect.left() - x * (100-pro) / 100 + rect.width() * (100-pro) / 100,
                    rect.top() - y * (100-pro) / 100 + rect.height() * (100-pro) / 100,
                    rect.width() * pro / 100,
                    rect.height() * pro / 100
                    )
            elif self.align == Qt.AlignCenter and self.model != PaintModel.Text and not self.fixed_fore_size: # 默认的缩放动画
                delta_x = 0
                delta_y = 0
                if self.click_ani_progress != 0: # 图标缩放
                    delta_x = rect.width() * self.click_ani_progress / 400
                    delta_y = rect.height() * self.click_ani_progress / 400
                elif self.show_ani_appearing:
                    '''
                    # 将动画进度转换为回弹动画进度
                    int pro 
                    if self.show_ani_progress <= 50:
                        pro = self.show_ani_progress * 2
                    elif self.show_ani_progress <= 75)
                        pro = (self.show_ani_progress-50)/2 + 100
                    else
                        pro = 100 + (100-self.show_ani_progress)/2

                    delta_x = rect.width() * (100-pro) / 100
                    delta_y = rect.height() * (100-pro) / 100
                    '''

                    pro = self.getNolinearProg(self.show_ani_progress, NolinearType.SpringBack50)
                    delta_x = int(rect.width() * (1-pro))
                    delta_y = int(rect.height() * (1-pro))
                elif self.show_ani_disappearing:
                    pro = 1 - self.getNolinearProg(self.show_ani_progress, NolinearType.SlowFaster)
                    delta_x = rect.width() * pro # (100-self.show_ani_progress) / 100
                    delta_y = rect.height() * pro # (100-self.show_ani_progress) / 100
                if delta_x or delta_y:
                    rect = QRect(rect.left()+delta_x, rect.top()+delta_y,
                                rect.width()-delta_x*2, rect.height()-delta_y*2)

            # if self.isEnabled():
            #     color = self.icon_color
            #     color.setAlpha(color.alpha() / 2)
            #     painter.setPen(color)

            if self.model == None:
                # 子类自己的绘制内容
                pass
            elif self.model == PaintModel.Text:
                # 绘制文字教程： https:#blog.csdn.net/temetnosce/article/details/78068464
                painter.setPen(self.text_color if self.isEnabled() else self.getOpacityColor(self.text_color))
                # if self.show_ani_appearing or self.show_ani_disappearing:
                #     pro = self.getSpringBackProgress(self.show_ani_progress, 50)
                #     font = painter.font()
                #     ps = font.pointSize()
                #     ps = ps * self.show_ani_progress / 100
                #     font.setPixelSize()(ps)
                #     painter.setFont(font)
                if self.font_size > 0:
                    font = painter.font()
                    font.setPixelSize(self.font_size)
                    painter.setFont(font)
                painter.drawText(rect, int(self.align), self.text)
            elif self.model == PaintModel.Icon: # 绘制图标
                self.icon.paint(painter, rect, self.align, self.getIconMode())
            elif self.model == PaintModel.PixmapMask:
                painter.setRenderHint(QPainter.SmoothPixmapTransform, True) # 可以让边缘看起来平滑一些
                painter.drawPixmap(rect, self.pixmap)
            elif self.model == PaintModel.IconText or self.model == PaintModel.PixmapText: # 强制左对齐；左图标中文字
                # 绘制图标
                sz = self.icon_text_size
                icon_rect = QRect(rect.left(), rect.top() + rect.height()/2 - sz / 2, sz, sz)
                if not self.fixed_fore_pos:
                    icon_rect.moveTo(icon_rect.left() - self.quick_sqrt(self.offset_pos.x()), icon_rect.top() - self.quick_sqrt(self.offset_pos.y()))
                self.drawIconBeforeText(painter, icon_rect)
                rect.setLeft(rect.left() + sz + self.icon_text_padding)

                # 绘制文字
                # 扩展文字范围，确保文字可见
                painter.setPen(self.text_color if self.isEnabled() else self.getOpacityColor(self.text_color))
                rect.setWidth(rect.width() + sz + self.icon_text_padding)
                if self.font_size > 0:
                    font = painter.font()
                    font.setPixelSize(self.font_size)
                    painter.setFont(font)
                painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, self.text)

        # ==== 绘制鼠标位置 ====
        # painter.drawEllipse(QRect(self.anchor_pos.x()-5, self.anchor_pos.y()-5, 10, 10)) # 移动锚点
        # painter.drawEllipse(QRect(self.effect_pos.x()-2, self.effect_pos.y()-2, 4, 4)) # 影响位置锚点

        # return super(MrxyButton, self).paintEvent(event) # 不绘制父类背景了

    def drawIconBeforeText(self, painter, icon_rect):
        '''IconText/PixmapText模式下，绘制图标，可扩展到绘制图标背景色（模仿menu选中、禁用情况）等'''
        if self.model == PaintModel.IconText:
            self.icon.paint(painter, icon_rect, self.align, self.getIconMode())
        elif self.model == PaintModel.PixmapText:
            painter.drawPixmap(self.icon_rect, self.pixmap)

    def inArea(self, point):
        '''
        判断坐标是否在按钮区域内
        避免失去了焦点，但是依旧需要 hover 效果（非菜单和弹窗抢走焦点）
        为子类异形按钮区域判断提供支持
        '''
        return not (point.x() < 0 or point.y() < 0 or point.x() > self.size().width() or point.y() > self.size().height())

    def getBgPainterPath(self):
        '''
        获取按钮背景的绘制区域
        为子类异形按钮提供支持
        :return:
        '''
        path = QPainterPath()
        if self.radius_x or self.radius_y:
            path.addRoundedRect(QRectF(0,0,self.size().width(),self.size().height()), self.radius_x, self.radius_y)
        else:
            path.addRect(QRectF(0,0,self.size().width(),self.size().height()))
        return path

    def getWaterPainterPath(self, water):
        '''
        获取水波纹绘制区域（圆形，但不规则区域
        圆形水面 & 按钮区域
        :param  water: 一面水波纹动画对象
        '''
        prog = self.getNolinearProg(water.progress, NolinearType.SlowFaster)
        ra = self.water_radius*prog
        circle = QRectF(water.point.x() - ra,
                    water.point.y() - ra,
                    ra*2,
                    ra*2)
        path = QPainterPath()
        path.addEllipse(circle)
        if self.radius_x or self.radius_y:
            return path & self.getBgPainterPath()
        return path

    def getUnifiedGeometry(self):
        '''
        获取统一的尺寸大小（已废弃）
        兼容圆形按钮出现动画，半径使用水波纹（对角线）
        可直接使用 protected 对象
        :return:
        '''
        # 将动画进度转换为回弹动画进度
        pro = self.getSpringBackProgress(self.show_ani_progress,50) if self.show_ani_appearing else self.show_ani_progress
        ul = 0
        ut = 0
        uw = self.size().width()
        uh = self.size().height()

        # self.show_ani_point 是鼠标进入的点，那么起始方向应该是相反的
        x = self.show_ani_point.x()
        y = self.show_ani_point.y()
        gen = self.quick_sqrt(x*x + y*y)
        x = - self.water_radius * x / gen # 动画起始中心点横坐标 反向
        y = - self.water_radius * y / gen # 动画起始中心点纵坐标 反向

        ul = ul + x * (100-pro) / 100 + uw * (100-pro) / 200
        ut = ut + y * (100-pro) / 100 + uh * (100-pro) / 200
        uw = uw * pro / 100
        uh = uh * pro / 100

        return QRect(ul, ut, uw, uh)

    def updateUnifiedGeometry(self):
        '''
        更新统一绘制区域
        内部的 _l, _t, _w, _h 可直接使用
        '''
        self._l = 0
        self._t = 0
        self._w = self.geometry().width()
        self._h = self.geometry().height()
        if (self.show_ani_appearing or self.show_ani_disappearing) and self.show_ani_point != QPoint( 0, 0 ):
            # 将动画进度转换为回弹动画进度
            pro = self.getSpringBackProgress(self.show_ani_progress,50) if self.show_ani_appearing else self.show_ani_progress

            # self.show_ani_point 是鼠标进入的点，那么起始方向应该是相反的
            x = self.show_ani_point.x()
            y = self.show_ani_point.y()
            gen = self.quick_sqrt(x*x + y*y)
            x = - self.water_radius * x / gen # 动画起始中心点横坐标 反向
            y = - self.water_radius * y / gen # 动画起始中心点纵坐标 反向

            self._l = self._l + x * (100-pro) / 100 + self._w * (100-pro) / 200
            self._t = self._t + y * (100-pro) / 100 + self._h * (100-pro) / 200
            self._w = self._w * pro / 100
            self._h = self._h * pro / 100

    def paintWaterRipple(self, painter):
        '''
        绘制一个水波纹动画
        :param painter: 绘制对象（即painter(self)对象）
        '''
        water_finished_color = QColor(self.press_bg)

        for water in self.waters:
            if water.finished: # 渐变消失
                water_finished_color.setAlpha(self.press_bg.alpha() * water.progress / 100)
                path_back = self.getBgPainterPath()
                painter.fillPath(path_back, QBrush(water_finished_color))
            else: # 圆形出现
                path = self.getWaterPainterPath(water)
                painter.fillPath(path, QBrush(self.press_bg))

    def setJitter(self):
        '''
        鼠标松开的时候，计算所有抖动效果的路径和事件
        在每次重绘界面的时候，依次遍历所有的路径
        :return:
        '''
        self.jitters.clear()
        center_pos = self.geometry().center()-self.geometry().topLeft()
        full_manh = (self.anchor_pos-center_pos).manhattanLength() # 距离
        # print((self.geometry().topLeft() - self.geometry().bottomRight()).manhattanLength())
        # 是否达到需要抖动的距离
        if full_manh > (self.geometry().topLeft() - self.geometry().bottomRight()).manhattanLength(): # 距离超过外接圆半径，开启抖动
            jitter_pos = QPoint(self.effect_pos)
            full_manh = (jitter_pos-center_pos).manhattanLength()
            manh = full_manh
            duration = self.jitter_duration
            self.timestamp = self.release_timestamp
            while (manh > self.elastic_coefficient):
                self.jitters.append(Jitter(jitter_pos, self.timestamp))
                jitter_pos = center_pos - (jitter_pos - center_pos) / self.elastic_coefficient
                duration = self.jitter_duration * manh / full_manh
                self.timestamp += duration
                manh = int(manh / self.elastic_coefficient)
            self.jitters.append(Jitter(jitter_pos, self.timestamp))
            self.anchor_pos = self.mouse_pos = center_pos
        elif not self.hovering: # 悬浮的时候依旧有效
            # 未达到抖动距离，直接恢复
            self.mouse_pos = center_pos

    def quick_sqrt(self, x):
        '''开根号'''
        symbol = 1
        if x < 0:
            symbol = -1
            x = -x
        return symbol*math.sqrt(x)

    def getTimestamp(self):
        '''获取现行时间戳，13位，精确到毫秒，返回时间戳'''
        return QDateTime.currentDateTime().toMSecsSinceEpoch()

    def isLightColor(self, color):
        '''
        是否为亮色颜色
        :param color: 颜色
        :return: 是否为亮色
        '''
        return color.red()*0.299 + color.green()*0.578 + color.blue()*0.114 >= 192

    def getSpringBackProgress(self, x, max):
        '''
        获取非线性动画在某一时间比例的动画进度
        仅适用于弹过头效果的动画
        :param x: 实际相对完整100%的动画进度
        :param max: 前半部分动画进度上限
        :return: 应当显示的动画进度
        '''
        if x <= max:
            return x * 100 / max
        if x <= max + (100-max)/2:
            return (x-max)/2+100
        return 100 + (100-x)/2

    def getOpacityColor(self, color, level=1):
        '''
        获取透明的颜色
        :param color: 颜色
        :param level: 比例
        :return: 透明颜色
        '''
        color2 = QColor(color)
        color2.setAlpha(int(color2.alpha() * level))
        return color2

    def getMaskPixmap(self, p, c):
        '''
        获取对应颜色的图标 pixmap
        :param p: 图标
        :param c: 颜色
        :return: 对应颜色的图标
        '''
        mask = p.mask()
        p.fill(c)
        p.setMask(mask)
        return p

    def getNolinearProg(self, p, type):
        if p <= 0:
            return 0.0
        if p >= 100:
            return 1.0

        if type == NolinearType.Linear:
            return p / 100.0
        elif type == NolinearType.SlowFaster:
            return p * p / 10000.0
        elif type == NolinearType.FastSlower:
            return self.quick_sqrt(p*100) / 100.0
        elif type == NolinearType.SlowFastSlower:
            if p <= 50:
                return p * p / 50.0
            else:
                return 0.5 + self.quick_sqrt(50*(p-50))/100.0
        elif type == NolinearType.SpringBack20:
            pass
        elif type == NolinearType.SpringBack50:
            if p <= 50:
                return p / 50.0
            elif p < 75:
                return 1.0 + (p-50) / 200.0
            else:
                return 1.0 + (100-p) / 200.0

    def getIconMode(self):
        return (QIcon.Selected if self.getState() else (QIcon.Active if self.hovering or self.pressing else QIcon.Normal)) if self.isEnabled() else QIcon.Disabled

    def anchorTimeOut(self):
        '''
        锚点变成到鼠标位置的定时时钟
        同步计算所有和时间或者帧数有关的动画和属性
        '''
        self.timestamp = self.getTimestamp()

        if self.pressing: # 鼠标按下
            if self.press_progress < 100: # 透明渐变，且没有完成
                self.press_progress += self.press_speed
                if self.press_progress >= 100:
                    self.press_progress = 100
                    if self.mouse_press_event:
                        self.signalMousePressLater.emit(self.mouse_press_event)
                        self.mouse_press_event = None
            if self.hovering and self.hover_progress < 100:
                self.hover_progress += self.hover_speed
                if self.hover_progress >= 100:
                    self.hover_progress = 100
                    self.signalMouseEnterLater.emit()
        else: # 鼠标悬浮
            if self.press_progress>0: # 如果按下的效果还在，变浅
                self.press_progress -= self.press_speed
                if self.press_progress <= 0:
                    self.press_progress = 0
                    if self.mouse_release_event:
                        self.signalMouseReleaseLater.emit(self.mouse_release_event)
                        self.mouse_release_event = None

            if self.hovering: # 在框内：加深
                if self.hover_progress < 100:
                    self.hover_progress += self.hover_speed
                    if self.hover_progress >= 100:
                        self.hover_progress = 100
                        self.signalMouseEnterLater.emit()
            else: # 在框外：变浅
                if self.hover_progress > 0:
                    self.hover_progress -= self.hover_speed
                    if self.hover_progress <= 0:
                        self.hover_progress = 0
                        self.signalMouseLeaveLater.emit()

        # ==== 按下背景水波纹动画 ====
        if self.water_animation:
            for water in self.waters:
                if water.finished: # 结束状态
                    water.progress = int(100 - 100 * (self.timestamp-water.finish_timestamp) / self.water_finish_duration)
                    if water.progress <= 0:
                        self.waters.remove(water)
                        if self.mouse_release_event: # 还没有发送按下延迟信号
                            self.signalMouseReleaseLater.emit(self.mouse_release_event)
                            self.mouse_release_event = None
                else: # 正在出现状态
                    if water.progress >= 100: # 满了
                        water.progress = 100
                        if water.release_timestamp: # 鼠标已经松开了
                            water.finished = True # 准备结束
                            water.finish_timestamp = self.timestamp
                    else: # 动画中的
                        if water.release_timestamp: # 鼠标已经松开了
                            water.progress = int(100 * (water.release_timestamp - water.press_timestamp) / self.water_press_duration
                                    + 100 * (self.timestamp - water.release_timestamp) / self.water_release_duration)
                        else: # 鼠标一直按下
                            water.progress = int(100 * (self.timestamp - water.press_timestamp) / self.water_press_duration)
                        if water.progress >= 100:
                            water.progress = 100
                            if self.mouse_press_event: # 还没有发送按下延迟信号
                                self.signalMousePressLater.emit(self.mouse_press_event)
                                self.mouse_press_event = None

        # ==== 出现动画 ====
        if self.show_animation:
            if self.show_ani_appearing: # 出现
                delta = self.getTimestamp() - self.show_timestamp
                if self.show_ani_progress >= 100: # 出现结束
                    self.show_ani_appearing = False
                    self.showAniFinished.emit()
                else:
                    self.show_ani_progress = int(100 * delta / self.show_duration)
                    if self.show_ani_progress > 100:
                        self.show_ani_progress = 100
            if self.show_ani_disappearing: # 消失
                delta = self.getTimestamp() - self.hide_timestamp
                if self.show_ani_progress <= 0: # 消失结束
                    self.show_ani_disappearing = False
                    self.show_foreground = False
                    self.show_ani_point = QPoint(0,0)
                    self.hideAniFinished.emit()
                else:
                    self.show_ani_progress = int(100 - 100 * delta / self.show_duration)
                    if self.show_ani_progress < 0:
                        self.show_ani_progress = 0

        # ==== 按下动画 ====
        if self.click_ani_disappearing: # 点击动画效果消失
            delta = self.getTimestamp()-self.release_timestamp-self.click_ani_duration
            if delta <= 0:
                self.click_ani_progress = 100
            else:
                self.click_ani_progress = int(100 - delta*100 / self.click_ani_duration)
            if self.click_ani_progress < 0:
                self.click_ani_progress = 0
                self.click_ani_disappearing = False
                self.pressAppearAniFinished.emit()
        if self.click_ani_appearing: # 点击动画效果
            delta = self.getTimestamp()-self.release_timestamp
            if delta <= 0:
                self.click_ani_progress = 0
            else:
                self.click_ani_progress = int(delta * 100 / self.click_ani_duration)
            if self.click_ani_progress > 100:
                self.click_ani_progress = 100 # 保持100的状态，下次点击时回到0
                self.click_ani_appearing = False
                self.click_ani_disappearing = True
                self.pressDisappearAniFinished.emit()

        # ==== 锚点移动 ====
        if len(self.jitters) > 0: # 松开时的抖动效果
            # 当前应该是处在最后一个点
            cur = self.jitters[0]
            aim = self.jitters[1]
            delay = int(self.getTimestamp()-cur.timestamp)
            dur = int(aim.timestamp - cur.timestamp)
            effect_pos = cur.point + (aim.point-cur.point)*delay/dur
            self.offset_pos = effect_pos- (self.geometry().center() - self.geometry().topLeft())

            if delay >= dur:
                del self.jitters[0]

            # 抖动结束
            if len(self.jitters) == 1:
                self.jitters.clear()
                self.jitterAniFinished.emit()
        elif self.anchor_pos != self.mouse_pos: # 移动效果
            delta_x = self.anchor_pos.x() - self.mouse_pos.x()
            delta_y = self.anchor_pos.y() - self.mouse_pos.y()

            self.anchor_pos.setX( self.anchor_pos.x() - self.quick_sqrt(delta_x) )
            self.anchor_pos.setY( self.anchor_pos.y() - self.quick_sqrt(delta_y) )

            self.offset_pos.setX(self.quick_sqrt(self.anchor_pos.x()-(self.geometry().width()>>1)))
            self.offset_pos.setY(self.quick_sqrt(self.anchor_pos.y()-(self.geometry().height()>>1)))
            self.effect_pos.setX( (self.geometry().width() >>1) + self.offset_pos.x())
            self.effect_pos.setY( (self.geometry().height()>>1) + self.offset_pos.y())
        elif not self.pressing and not self.hovering and not self.hover_progress and not self.press_progress \
                 and not self.click_ani_appearing and not self.click_ani_disappearing and len(self.jitters) == 0 and len(self.waters) == 0 \
                 and not self.show_ani_appearing and not self.show_ani_disappearing: # 没有需要加载的项，暂停（节约资源）
            self.anchor_timer.stop()

        # ==== 统一坐标的出现动画 ====
        if self.unified_geometry:
            self.updateUnifiedGeometry()

        self.update()

    def slotClicked(self):
        '''鼠标单击事件，实测按下后，在按钮区域弹起，不管移动多少距离都算是 clicked'''
        self.click_ani_appearing = True
        self.click_ani_disappearing = False
        self.click_ani_progress = 0
        self.release_offset = self.offset_pos

        self.jitters.clear() # 清除抖动

    def slotCloseState(self):
        '''强行关闭状态，以槽的形式，便与利用'''
        self.setState(False)

    def getState(self):
        '''
        获取状态
        :return: 状态
        '''
        return self._state





