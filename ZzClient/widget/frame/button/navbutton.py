from PyQt5.QtCore import QSize, Qt, QRect, QPoint, QEvent
from PyQt5.QtGui import QColor, QPixmap, QPainter, QBrush, QPen, QPolygon
from PyQt5.QtWidgets import QWidget, QPushButton
from qtpy import QtCore

TextAlign_Left = 0x0001     # 左侧对齐
TextAlign_Right = 0x0002    # 右侧对齐
TextAlign_Top = 0x0020      # 顶部对齐
TextAlign_Bottom = 0x0040   # 底部对齐
TextAlign_Center = 0x0004   # 居中对齐
TrianglePosition_Left = 0   # 左侧
TrianglePosition_Right = 1  # 右侧
TrianglePosition_Top = 2    # 顶部
TrianglePosition_Bottom = 3 # 底部
IconPosition_Left = 0       # 左侧
IconPosition_Right = 1      # 右侧
IconPosition_Top = 2        # 顶部
IconPosition_Bottom = 3     # 底部
LinePosition_Left = 0       # 左侧
LinePosition_Right = 1      # 右侧
LinePosition_Top = 2        # 顶部
LinePosition_Bottom = 3     # 底部

'''
导航按钮
'''

class NavButton(QPushButton):
    paddingLeft = 20
    paddingRight = 5
    paddingTop = 5
    paddingBottom = 5
    textAlign = TextAlign_Left

    showTriangle = False
    triangleLen = 5
    trianglePosition = TrianglePosition_Right
    triangleColor = QColor(255, 255, 255)

    showIcon = False
    iconSpace = 10
    iconSize = QSize(16, 16)

    iconPaddingLeft = 0                # 图标左侧间隔 相对于文字
    iconPaddingRight = 20              # 图标右侧间隔 相对于右边距
    iconPaddingTop = 0                 # 图标顶部间隔 相对于顶部
    iconPaddingBottom = 0              # 图标底部间隔
    iconPosition = IconPosition_Left

    showLine = False
    lineSpace = 0
    lineWidth = 5
    linePosition = LinePosition_Left
    lineColor = QColor(0, 187, 158)

    normalBgColor = QColor(230, 230, 230)
    hoverBgColor = QColor(130, 130, 130)
    checkBgColor = QColor(80, 80, 80)
    normalTextColor = QColor(100, 100, 100)
    hoverTextColor = QColor(255, 255, 255)
    checkTextColor = QColor(255, 255, 255)

    normalBgBrush = Qt.NoBrush
    hoverBgBrush = Qt.NoBrush
    checkBgBrush = Qt.NoBrush

    text = ""

    hover = False

    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)

        self.iconNormal = QPixmap()
        self.iconHover = QPixmap()
        self.iconCheck = QPixmap()

        self.setCheckable(True)

    def enterEvent(self, event):
        self.hover = True
        self.update()

    def leaveEvent(self, event):
        self.hover = False
        self.update()

    def paintEvent(self, event):
        QPushButton.paintEvent(self, event)
        # 绘制准备工作,启用反锯齿
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        # 绘制背景
        self.drawBg(painter)
        # 绘制文字
        self.drawText(painter)
        # 绘制图标
        self.drawIcon(painter)
        # 绘制边框线条
        self.drawLine(painter)
        # 绘制倒三角
        self.drawTriangle(painter)

    def drawBg(self, painter):
        painter.save()
        painter.setPen(Qt.NoPen)

        width = self.width()
        height = self.height()

        bgRect: QRect = None
        if self.linePosition == LinePosition_Left:
             bgRect = QRect(self.lineSpace, 0, width - self.lineSpace, height)
        elif self.linePosition == LinePosition_Right:
            bgRect = QRect(0, 0, width - self.lineSpace, height)
        elif self.linePosition == LinePosition_Top:
            bgRect = QRect(0, self.lineSpace, width, height - self.lineSpace)
        elif self.linePosition == LinePosition_Bottom:
            bgRect = QRect(0, 0, width, height - self.lineSpace)

        # 如果画刷存在则取画刷
        bgBrush: QBrush = None
        if self.isChecked():
            bgBrush = self.checkBgBrush
        elif self.hover:
            bgBrush = self.hoverBgBrush
        else:
            bgBrush = self.normalBgBrush

        if bgBrush != Qt.NoBrush:
            painter.setBrush(bgBrush)
        else:
            # 根据当前状态选择对应颜色
            bgColor: QColor = None
            if self.isChecked():
                bgColor = self.checkBgColor
            elif self.hover:
                bgColor = self.hoverBgColor
            else:
                bgColor = self.normalBgColor

            painter.setBrush(bgColor)

        painter.drawRect(bgRect)
        painter.restore()

    def drawText(self, painter):
        painter.save()
        painter.setBrush(Qt.NoBrush)

        # 根据当前状态选择对应颜色
        textColor: QColor = None
        if self.isChecked():
            textColor = self.checkTextColor
        elif self.hover:
            textColor = self.hoverTextColor
        else:
            textColor = self.normalTextColor

        textRect: QRect
        if IconPosition_Top == self.iconPosition:
            #（左边距 + 图标左边距，顶边距 + 图标顶边距 + 图标高度，按钮宽 - 左边距 - 图标左边距 - 右边距 - 图标右边距，按钮高 - 文字顶边距 - 图标顶边距 - 图标高 - 图标底边距）
            # textRect = QRect(self.paddingLeft + self.iconPaddingLeft, self.paddingTop + self.iconPaddingTop + self.iconSize.height(), width() - self.paddingLeft - self.iconPaddingLeft - self.paddingRight - self.iconPaddingRight, height() - self.paddingTop - self.iconPaddingTop - self.iconSize.height() - self.paddingBottom)
             textRect = QRect(0, self.paddingTop + self.iconPaddingTop + self.iconSize.height(), self.width(), self.height() - self.paddingTop - self.iconPaddingTop - self.iconSize.height() - self.paddingBottom)
        elif IconPosition_Right == self.iconPosition:
            #（左边距，顶边距，按钮宽 - 右边距 - 图标右边距 - 图标宽 ，按钮高 - 文字顶边距 - 文字底边距）
            textRect = QRect(self.paddingLeft, self.paddingTop, self.width() - self.paddingLeft - self.paddingRight - self.iconPaddingRight - self.iconSize.width(), self.height() - self.paddingTop - self.paddingBottom)
        elif IconPosition_Bottom == self.iconPosition:
            #（左边距 + 图标左边距，顶边距 + 图标顶边距 ，按钮宽 - 左边距 - 图标左边距 - 右边距 - 图标右边距，按钮高 - 文字顶边距 - 图标顶边距 - 图标高 - 图标底边距）
            # textRect = QRect(self.paddingLeft + self.iconPaddingLeft, self.paddingTop + self.iconPaddingTop, self.width() - self.paddingLeft - self.iconPaddingLeft - self.paddingRight - self.iconPaddingRight, self.height() - self.paddingTop - self.iconPaddingTop - self.iconSize.height() - self.paddingBottom)
            textRect = QRect(0, self.paddingTop + self.iconPaddingTop, self.width(), self.height() - self.paddingTop - self.iconPaddingTop - self.iconSize.height() - self.paddingBottom)
        if IconPosition_Left == self.iconPosition:
            textRect = QRect(self.paddingLeft + self.iconPaddingLeft + self.iconSize.width(), self.paddingTop, self.width() - self.paddingLeft - self.paddingRight, self.height() - self.paddingTop - self.paddingBottom)

        painter.setPen(textColor)

        if TextAlign_Top == self.textAlign or TextAlign_Bottom == self.textAlign:
            painter.drawText(textRect, self.textAlign | Qt.AlignHCenter, self.text)
        else:
            painter.drawText(textRect, self.textAlign | Qt.AlignVCenter, self.text)

        painter.restore()

    def drawIcon(self, painter):
        if not self.showIcon:
            return
        painter.save()

        pix: QPixmap
        if self.isChecked():
            pix = self.iconCheck
        elif self.hover:
            pix = self.iconHover
        else:
            pix = self.iconNormal

        if not pix.isNull():
            # 等比例平滑缩放图标
            pix = pix.scaled(self.iconSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if IconPosition_Top == self.iconPosition:
                painter.drawPixmap((self.width() - self.iconSize.width())/2, self.iconPaddingTop + self.paddingTop, pix)
            elif IconPosition_Right == self.iconPosition:
                # 按钮宽 - 图标右边距 - 图标宽度 > 垂直居中
                painter.drawPixmap((self.width() - self.iconPaddingRight - self.iconSize.width()), (self.height() - self.iconSize.height())/2, pix)
            elif IconPosition_Bottom == self.iconPosition:
                painter.drawPixmap((self.width() - self.iconSize.width())/2, (self.height() - self.iconSize.height() - self.iconPaddingBottom - self.paddingBottom), pix)
            if IconPosition_Left == self.iconPosition:
                # 图标左边距 + 文字左边距  垂直居中
                painter.drawPixmap(self.iconPaddingLeft + self.paddingLeft, (self.height() - self.iconSize.height())/2, pix)

        painter.restore()

    def drawLine(self, painter):
        if not self.showLine or not self.isChecked():
            return
        painter.save()

        pen = QPen()
        pen.setWidth(self.lineWidth)
        pen.setColor(self.lineColor)
        painter.setPen(pen)

        # 根据线条位置设置线条坐标
        pointStart: QPoint
        pointEnd: QPoint
        if self.linePosition == LinePosition_Left:
            pointStart = QPoint(0, 0)
            pointEnd = QPoint(0, self.height())
        elif self.linePosition == LinePosition_Right:
            pointStart = QPoint(self.width(), 0)
            pointEnd = QPoint(self.width(), self.height())
        elif self.linePosition == LinePosition_Top:
            pointStart = QPoint(0, 0)
            pointEnd = QPoint(self.width(), 0)
        elif self.linePosition == LinePosition_Bottom:
            pointStart = QPoint(0, self.height())
            pointEnd = QPoint(self.width(), self.height())

        painter.drawLine(pointStart, pointEnd)

        painter.restore()

    def drawTriangle(self, painter):
        if not self.showTriangle:
            return

        # 选中或者悬停显示
        if not self.hover or not self.isChecked():
            return

        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.triangleColor)

        # 绘制在右侧中间,根据设定的倒三角的边长设定三个点位置
        width = self.width()
        height = self.height()
        midWidth = width/2
        midHeight = height/2

        pts: QPolygon
        if self.trianglePosition == TrianglePosition_Left:
            pts.setPoints(3, self.triangleLen, midHeight, 0, midHeight - self.triangleLen, 0, midHeight + self.triangleLen)
        elif self.trianglePosition == TrianglePosition_Right:
            pts.setPoints(3, width - self.triangleLen, midHeight, width, midHeight - self.triangleLen, width, midHeight + self.triangleLen)
        elif self.trianglePosition == TrianglePosition_Top:
            pts.setPoints(3, midWidth, self.triangleLen, midWidth - self.triangleLen, 0, midWidth + self.triangleLen, 0)
        elif self.trianglePosition == TrianglePosition_Bottom:
            pts.setPoints(3, midWidth, height - self.triangleLen, midWidth - self.triangleLen, height, midWidth + self.triangleLen, height)

        painter.drawPolygon(pts)

        painter.restore()

    def setPaddingLeft(self, paddingLeft):
        if (self.paddingLeft != paddingLeft):
            self.paddingLeft = paddingLeft
            self.update()

    def setPaddingRight(self, paddingRight):
        if (self.paddingRight != paddingRight):
            self.paddingRight = paddingRight
            self.update()

    def setPaddingTop(self, paddingTop):
        if (self.paddingTop != paddingTop):
            self.paddingTop = paddingTop
            self.update()

    def setPaddingBottom(self, paddingBottom):
        if (self.paddingBottom != paddingBottom):
            self.paddingBottom = paddingBottom
            self.update()

    def setPadding(self, padding):
        self.setPadding(padding, padding, padding, padding)

    def setPadding(self, paddingLeft, paddingRight, paddingTop, paddingBottom):
        self.paddingLeft = paddingLeft
        self.paddingRight = paddingRight
        self.paddingTop = paddingTop
        self.paddingBottom = paddingBottom
        self.update()

    def setIconLeftPadding(self, paddingLeft):
        if(self.iconPaddingLeft != paddingLeft):
            self.iconPaddingLeft = paddingLeft
            self.update()

    def setIconRightPadding(self, paddingRight):
        if(self.iconPaddingRight != paddingRight):
            self.iconPaddingRight = paddingRight
            self.update()

    def setIconTopPadding(self, paddingTop):
        if(self.iconPaddingTop != paddingTop):
            self.iconPaddingTop = paddingTop
            self.update()

    def setIconBottomPadding(self, paddingBottom):
        if(self.iconPaddingBottom != paddingBottom):
            self.iconPaddingBottom = paddingBottom
            self.update()

    def setIconPadding(self, padding):
        self.iconSpace = padding

        self.setPadding(self.iconSpace, self.iconSpace, self.iconSpace, self.iconSpace)

    def setIconPadding(self, paddingLeft, paddingRight, paddingTop, paddingBottom):
        self.iconPaddingLeft = paddingLeft
        self.iconPaddingRight = paddingRight
        self.iconPaddingTop = paddingTop
        self.iconPaddingBottom = paddingBottom
        self.update()

    def setTextAlign(self, textAlign):
        if (self.textAlign != textAlign):
            self.textAlign = textAlign
            self.update()

    def setShowTriangle(self, showTriangle):
        if (self.showTriangle != showTriangle):
            self.showTriangle = showTriangle
            self.update()

    def setTriangleLen(self, triangleLen):
        if (self.triangleLen != triangleLen):
            self.triangleLen = triangleLen
            self.update()

    def setTrianglePosition(self, trianglePosition):
        if (self.trianglePosition != trianglePosition):
            self.trianglePosition = trianglePosition
            self.update()

    def setTriangleColor(self, triangleColor):
        if (self.triangleColor != triangleColor):
            self.triangleColor = triangleColor
            self.update()

    def setShowIcon(self, showIcon):
        if (self.showIcon != showIcon):
            self.showIcon = showIcon
            self.update()

    def setIconSpace(self, iconSpace):
        if (self.iconSpace != iconSpace):
            self.iconSpace = iconSpace
            self.update()

    def setIconSize(self, iconSize):
        if (self.iconSize != iconSize):
            self.iconSize = iconSize
            self.update()

    def setIconNormal(self, iconNormal):
        self.iconNormal = iconNormal
        self.update()

    def setIconHover(self, iconHover):
        self.iconHover = iconHover
        self.update()

    def setIconCheck(self, iconCheck):
        self.iconCheck = iconCheck
        self.update()

    def setIconPosition(self, iconPos):
        self.iconPosition = iconPos
        self.update()

    def setShowLine(self, showLine):
        if (self.showLine != showLine):
            self.showLine = showLine
            self.update()

    def setLineSpace(self, lineSpace):
        if (self.lineSpace != lineSpace):
            self.lineSpace = lineSpace
            self.update()

    def setLineWidth(self, lineWidth):
        if (self.lineWidth != lineWidth):
            self.lineWidth = lineWidth
            self.update()

    def setLinePosition(self, linePosition):
        if (self.linePosition != linePosition):
            self.linePosition = linePosition
            self.update()

    def setLineColor(self, lineColor):
        if (self.lineColor != lineColor):
            self.lineColor = lineColor
            self.update()

    def setNormalBgColor(self, normalBgColor):
        if (self.normalBgColor != normalBgColor):
            self.normalBgColor = normalBgColor
            self.update()

    def setHoverBgColor(self, hoverBgColor):
        if (self.hoverBgColor != hoverBgColor):
            self.hoverBgColor = hoverBgColor
            self.update()

    def setCheckBgColor(self, checkBgColor):
        if (self.checkBgColor != checkBgColor):
            self.checkBgColor = checkBgColor
            self.update()

    def setNormalTextColor(self, normalTextColor):
        if (self.normalTextColor != normalTextColor):
            self.normalTextColor = normalTextColor
            self.update()

    def setHoverTextColor(self, hoverTextColor):
        if (self.hoverTextColor != hoverTextColor):
            self.hoverTextColor = hoverTextColor
            self.update()

    def setCheckTextColor(self, checkTextColor):
        if (self.checkTextColor != checkTextColor):
            self.checkTextColor = checkTextColor
            self.update()

    def setNormalBgBrush(self, normalBgBrush):
        if (self.normalBgBrush != normalBgBrush):
            self.normalBgBrush = normalBgBrush
            self.update()

    def setHoverBgBrush(self, hoverBgBrush):
        if (self.hoverBgBrush != hoverBgBrush):
            self.hoverBgBrush = hoverBgBrush
            self.update()

    def setCheckBgBrush(self, checkBgBrush):
        if (self.checkBgBrush != checkBgBrush):
            self.checkBgBrush = checkBgBrush
            self.update()

    def setShowText(self, text):
        if (self.text != text):
            self.text = text
            self.update()

