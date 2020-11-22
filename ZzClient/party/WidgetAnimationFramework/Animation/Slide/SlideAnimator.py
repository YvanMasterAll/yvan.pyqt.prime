import math
from PyQt5.QtCore import QPropertyAnimation, QEvent, QEasingCurve, Qt, QAbstractAnimation, QRect, QObject, QPoint, QSize
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from party.WidgetAnimationFramework.AbstractAnimator import AbstractAnimator
from party.WidgetAnimationFramework.Animation.CircleFill import CircleFillDecorator
from party.WidgetAnimationFramework.Animation.Expand import ExpandDecorator
from party.WidgetAnimationFramework.Animation.Slide.SlideForegroundDecorator import SlideForegroundDecorator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn.StackedWidgetFadeInDecorator import StackedWidgetFadeInDecorator
from party.WidgetAnimationFramework.WAF import ApplicationSide, AnimationDirection


class SlideAnimator(AbstractAnimator):
    m_direction:AnimationDirection
    m_isFixBackground:bool
    m_isFixStartSize:bool
    m_startMinSize = QSize()
    m_startMaxSize = QSize()
    m_startSize = QSize()
    m_decorator: SlideForegroundDecorator
    m_animation: QPropertyAnimation

    def __init__(self, _widgetForSlide):
        super(SlideAnimator, self).__init__(_widgetForSlide)

        self.m_direction = AnimationDirection.FromLeftToRight
        self.m_isFixBackground = True
        self.m_isFixStartSize = False
        self.m_decorator = SlideForegroundDecorator(_widgetForSlide)
        self.m_animation = QPropertyAnimation(self.m_decorator, b"maximumWidth")

        _widgetForSlide.installEventFilter(self)

        self.m_animation.setDuration(300)

        self.m_decorator.hide()

        def valueChanged(_value):
            if self.isWidth():
                self.widgetForSlide().setMaximumWidth(_value)
            else:
                self.widgetForSlide().setMaximumHeight(_value)
        self.m_animation.valueChanged.connect(valueChanged)

        def finished():
            self.setAnimatedStopped()
            self.m_decorator.hide()
        self.m_animation.finished.connect(finished)

    def setAnimationDirection(self, _direction):
        if self.m_direction != _direction:
            self.m_direction = _direction
        self.m_animation.setPropertyName(b"maximumWidth" if self.isWidth() else b"maximumHeight")

    def setFixBackground(self, _fix):
        if self.m_isFixBackground != _fix:
            self.m_isFixBackground = _fix

    def setFixStartSize(self, _fix):
        if self.m_isFixStartSize != _fix:
            self.m_isFixStartSize = _fix

    def animationDuration(self):
        return self.m_animation.duration()

    def animateForward(self):
        self.slideIn()

    def slideIn(self):
        if not self.m_startMinSize.isValid():
            self.m_startMinSize = self.widgetForSlide().minimumSize()
        if not self.m_startMaxSize.isValid():
            self.m_startMaxSize = self.widgetForSlide().maximumSize()
        if not self.m_startSize.isValid():
            self.m_startSize = self.widgetForSlide().sizeHint()

        if self.isAnimated() and self.isAnimatedForward():
            return
        self.setAnimatedForward()

        if self.isWidth():
            self.widgetForSlide().setMaximumWidth(0)
        else:
            self.widgetForSlide().setMaximumHeight(0)

        self.widgetForSlide().show()
        currentSize = self.widgetForSlide().size()

        finalSize = QSize(currentSize.width(), currentSize.height())
        self.fixSize(self.m_startSize, finalSize)

        self.widgetForSlide().hide()
        self.fixSizeOfWidgetForSlide(finalSize)
        self.m_decorator.grabParent(finalSize)
        self.fixSizeOfWidgetForSlide(currentSize)
        self.widgetForSlide().show()

        if self.m_isFixBackground:
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
            self.m_animation.setStartValue(self.widgetForSlide().width() if self.isWidth() else self.widgetForSlide().height())
            self.m_animation.setEndValue(finalSize.width() if self.isWidth() else finalSize.height())
            self.m_animation.start()

    def animateBackward(self):
        self.slideOut()

    def slideOut(self):
        if not self.m_startMinSize.isValid():
            self.m_startMinSize = self.widgetForSlide().minimumSize()
        if not self.m_startMaxSize.isValid():
            self.m_startMaxSize = self.widgetForSlide().maximumSize()
        if not self.m_startSize.isValid() or not self.m_isFixStartSize:
            self.m_startSize = self.widgetForSlide().size()

        if self.isAnimated() and self.isAnimatedBackward():
            return
        self.setAnimatedBackward()

        finalSize = self.widgetForSlide().size()
        if self.isWidth():
            finalSize.setWidth(0)
        else:
            finalSize.setHeight(0)

        self.m_decorator.grabParent(self.widgetForSlide().size())

        if self.m_isFixBackground:
            self.m_decorator.move(0, 0)
            self.m_decorator.show()
            self.m_decorator.raise_()

        if self.m_animation.state() == QPropertyAnimation.Running:
            self.m_animation.pause()
            self.m_animation.setDirection(QPropertyAnimation.Backward)
            self.m_animation.resume()
        else:
            self.m_animation.setEasingCurve(QEasingCurve.InQuart)
            self.m_animation.setDirection(QPropertyAnimation.Forward)
            self.m_animation.setStartValue(self.widgetForSlide().width() if self.isWidth() else self.widgetForSlide().height())
            self.m_animation.setEndValue(finalSize.width() if self.isWidth() else finalSize.height())
            self.m_animation.start()

    def eventFilter(self, _object, _event):
        if _object == self.widgetForSlide() and _event.type() == QEvent.Resize and self.m_decorator.isVisible():
            if self.m_direction == AnimationDirection.FromLeftToRight:
                self.m_decorator.move(self.widgetForSlide().width() - self.m_decorator.width(), 0)
            if self.m_direction == AnimationDirection.FromTopToBottom:
                self.m_decorator.move(0, self.widgetForSlide().height() - self.m_decorator.height())

        return QObject.eventFilter(self, _object, _event)

    def isWidth(self):
        return self.m_direction == AnimationDirection.FromLeftToRight or self.m_direction == AnimationDirection.FromRightToLeft

    def fixSize(self, _sourceSize, _targetSize):
        if self.isWidth():
            _targetSize.setWidth(_sourceSize.width())
        else:
            _targetSize.setHeight(_sourceSize.height())

    def fixSizeOfWidgetForSlide(self, _sourceSize):
        if self.isWidth():
            self.widgetForSlide().setFixedWidth(_sourceSize.width())
        else:
            self.widgetForSlide().setFixedHeight(_sourceSize.height())


    def widgetForSlide(self):
        return self.parent()




