import math

from PyQt5.QtCore import QPropertyAnimation, QEvent, QEasingCurve, Qt, QAbstractAnimation, QRect, QObject
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from party.WidgetAnimationFramework.AbstractAnimator import AbstractAnimator
from party.WidgetAnimationFramework.Animation.CircleFill import CircleFillDecorator
from party.WidgetAnimationFramework.Animation.Expand.ExpandDecorator import ExpandDecorator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn.StackedWidgetFadeInDecorator import StackedWidgetFadeInDecorator


class ExpandAnimator(AbstractAnimator):
    m_decorator: ExpandDecorator
    m_animation: QPropertyAnimation
    m_expandRect: QRect

    def __init__(self, _widgetForFill):
        super(ExpandAnimator, self).__init__(_widgetForFill)

        self.m_decorator = ExpandDecorator(_widgetForFill)
        self.m_animation = QPropertyAnimation(self.m_decorator, b"_expandRect")

        _widgetForFill.installEventFilter(self)

        self.m_animation.setDuration(400)

        self.m_decorator.hide()

        def finished():
            self.setAnimatedStopped()
            if self.isAnimatedBackward():
                self.m_decorator.hide()

        self.m_animation.finished.connect(finished)

    def setExpandRect(self, _rect):
        self.m_expandRect = _rect
        self.m_decorator.setExpandRect(_rect)

    def setFillColor(self, _color):
        self.m_decorator.setFillColor(_color)

    def animationDuration(self):
        return self.m_animation.duration()

    def animateForward(self):
        self.expandIn()

    def expandIn(self):
        if self.isAnimated() and self.isAnimatedForward():
            return
        self.setAnimatedForward()

        startExpandRect = self.m_expandRect
        finalExpandRect = self.widgetForFill().rect()

        self.m_decorator.resize(self.widgetForFill().size())
        self.m_decorator.move(0, 0)
        self.m_decorator.grabExpandRect()
        self.m_decorator.show()
        self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startExpandRect)
            self.m_animation.setEndValue(finalExpandRect)
            self.m_animation.start()

    def animateBackward(self):
        self.expandOut()

    def expandOut(self):
        if self.isAnimated() and self.isAnimatedBackward():
            return
        self.setAnimatedBackward()

        startExpandRect = self.widgetForFill().rect()
        finalExpandRect = self.m_expandRect

        self.m_decorator.resize(self.widgetForFill().size())
        self.m_decorator.move(0, 0)
        self.m_decorator.hide()
        self.m_decorator.grabExpandRect()
        self.m_decorator.show()
        self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startExpandRect)
            self.m_animation.setEndValue(finalExpandRect)
            self.m_animation.start()

    def eventFilter(self, _object, _event):
        if _object == self.widgetForFill() and _event.type() == QEvent.Resize and self.m_decorator.isVisible():
            self.m_decorator.resize(self.widgetForFill().size())
            self.m_animation.setEndValue(self.widgetForFill().rect())

        return QObject.eventFilter(self, _object, _event)

    def widgetForFill(self):
        return self.parent()


