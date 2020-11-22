import math

from PyQt5.QtCore import QPropertyAnimation, QEvent, QEasingCurve, Qt, QAbstractAnimation
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from party.WidgetAnimationFramework.AbstractAnimator import AbstractAnimator
from party.WidgetAnimationFramework.Animation.CircleFill.CircleFillDecorator import CircleFillDecorator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn.StackedWidgetFadeInDecorator import StackedWidgetFadeInDecorator


class CircleFillAnimator(AbstractAnimator):
    m_decorator: CircleFillDecorator
    m_animation: QPropertyAnimation
    m_hideAfterFinish = True

    def __init__(self, _widgetForFill):
        super(CircleFillAnimator, self).__init__(_widgetForFill)

        self.m_decorator = CircleFillDecorator(_widgetForFill)
        self.m_animation = QPropertyAnimation(self.m_decorator, b"_radius")

        _widgetForFill.installEventFilter(self)

        self.m_animation.setDuration(500)

        self.m_decorator.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.m_decorator.hide()

        def finished():
            self.setAnimatedStopped()
            if self.m_hideAfterFinish:
                self.hideDecorator()

        self.m_animation.finished.connect(finished)

    def setStartPoint(self, _point):
        self.m_decorator.setStartPoint(_point)

    def setFillColor(self, _color):
        self.m_decorator.setFillColor(_color)

    def setHideAfterFinish(self, _hide):
        self.m_hideAfterFinish = _hide

    def animationDuration(self):
        return self.m_animation.duration()

    def animateForward(self):
        self.fillIn()

    def fillIn(self):
        if self.isAnimated() and self.isAnimatedForward():
            return
        self.setAnimatedForward()

        startRadius = 0
        finalRadius = math.sqrt(
            self.widgetForFill().height() * self.widgetForFill().height() + self.widgetForFill().width() * self.widgetForFill().width())

        self.m_decorator.resize(self.widgetForFill().size())
        self.m_decorator.move(0, 0)
        self.m_decorator.show()
        self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.OutQuart)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startRadius)
            self.m_animation.setEndValue(finalRadius)
            self.m_animation.start()

    def animateBackward(self):
        self.fillOut()

    def fillOut(self):
        if self.isAnimated() and self.isAnimatedBackward():
            return
        self.setAnimatedBackward()

        startRadius = math.sqrt(
            self.widgetForFill().height() * self.widgetForFill().height() + self.widgetForFill().width() * self.widgetForFill().width())
        finalRadius = 0

        self.m_decorator.resize(self.widgetForFill().size())
        self.m_decorator.move(0, 0)
        self.m_decorator.show()
        self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.OutQuart)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startRadius)
            self.m_animation.setEndValue(finalRadius)
            self.m_animation.start()

    def hideDecorator(self):
        hideEffect = self.m_decorator.graphicsEffect()
        if hideEffect == None:
            hideEffect = QGraphicsOpacityEffect(self.m_decorator)
            self.m_decorator.setGraphicsEffect(hideEffect)
        hideEffect.setOpacity(1)

        hideAnimation = QPropertyAnimation(hideEffect, b"opacity", self.m_decorator)
        hideAnimation.setDuration(400)
        hideAnimation.setStartValue(1)
        hideAnimation.setEndValue(0)

        def finished():
            self.m_decorator.hide()
            hideEffect.setOpacity(1)

        hideAnimation.finished.connect(finished)

        hideAnimation.start(QAbstractAnimation.DeleteWhenStopped)

    def widgetForFill(self):
        return self.parent()


