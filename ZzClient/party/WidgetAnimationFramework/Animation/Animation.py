from party.WidgetAnimationFramework.Animation.AnimationPrivate import AnimationPrivate
from party.WidgetAnimationFramework.Animation.CircleFill.CircleFillAnimator import CircleFillAnimator
from party.WidgetAnimationFramework.Animation.Expand.ExpandAnimator import ExpandAnimator
from party.WidgetAnimationFramework.Animation.SideSlide.SideSlideAnimator import SideSlideAnimator
from party.WidgetAnimationFramework.Animation.Slide.SlideAnimator import SlideAnimator


class Animation:
    m_pimpl = 0

    @classmethod
    def pimpl(cls):
        if cls.m_pimpl == 0:
            cls.m_pimpl = AnimationPrivate()

        return cls.m_pimpl

    @classmethod
    def runAnimation(cls, _animator, _in):
        if _in:
            _animator.animateForward()
        else:
            _animator.animateBackward()

        return _animator.animationDuration()

    @classmethod
    def sideSlideIn(cls, _widget, _side, _decorateBackground=True):
        IN = True
        return cls.sideSlide(_widget, _side, IN, _decorateBackground)

    @classmethod
    def sideSlideOut(cls, _widget, _side, _decorateBackground=True):
        OUT = False
        return cls.sideSlide(_widget, _side, OUT, _decorateBackground)

    @classmethod
    def sideSlide(cls, _widget, _side, _in, _decorateBackground=True):
        animatorType = AnimationPrivate.AnimatorType.SideSlide
        animator = 0
        if cls.pimpl().hasAnimator(_widget, animatorType):
            animator = cls.pimpl().animator(_widget, animatorType)
            if isinstance(animator, SideSlideAnimator):
                animator.setApplicationSide(_side)
                animator.setDecorateBackground(_decorateBackground)
        else:
            sideSlideAnimator = SideSlideAnimator(_widget)
            sideSlideAnimator.setApplicationSide(_side)
            sideSlideAnimator.setDecorateBackground(_decorateBackground)
            animator = sideSlideAnimator

            cls.pimpl().saveAnimator(_widget, animator, animatorType)

        return cls.runAnimation(animator, _in)

    @classmethod
    def slideIn(cls, _widget, _direction, _fixBackground, _fixStartSize):
        IN = True
        return cls.slide(_widget, _direction, _fixBackground, _fixStartSize, IN)

    @classmethod
    def slideOut(cls, _widget, _direction, _fixBackground, _fixStartSize):
        OUT = False
        return cls.slide(_widget, _direction, _fixBackground, _fixStartSize, OUT)

    @classmethod
    def slide(cls, _widget, _direction, _fixBackground, _fixStartSize, _in):
        animatorType = AnimationPrivate.AnimatorType.Slide
        animator = 0
        if cls.pimpl().hasAnimator(_widget, animatorType):
            animator = cls.pimpl().animator(_widget, animatorType)
            if isinstance(animator, SlideAnimator):
                animator.setAnimationDirection(_direction)
                animator.setFixBackground(_fixBackground)
                animator.setFixStartSize(_fixStartSize)
        else:
            slideAnimator = SlideAnimator(_widget)
            slideAnimator.setAnimationDirection(_direction)
            slideAnimator.setFixBackground(_fixBackground)
            slideAnimator.setFixStartSize(_fixStartSize)
            animator = slideAnimator

            cls.pimpl().saveAnimator(_widget, animator, animatorType)

        return cls.runAnimation(animator, _in)

    @classmethod
    def circleFillIn(cls, _widget, _startPoint, _fillColor, _hideAfterFinish):
        IN = True
        return cls.circleFill(_widget, _startPoint, _fillColor, _hideAfterFinish, IN)

    @classmethod
    def circleFillOut(cls, _widget, _startPoint, _fillColor, _hideAfterFinish):
        OUT = False
        return cls.circleFill(_widget, _startPoint, _fillColor, _hideAfterFinish, OUT)

    @classmethod
    def circleFill(cls, _widget, _startPoint, _fillColor, _hideAfterFinish, _in):
        animatorType = AnimationPrivate.AnimatorType.CircleFill
        animator = 0
        if cls.pimpl().hasAnimator(_widget, animatorType):
            animator = cls.pimpl().animator(_widget, animatorType)
            if isinstance(animator, CircleFillAnimator):
                animator.setStartPoint(_startPoint)
                animator.setFillColor(_fillColor)
                animator.setHideAfterFinish(_hideAfterFinish)
        else:
            circleFillAnimator = CircleFillAnimator(_widget)
            circleFillAnimator.setStartPoint(_startPoint)
            circleFillAnimator.setFillColor(_fillColor)
            circleFillAnimator.setHideAfterFinish(_hideAfterFinish)
            animator = circleFillAnimator

            cls.pimpl().saveAnimator(_widget, animator, animatorType)

        return cls.runAnimation(animator, _in)

    @classmethod
    def expand(cls, _widget, _expandRect, _fillColor, _in):
        animatorType = AnimationPrivate.AnimatorType.Expand
        animator = 0
        if cls.pimpl().hasAnimator(_widget, animatorType):
            animator = cls.pimpl().animator(_widget, animatorType)
            if isinstance(animator, ExpandAnimator):
                animator.setExpandRect(_expandRect)
                animator.setFillColor(_fillColor)
        else:
            expandAnimator = ExpandAnimator(_widget)
            expandAnimator.setExpandRect(_expandRect)
            expandAnimator.setFillColor(_fillColor)
            animator = expandAnimator

            cls.pimpl().saveAnimator(_widget, animator, animatorType)

        return cls.runAnimation(animator, _in)