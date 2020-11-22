from PyQt5.QtCore import QPropertyAnimation, QEvent, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget

from party.WidgetAnimationFramework.AbstractAnimator import AbstractAnimator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn import StackedWidgetFadeInDecorator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetSlide import StackedWidgetSlideDecorator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetSlideOver.StackedWidgetSlideOverDecorator import StackedWidgetSlideOverDecorator
from party.WidgetAnimationFramework.WAF import AnimationDirection

class StackedWidgetSlideOverAnimator(AbstractAnimator):
    m_direction:AnimationDirection
    m_coveredWidget:QWidget
    m_decorator:StackedWidgetSlideOverDecorator
    m_animation:QPropertyAnimation

    def __init__(self, _container, _widgetForSlide):
        super(StackedWidgetSlideOverAnimator, self).__init__(_container)

        self.m_direction = AnimationDirection.FromLeftToRight
        self.m_coveredWidget = _container.currentWidget()
        self.m_decorator = StackedWidgetSlideOverDecorator(_container, _widgetForGrab=_widgetForSlide)
        self.m_animation = QPropertyAnimation(self.m_decorator, b"pos")

        _container.installEventFilter(self)

        self.m_animation.setDuration(400)

        self.m_decorator.hide()

        def finished():
            self.setAnimatedStopped()

            if self.isAnimatedForward():
                _container.setCurrentWidget(_widgetForSlide)
            self.m_decorator.hide()

        self.m_animation.finished.connect(finished)

    def updateCoveredWidget(self):
        self.m_coveredWidget = self.stackedWidget().currentWidget()

    def setAnimationDirection(self, _direction):
        if self.m_direction != _direction:
            self.m_direction = _direction

    def animationDuration(self):
        return self.m_animation.duration()

    def animateForward(self):
        self.slideOverIn()

    def slideOverIn(self):
        if self.isAnimated() and self.isAnimatedForward():
            return
        self.setAnimatedForward()

        self.m_decorator.grabWidget()

        startPos = QPoint()
        finalPos = QPoint()

        if self.m_direction == AnimationDirection.FromLeftToRight:
            startPos.setX(-1 * self.stackedWidget().width())
        if self.m_direction == AnimationDirection.FromRightToLeft:
            startPos.setX(self.stackedWidget().width())
        if self.m_direction == AnimationDirection.FromTopToBottom:
            startPos.setY(-1 * self.stackedWidget().height())
        if self.m_direction == AnimationDirection.FromBottomToTop:
            startPos.setY(self.stackedWidget().height())

        self.m_decorator.show()
        self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.InOutExpo)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startPos)
            self.m_animation.setEndValue(finalPos)

            self.m_animation.start()

    def animateBackward(self):
        self.slideOverOut()

    def slideOverOut(self):
        if self.isAnimated() and self.isAnimatedBackward():
            return
        self.setAnimatedBackward()

        self.m_decorator.grabWidget()

        startPos = QPoint()
        finalPos = QPoint()

        if self.m_direction == AnimationDirection.FromLeftToRight:
            finalPos.setX(-1 * self.stackedWidget().width())
        if self.m_direction == AnimationDirection.FromRightToLeft:
            finalPos.setX(self.stackedWidget().width())
        if self.m_direction == AnimationDirection.FromTopToBottom:
            finalPos.setY(-1 * self.stackedWidget().height())
        if self.m_direction == AnimationDirection.FromBottomToTop:
            finalPos.setY(self.stackedWidget().height())

        if isinstance(self.stackedWidget(), type(self)):
            self.stackedWidget().setCurrentWidget(self.m_coveredWidget)

        self.m_decorator.show()
        self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.InOutExpo)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startPos)
            self.m_animation.setEndValue(finalPos)

            self.m_animation.start()

    def eventFilter(self, _object, _event):
        if _object == self.stackedWidget() and _event.type() == QEvent.Resize and self.m_decorator.isVisible():
            self.m_decorator.grabWidget()

        return QWidget.eventFilter(self, _object, _event)

    def stackedWidget(self):
        return self.parent()
