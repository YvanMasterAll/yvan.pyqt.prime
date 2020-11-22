class AnimationPrivate:
    m_animators = {}

    class AnimatorType:
        SideSlide = 0
        Slide = 1
        Popup = 2
        CircleFill =3
        Expand = 4

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