from PyQt5.QtCore import QPropertyAnimation


class NotificationParams:
    HINT, INFO, WARN, ERROR = range(4)

    remainTimeMs = 0
    positionAnimation:QPropertyAnimation = None
    opacityAnimation:QPropertyAnimation = None

    def __init__(self, type=0, message='提示信息', title='提示', detailsButtonText='详情', callback=None):
        super(NotificationParams, self).__init__()
        self.type = type
        self.message = message
        self.title = title
        self.detailsButtonText = detailsButtonText
        self.callback = callback

    def InitAnimation(self, target):
        self.positionAnimation = QPropertyAnimation(target, b"pos")
        durationTimeMs = 120
        self.positionAnimation.setDuration(durationTimeMs)

        self.opacityAnimation = QPropertyAnimation(target, b"_opacity")
        self.opacityAnimation.setDuration(durationTimeMs * 2)

    def DecrementTime(self, elapsedMs):
        if elapsedMs > self.remainTimeMs:
            self.remainTimeMs = 0
        else:
            self.remainTimeMs -= elapsedMs