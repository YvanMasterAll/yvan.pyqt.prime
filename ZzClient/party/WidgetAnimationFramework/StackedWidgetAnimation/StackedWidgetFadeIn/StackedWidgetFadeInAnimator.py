from PyQt5.QtCore import QPropertyAnimation, QEvent, QEasingCurve, pyqtSignal
from PyQt5.QtWidgets import QWidget

from party.WidgetAnimationFramework.AbstractAnimator import AbstractAnimator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn.StackedWidgetFadeInDecorator import StackedWidgetFadeInDecorator


class StackedWidgetFadeInAnimator(AbstractAnimator):
    m_decorator: StackedWidgetFadeInDecorator
    m_animation: QPropertyAnimation

    def __init__(self, _container, _fadeWidget):
        super(StackedWidgetFadeInAnimator, self).__init__(_container)

        self.m_decorator = StackedWidgetFadeInDecorator(_container, _fadeWidget=_fadeWidget)
        self.m_animation = QPropertyAnimation(self.m_decorator, b"opacity")

        _container.installEventFilter(self)

        self.m_animation.setDuration(200)

        self.m_decorator.hide()

        def finished():
            self.setAnimatedStopped()

            if self.m_animation.direction() == QPropertyAnimation.Forward:
                _container.setCurrentWidget(_fadeWidget)
            self.m_decorator.hide()

        self.m_animation.finished.connect(finished)

    def animationDuration(self):
        return self.m_animation.duration()

    def animateForward(self):
        self.fadeIn()

    def fadeIn(self):
        if self.isAnimated() and self.isAnimatedForward():
            return
        self.setAnimatedForward()

        self.m_decorator.grabContainer()
        self.m_decorator.grabFadeWidget()

        startOpacity = 0
        finalOpacity = 1

        self.m_decorator.setOpacity(startOpacity)
        self.m_decorator.move(0, 0)
        self.m_decorator.show()
        self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.InQuad)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startOpacity)
            self.m_animation.setEndValue(finalOpacity)

            self.m_animation.start()

    def eventFilter(self, _object, _event):
        if _object == self.fadeWidget() and _event.type() == QEvent.Resize and self.m_decorator.isVisible():
            self.m_decorator.grabContainer()
            self.m_decorator.grabFadeWidget()

        return QWidget.eventFilter(self, _object, _event)

    def fadeWidget(self):
        return self.parent()

