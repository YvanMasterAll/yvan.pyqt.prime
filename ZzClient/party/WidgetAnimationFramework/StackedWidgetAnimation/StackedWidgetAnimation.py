from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetAnimationPrivate import \
    StackedWidgetAnimationPrivate
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetFadeIn.StackedWidgetFadeInAnimator import \
    StackedWidgetFadeInAnimator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetSlide.StackedWidgetSlideAnimator import \
    StackedWidgetSlideAnimator
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetSlideOver.StackedWidgetSlideOverAnimator import StackedWidgetSlideOverAnimator

class StackedWidgetAnimation:
    m_pimpl = 0

    @classmethod
    def pimpl(cls):
        if cls.m_pimpl == 0:
            cls.m_pimpl = StackedWidgetAnimationPrivate()

        return cls.m_pimpl

    @classmethod
    def slide(cls, _container, _widget, _direction):
        animatorType = StackedWidgetAnimationPrivate.AnimatorType.Slide
        animator = 0
        if cls.pimpl().hasAnimator(_widget, animatorType):
            animator = cls.pimpl().animator(_widget, animatorType)
            if isinstance(animator, StackedWidgetSlideAnimator):
                animator.setAnimationDirection(_direction)
        else:
            slideAnimator = StackedWidgetSlideAnimator(_container, _widget)
            slideAnimator.setAnimationDirection(_direction)
            animator = slideAnimator

            cls.pimpl().saveAnimator(_widget, animator, animatorType)

        animator.animateForward()

    @classmethod
    def slideOverIn(cls, _container, _widget, _direction):
        IN = True
        cls.slideOver(_container, _widget, _direction, IN)

    @classmethod
    def slideOverOut(cls, _container, _widget, _direction):
        OUT = False
        cls.slideOver(_container, _widget, _direction, OUT)

    @classmethod
    def slideOver(cls, _container, _widget, _direction, _in):
        animatorType = StackedWidgetAnimationPrivate.AnimatorType.SlideOver
        animator = 0
        if cls.pimpl().hasAnimator(_widget, animatorType):
            animator = cls.pimpl().animator(_widget, animatorType)
            if isinstance(animator, StackedWidgetSlideOverAnimator):
                if _in:
                    animator.updateCoveredWidget()
                animator.setAnimationDirection(_direction)
        else:
            slideOverAnimator = StackedWidgetSlideOverAnimator(_container, _widgetForSlide=_widget)
            slideOverAnimator.setAnimationDirection(_direction)
            animator = slideOverAnimator

            cls.pimpl().saveAnimator(_widget, animator, animatorType)

        if _in:
            animator.animateForward()
        else:
            animator.animateBackward()

    @classmethod
    def fadeIn(cls, _container, _widget):
        animatorType = StackedWidgetAnimationPrivate.AnimatorType.FadeIn
        animator = 0
        if cls.pimpl().hasAnimator(_widget, animatorType):
            animator = cls.pimpl().animator(_widget, animatorType)
        else:
            fadeInAnimator = StackedWidgetFadeInAnimator(_container, _widget)
            animator = fadeInAnimator

            cls.pimpl().saveAnimator(_widget, animator, animatorType)

        animator.animateForward()

        return animator.animationDuration()