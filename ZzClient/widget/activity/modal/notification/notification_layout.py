from PyQt5.QtCore import QObject, Qt, QPoint, QElapsedTimer, QBasicTimer, \
    QEvent
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from widget.activity.modal.notification.notification_widget import NotificationWidget

class NotificationLayout(QObject):
    displayTimeMs = 2000
    maximumDisplayCount = 5
    elapsedTimer = QElapsedTimer()
    basicTimer = QBasicTimer()
    layoutType = Qt.AlignTop | Qt.AlignRight
    notifications = {}

    def __init__(self, *args, **kwargs):
        super(NotificationLayout, self).__init__(*args, **kwargs)

        self.basicTimer.start(600, self)

    def destroyed(self, object = ...) -> None:
        self.Clear()

    def AddNotificationWidget(self, parent, params):
        if not parent:
            desktop = QApplication.desktop()
            desktop.setGeometry(desktop.availableGeometry())
            parent = desktop
        if self.notifications.__contains__(parent):
            parent.installEventFilter(self)
            parent.destroyed.connect(self.OnParentWidgetDestroyed)

        widget = NotificationWidget(parent, params=params)
        widget.CloseButtonClicked.connect(self.OnCloseClicked)
        widget.DetailsButtonClicked.connect(self.OnDetailsClicked)
        widget.destroyed.connect(self.OnWidgetDestroyed)

        widgetParams = params
        widgetParams.InitAnimation(widget)

        widgetParams.callback = params.callback
        widgetParams.remainTimeMs = self.displayTimeMs

        if not self.notifications.__contains__(parent):
            self.notifications[parent] = []
        self.notifications[parent].append((widget, widgetParams))

        self.LayoutWidgets(parent)

    def LayoutWidgets(self, parent):
        totalHeight = 0
        widgets = self.notifications[parent]

        size = min(len(widgets), self.maximumDisplayCount)
        widgetsToDisplay = widgets[:size]
        if self.layoutType & Qt.AlignTop:
            widgetsToDisplay.reverse()
        for pair in widgetsToDisplay:
            widget = pair[0]
            justCreated = False
            if widget.isVisible() == False:
                justCreated = True
                opacityAnimation = pair[1].opacityAnimation
                widget.show()
                opacityAnimation.setStartValue(0.0)
                opacityAnimation.setEndValue(1.0)
                opacityAnimation.start()

            x = 0 if self.layoutType & Qt.AlignLeft else (parent.width() - widget.width())
            y = totalHeight if self.layoutType & Qt.AlignTop else parent.height() - widget.height() - totalHeight
            widgetPos = QPoint(x, y)

            # noticationWidget marked as window inside Qt, self case we need to use global coordinates
            # if not mark it as window - on OS X notification will be behind from RenderWidget

            widgetPos = parent.mapToGlobal(widgetPos)

            if justCreated:
                widget.move(widgetPos)
            else:
                positionAnimation = pair[1].positionAnimation
                positionAnimation.stop()
                positionAnimation.setStartValue(widget.pos())
                positionAnimation.setEndValue(widgetPos)
                positionAnimation.start()

            totalHeight += widget.size().height()

    def Clear(self):
        for widgets in self.notifications:
            for pair in widgets:
                widget = pair[0]
                widget.close()
                widget.setParent(None)

        self.notifications.clear()

    def eventFilter(self, sender, event):
        type = event.type()
        if type == QEvent.Resize or type == QEvent.Move:
            self.LayoutWidgets(sender)

        return QObject.eventFilter(self, sender, event)

    def timerEvent(self, event):
        elapsedMs = self.elapsedTimer.restart()
        for parent in self.notifications:
            widgets = self.notifications[parent]
            if parent.isActiveWindow() or isinstance(parent, QDesktopWidget):
                for pair in widgets:
                    widget = pair[0]
                    params = pair[1]
                    params.DecrementTime(elapsedMs)
                    if params.remainTimeMs == 0:
                        widget.setParent(None)
                        widget.close()
                        widgets.remove(pair)
                self.LayoutWidgets(parent)
                return

    def SetLayoutType(self, type):
        if self.layoutType == type:
            return

        self.layoutType = type

        # now remove all notifications
        self.Clear()

    def SetDisplayTimeMs(self, displayTimeMs_):
        self.displayTimeMs = displayTimeMs_;

    def OnCloseClicked(self, notification):
        notification.setParent(None)
        for parent in self.notifications:
            widgets = self.notifications[parent]
            for pair in widgets:
                if pair[0] == notification:
                    widgets.remove(pair)
                    notification.close()
                    self.LayoutWidgets(parent)
                    return

    def OnDetailsClicked(self, notification):
        parent = notification.parentWidget()
        widgets = self.notifications[parent]

        for pair in widgets:
            if pair[0] == notification:
                pair[1].callback()
                break

        del notification

    def OnWidgetDestroyed(self):
        notification = self.sender()
        for parent in self.notifications:
            widgets = self.notifications[parent]
            _notification = None
            for pair in widgets:
                if pair[0] == notification:
                    _notification = pair[0]
                    break
            if _notification:
                self.LayoutWidgets(parent)
                return

    def OnParentWidgetDestroyed(self):
        senderWidget = self.sender()
        if self.notifications.__contains__(senderWidget):
            del self.notifications[senderWidget]

