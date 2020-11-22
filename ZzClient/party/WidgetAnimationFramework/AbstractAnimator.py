from PyQt5.QtCore import QObject


class AbstractAnimator(QObject):
    m_isAnimated = False
    m_isAnimatedForward = True

    def setAnimatedForward(self):
        self.m_isAnimated = True
        self.m_isAnimatedForward = True

    def setAnimatedBackward(self):
        self.m_isAnimated = True
        self.m_isAnimatedForward = False

    def setAnimatedStopped(self):
        self.m_isAnimated = False

    def isAnimated(self):
        return self.m_isAnimated

    def isAnimatedForward(self):
        return self.m_isAnimatedForward

    def isAnimatedBackward(self):
        return not self.isAnimatedForward()