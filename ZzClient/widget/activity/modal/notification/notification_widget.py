import qtawesome
from PyQt5.QtCore import pyqtProperty, Qt, pyqtSignal, QRect, QPoint, QSize
from PyQt5.QtGui import QPainter, QPalette, QBrush, QPen
from PyQt5.QtWidgets import QWidget, QPushButton, QSizePolicy, QVBoxLayout, QLabel, QHBoxLayout

from common.loader.resource import ResourceLoader
from widget.activity.modal.notification.notification_params import NotificationParams


class NotificationWidget(QWidget):
    CloseButtonClicked = pyqtSignal(QWidget)
    DetailsButtonClicked = pyqtSignal(QWidget)
    m_opacity = 1
    __width = 400
    __icon_size = 40

    def __init__(self, *args, params, **kwargs):
        super(NotificationWidget, self).__init__(*args, **kwargs)

        self.params = params

        flags = (Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowFlags(flags)

        self.setAttribute(Qt.WA_TranslucentBackground)  # Indicates that the background will be transparent
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # At the show, widget does not get the focus automatically

        self.InitUI(params)

        self.setFixedWidth(self.__width)

    def OnCloseButtonClicked(self):
        self.CloseButtonClicked.emit(self)

    def OnDetailsButtonClicked(self):
        self.DetailsButtonClicked.emit(self)

    def InitUI(self, params):
        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(10, 0, 0, 0)
        mainLayout.setSpacing(0)

        iconLabel = QLabel()
        if params.type == NotificationParams.INFO or params.type == NotificationParams.HINT:
            iconLabel.setPixmap(qtawesome.icon('mdi.information-variant', color=ResourceLoader().qt_color_text).pixmap(QSize(self.__icon_size, self.__icon_size)))
        if params.type == NotificationParams.WARN:
            iconLabel.setPixmap(qtawesome.icon('mdi.alert-octagon', color=ResourceLoader().qt_color_warning).pixmap(QSize(self.__icon_size, self.__icon_size)))
        if params.type == NotificationParams.ERROR:
            iconLabel.setPixmap(qtawesome.icon('mdi.alert-decagram', color=ResourceLoader().qt_color_warning).pixmap(QSize(self.__icon_size, self.__icon_size)))
        iconLabel.setScaledContents(False)
        mainLayout.addWidget(iconLabel)

        messageLayout = QVBoxLayout()
        messageLayout.setContentsMargins(0, 10, 10, 12)
        messageLayout.setSpacing(4)
        mainLayout.addItem(messageLayout)

        titleLayout = QHBoxLayout()
        messageLayout.addItem(titleLayout)

        if self.params.type != NotificationParams.HINT and self.params.title != '':
            title = self.params.title
            labelTitle = QLabel(title)
            labelTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            labelTitle.setStyleSheet("font-weight: bold;font-size: 13px;")
            titleLayout.addWidget(labelTitle)

        message = self.params.message
        labelMessage = QLabel(message)
        labelMessage.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        labelMessage.setWordWrap(True)
        messageLayout.addWidget(labelMessage)

        palette = QPalette()
        baseColor = palette.color(QPalette.Midlight)
        buttonColor = baseColor
        buttonColor.setAlpha(0)
        pressedColor = baseColor
        pressedColor.setAlpha(255)

        styleSheet = str("QPushButton{border:none;}")

        buttonsLayout = QVBoxLayout()
        buttonsLayout.setContentsMargins(0, 4, 0, 4)
        buttonsLayout.setSpacing(0)
        self.closeButton = QPushButton()
        self.closeButton.setText("关闭")
        self.closeButton.setObjectName("CloseButton")
        self.closeButton.setProperty('type', 1)
        self.closeButton.setStyleSheet(styleSheet)
        self.closeButton.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
        buttonsLayout.addWidget(self.closeButton)
        self.closeButton.clicked.connect(self.OnCloseButtonClicked)

        if self.params.callback:
            self.detailsButton = QPushButton(self.params.detailsButtonText)
            self.detailsButton.setProperty('type', 1)
            self.detailsButton.setObjectName("DetailsButton")
            self.detailsButton.setStyleSheet(styleSheet)
            self.detailsButton.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
            buttonsLayout.addWidget(self.detailsButton)
            self.detailsButton.clicked.connect(self.OnDetailsButtonClicked)

        mainLayout.addItem(buttonsLayout)
        self.setLayout(mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        roundedRect = QRect()
        radius = 6
        roundedRect.setX(self.rect().x() + radius / 2)
        roundedRect.setY(self.rect().y() + radius / 2)
        roundedRect.setWidth(self.rect().width() - radius)
        roundedRect.setHeight(self.rect().height() - radius)

        palette = QPalette()
        rectColor = palette.color(QPalette.Window)
        painter.setBrush(QBrush(rectColor))
        roundedRectPen = QPen(Qt.black)
        painter.setPen(roundedRectPen)

        painter.drawRoundedRect(roundedRect, radius, radius)

        closeButtonGeometry = self.closeButton.geometry()
        lineColor = palette.color(QPalette.Text)
        pen = QPen(lineColor)
        pen.setWidth(1)
        painter.setPen(pen)
        # horizontal line
        if hasattr(self, 'detailsButton'):
            detailsButtonGeometry = self.detailsButton.geometry()
            y = (closeButtonGeometry.bottom() + detailsButtonGeometry.top()) / 2
            left = QPoint(min(closeButtonGeometry.left(), detailsButtonGeometry.left()), y)
            right = QPoint(max(closeButtonGeometry.right(), detailsButtonGeometry.right())-8, y)
            painter.drawLine(left, right)

        # vertical line
        # close button and details button have Preferred size policy
        x = closeButtonGeometry.left() - pen.width()
        top = QPoint(x, roundedRect.top() + roundedRectPen.width())
        bottom = QPoint(x, roundedRect.bottom() - roundedRectPen.width())
        painter.drawLine(top, bottom)

    def opacity(self):
        return self.m_opacity

    def setOpacity(self, _opacity):
        if self.m_opacity != _opacity:
            self.m_opacity = _opacity

            self.setWindowOpacity(_opacity)

    _opacity = pyqtProperty(float, fget=opacity, fset=setOpacity)