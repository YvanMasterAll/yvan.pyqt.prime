import math

from PyQt5.QtCore import QPropertyAnimation, QEvent, QEasingCurve, Qt, QAbstractAnimation, QRect, QObject, QPoint
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from party.WidgetAnimationFramework.AbstractAnimator import AbstractAnimator
from party.WidgetAnimationFramework.Animation.CircleFill import CircleFillDecorator
from party.WidgetAnimationFramework.Animation.Expand import ExpandDecorator
from party.WidgetAnimationFramework.Animation.SideSlide.SideSlideDecorator import SideSlideDecorator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn.StackedWidgetFadeInDecorator import StackedWidgetFadeInDecorator
from party.WidgetAnimationFramework.WAF import ApplicationSide, AnimationDirection


class SideSlideAnimator(AbstractAnimator):
    m_side:ApplicationSide
    m_decorateBackground:bool
    m_decorator:SideSlideDecorator
    m_animation:QPropertyAnimation

    def __init__(self, _widgetForSlide):
        super(SideSlideAnimator, self).__init__(_widgetForSlide)

        self.m_side = ApplicationSide()
        self.m_decorateBackground = True
        self.m_decorator = SideSlideDecorator(_widgetForSlide.parentWidget())
        self.m_animation = QPropertyAnimation(self.m_decorator, b"_slidePos")

        _widgetForSlide.parentWidget().installEventFilter(self)

        self.m_animation.setEasingCurve(QEasingCurve.InQuad)
        self.m_animation.setDuration(260)

        self.m_decorator.hide()

        def finished():
            self.setAnimatedStopped()
            if self.isAnimatedForward():
                self.widgetForSlide().move(self.m_decorator.slidePos())
            else:
                self.m_decorator.hide()
        self.m_animation.finished.connect(finished)

        self.m_decorator.clicked.connect(self.slideOut)

    def setApplicationSide(self, _side):
        if self.m_side != _side:
            self.m_side = _side

    def setDecorateBackground(self, _decorate):
        if self.m_decorateBackground != _decorate:
            self.m_decorateBackground = _decorate

    def animationDuration(self):
        return self.m_animation.duration()

    def animateForward(self):
        self.slideIn()

    def slideIn(self):
        if self.isAnimated() and self.isAnimatedForward():
            return
        self.setAnimatedForward()

        self.widgetForSlide().lower()
        self.widgetForSlide().move(-self.widgetForSlide().width(), -self.widgetForSlide().height())
        self.widgetForSlide().show()
        self.widgetForSlide().resize(self.widgetForSlide().sizeHint())

        _topWidget = self.widgetForSlide()
        topWidget = self.widgetForSlide()
        while _topWidget:
            topWidget = _topWidget
            _topWidget = topWidget.parentWidget()

        finalSize = self.widgetForSlide().size()
        startPosition = QPoint()
        finalPosition = QPoint()
        if self.m_side == ApplicationSide.LeftSide:
            finalSize.setHeight(topWidget.height())
            startPosition = QPoint(-finalSize.width(), 0)
            finalPosition = QPoint(0, 0)
        if self.m_side == ApplicationSide.TopSide:
            finalSize.setWidth(topWidget.width())
            startPosition = QPoint(0, -finalSize.height())
            finalPosition = QPoint(0, 0)
        if self.m_side == ApplicationSide.RightSide:
            finalSize.setHeight(topWidget.height())
            startPosition = QPoint(topWidget.width(), 0)
            finalPosition = QPoint(topWidget.width() - finalSize.width(), 0)
        if self.m_side == ApplicationSide.BottomSide:
            finalSize.setWidth(topWidget.width())
            startPosition = QPoint(0, topWidget.height())
            finalPosition = QPoint(0, topWidget.height() - finalSize.height())

        if self.m_decorateBackground:
            self.m_decorator.setParent(topWidget)
            self.m_decorator.move(0, 0)
            self.m_decorator.grabParent()
            self.m_decorator.show()
            self.m_decorator.raise_()

        self.widgetForSlide().move(startPosition)
        self.widgetForSlide().resize(finalSize)
        self.widgetForSlide().raise_()

        self.m_decorator.grabSlideWidget(self.widgetForSlide())

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.OutQuart)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(startPosition)
            self.m_animation.setEndValue(finalPosition)
            self.m_animation.start()

        if self.m_decorateBackground:
            DARKER = True
            self.m_decorator.decorate(DARKER)

    def animateBackward(self):
        self.slideOut()

    def slideOut(self):
        if self.isAnimated() and self.isAnimatedBackward():
            return
        self.setAnimatedBackward()

        if self.widgetForSlide().isVisible():
            _topWidget = self.widgetForSlide()
            topWidget = self.widgetForSlide()
            while _topWidget:
                topWidget = _topWidget
                _topWidget = topWidget.parentWidget()

            self.widgetForSlide().hide()

            finalSize = self.widgetForSlide().size()
            startPosition = self.widgetForSlide().pos()
            finalPosition = QPoint()
            if self.m_side == ApplicationSide.LeftSide:
                startPosition = QPoint(0, 0)
                finalPosition = QPoint(-finalSize.width(), 0)
            if self.m_side == ApplicationSide.TopSide:
                startPosition = QPoint(0, 0)
                finalPosition = QPoint(0, -finalSize.height())
            if self.m_side == ApplicationSide.RightSide:
                startPosition = QPoint(topWidget.width() - finalSize.width(), 0)
                finalPosition = QPoint(topWidget.width(), 0)
            if self.m_side == ApplicationSide.BottomSide:
                startPosition = QPoint(0, topWidget.height() - finalSize.height())
                finalPosition = QPoint(0, topWidget.height())

            if self.m_animation.state() == QPropertyAnimation.Running:
                self.m_animation.pause()
                self.m_animation.setDirection(QPropertyAnimation.Backward)
                self.m_animation.resume()
            else:
                self.m_animation.setEasingCurve(QEasingCurve.InQuart)
                self.m_animation.setDirection(QPropertyAnimation.Forward)
                self.m_animation.setStartValue(startPosition)
                self.m_animation.setEndValue(finalPosition)
                self.m_animation.start()

            if self.m_decorateBackground:
                LIGHTER = False
                self.m_decorator.decorate(LIGHTER)

    def eventFilter(self, _object, _event):
        if _object == self.widgetForSlide().parentWidget() and _event.type() == QEvent.Resize:
            widgetForSlideParent = self.widgetForSlide().parentWidget()
            if self.m_side == ApplicationSide.RightSide:
                self.widgetForSlide().move(widgetForSlideParent.width() - self.widgetForSlide().width(), 0)
            if self.m_side == ApplicationSide.LeftSide:
                self.widgetForSlide().resize(self.widgetForSlide().width(), widgetForSlideParent.height())
            if self.m_side == ApplicationSide.BottomSide:
                self.widgetForSlide().move(0, widgetForSlideParent.height() - self.widgetForSlide().height())
            if self.m_side == ApplicationSide.TopSide:
                self.widgetForSlide().resize(widgetForSlideParent.width(), self.widgetForSlide().height())

            self.m_decorator.grabSlideWidget(self.widgetForSlide())

        return QObject.eventFilter(self, _object, _event)

    def widgetForSlide(self):
        return self.parent()



