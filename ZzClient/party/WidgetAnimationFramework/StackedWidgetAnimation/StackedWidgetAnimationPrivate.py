class StackedWidgetAnimationPrivate:
    m_animators = {}

    class AnimatorType:
        Slide = 0
        SlideOver = 1
        FadeIn = 2
        ExpandOrCollapse =3

    def hasAnimator(self, _widget, _animatorType):
        contains = False
        if self.m_animators.__contains__(_animatorType):
            contains = self.m_animators[_animatorType].__contains__(_widget)
        return contains

    def animator(self, _widget, _animatorType):
        animator = 0
        if self.m_animators.__contains__(_animatorType):
            if self.m_animators[_animatorType].__contains__(_widget):
                animator = self.m_animators[_animatorType][_widget]
        return animator

    def saveAnimator(self, _widget, _animator, _animatorType):
        if not self.hasAnimator(_widget, _animatorType):
            animators = {}
            animators[_widget] = _animator
            self.m_animators[_animatorType] = animators