from PyQt5.QtCore import QPropertyAnimation, QEvent, QEasingCurve, QPoint
from PyQt5.QtWidgets import QWidget

from party.WidgetAnimationFramework.AbstractAnimator import AbstractAnimator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn import StackedWidgetFadeInDecorator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetSlide.StackedWidgetSlideDecorator import StackedWidgetSlideDecorator
from party.WidgetAnimationFramework.WAF import AnimationDirection

class StackedWidgetSlideAnimator(AbstractAnimator):
    m_direction:AnimationDirection
    m_containerDecorator:StackedWidgetSlideDecorator
    m_widgetDecorator:StackedWidgetSlideDecorator
    m_containerAnimation:QPropertyAnimation
    m_widgetAnimation:QPropertyAnimation

    def __init__(self, _container, _widgetForSlide):
        super(StackedWidgetSlideAnimator, self).__init__(_container)

        self.m_direction = AnimationDirection.FromLeftToRight
        self.m_containerDecorator = StackedWidgetSlideDecorator(_container, _widgetForGrab=_container.currentWidget())
        self.m_widgetDecorator = StackedWidgetSlideDecorator(_container, _widgetForGrab=_widgetForSlide)
        self.m_containerAnimation = QPropertyAnimation(self.m_containerDecorator, b"pos")
        self.m_widgetAnimation = QPropertyAnimation(self.m_widgetDecorator, b"pos")

        _container.installEventFilter(self)

        self.m_containerAnimation.setDuration(400)
        self.m_widgetAnimation.setDuration(400)

        self.m_containerDecorator.hide()
        self.m_widgetDecorator.hide()

        def finished():
            self.setAnimatedStopped()
            _container.setCurrentWidget(_widgetForSlide)
            self.m_containerDecorator.hide()
            self.m_widgetDecorator.hide()

        self.m_widgetAnimation.finished.connect(finished)

    def setAnimationDirection(self, _direction):
        if self.m_direction != _direction:
            self.m_direction = _direction

    def animationDuration(self):
        return self.m_containerAnimation.duration()

    def animateForward(self):
        self.slide()

    def slide(self):
        if self.isAnimated() and self.isAnimatedForward():
            return
        self.setAnimatedForward()

        self.m_containerDecorator.grabContainer()
        self.m_widgetDecorator.grabWidget()

        containerStartPos = QPoint()
        containerFinalPos = QPoint()
        widgetStartPos = QPoint()
        widgetFinalPos = QPoint()
        if self.m_direction == AnimationDirection.FromLeftToRight:
            containerFinalPos.setX(self.widgetForSlide().width())
            widgetStartPos.setX(-1 * self.widgetForSlide().width())
        if self.m_direction == AnimationDirection.FromRightToLeft:
            containerFinalPos.setX(-1 * self.widgetForSlide().width())
            widgetStartPos.setX(self.widgetForSlide().width())
        if self.m_direction == AnimationDirection.FromTopToBottom:
            containerFinalPos.setY(self.widgetForSlide().height())
            widgetStartPos.setY(-1 * self.widgetForSlide().height())
        if self.m_direction == AnimationDirection.FromBottomToTop:
            containerFinalPos.setY(-1 * self.widgetForSlide().height())
            widgetStartPos.setY(self.widgetForSlide().height())

        self.m_containerDecorator.move(containerStartPos)
        self.m_containerDecorator.show()
        self.m_containerDecorator.raise_()
        self.m_widgetDecorator.move(widgetStartPos)
        self.m_widgetDecorator.show()
        self.m_widgetDecorator.raise_()

        if self.m_widgetAnimation.state() == QPropertyAnimation.Running:
            self.m_containerAnimation.pause()
            self.m_containerAnimation.setDirection(QPropertyAnimation.Backward)
            self.m_containerAnimation.resume()
            self.m_widgetAnimation.pause()
            self.m_widgetAnimation.setDirection(QPropertyAnimation.Backward)
            self.m_widgetAnimation.resume()
        else:
            self.m_containerAnimation.setEasingCurve(QEasingCurve.InOutExpo)
            self.m_containerAnimation.setDirection(QPropertyAnimation.Forward)
            self.m_containerAnimation.setStartValue(containerStartPos)
            self.m_containerAnimation.setEndValue(containerFinalPos)
            self.m_widgetAnimation.setEasingCurve(QEasingCurve.InOutExpo)
            self.m_widgetAnimation.setDirection(QPropertyAnimation.Forward)
            self.m_widgetAnimation.setStartValue(widgetStartPos)
            self.m_widgetAnimation.setEndValue(widgetFinalPos)

            self.m_containerAnimation.start()
            self.m_widgetAnimation.start()

    def eventFilter(self, _object, _event):
        if _object == self.widgetForSlide() and _event.type() == QEvent.Resize and self.m_containerDecorator.isVisible() and self.m_widgetDecorator.isVisible():
            self.m_containerDecorator.grabWidget()
            self.m_widgetDecorator.grabWidget()

        return QWidget.eventFilter(self, _object, _event)

    def widgetForSlide(self):
        return self.parent()
