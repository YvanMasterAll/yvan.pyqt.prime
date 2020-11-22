# import sys
# from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer
# from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient
# from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QStackedWidget, \
#     QLabel
# from qtpy import QtCore, QtWidgets
# import resources.qss.theme.dark.style_rc
# from config.theme import Theme
# from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetAnimation import StackedWidgetAnimation
# from party.WidgetAnimationFramework.WAF import AnimationDirection
# from view.home.sidebar import SideBar
# from widget.frame.button.mrxy.mrxy_button import MrxyButton
# from widget.view import BaseView
#
# Style = '''
# Window {
#     background-color: #282C34;
# }
# '''
#
# class Window(QWidget):
#     def __init__(self, *args, **kwargs):
#         super(Window, self).__init__(*args, **kwargs)
#
#         self.resize(500, 500)
#         self.setStyleSheet(Style)
#         layout = QVBoxLayout()
#         layout.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(layout)
#         stackedWidget = QStackedWidget(self)
#
#         testPage = QWidget()
#         testPage.setLayout(QVBoxLayout())
#         label = QLabel()
#         label.setText("hello")
#         testPage.layout().addWidget(label)
#
#         stackedWidget.addWidget(testPage)
#
#         sidebar = SideBar()
#         stackedWidget.addWidget(sidebar)
#         stackedWidget.setCurrentWidget(sidebar)
#         layout.addWidget(stackedWidget)
#
#         # QTimer.singleShot(1000, lambda :StackedWidgetAnimation.fadeIn(stackedWidget, testPage))
#         # xx = StackedWidgetAnimation.fadeIn(stackedWidget, testPage)
#         # StackedWidgetAnimation.slide(stackedWidget, testPage, AnimationDirection.FromLeftToRight)
#         # StackedWidgetAnimation.fadeIn(stackedWidget, testPage)
#         # StackedWidgetAnimation.slideOver(stackedWidget, testPage, AnimationDirection.FromLeftToRight, True)
#         # StackedWidgetAnimation.slideOverIn(stackedWidget, testPage, AnimationDirection.FromLeftToRight)
#         StackedWidgetAnimation.slideOverOut(stackedWidget, testPage, AnimationDirection.FromLeftToRight)
#
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     Theme.load()
#     # fontDB = QFontDatabase()
#     # font_id = fontDB.addApplicationFont(':font/Microsoft-YaHei.ttf')
#     # fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
#     # app.setFont(QFont('Microsoft YaHei'))
#     window = Window()
#     window.show()
#
#     sys.exit(app.exec_())



import sys

from PyQt5.QtCore import QTimer, QMargins, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QSizePolicy, QLabel, QHBoxLayout, QToolButton, QApplication, QWidget, QFrame, QTabBar, \
    QStackedWidget, QTextEdit, QPushButton, QVBoxLayout, QLineEdit

from party.WidgetAnimationFramework.Animation.Animation import Animation
from party.WidgetAnimationFramework.StackedWidgetAnimation.StackedWidgetAnimation import StackedWidgetAnimation
from party.WidgetAnimationFramework.WAF import AnimationDirection, ApplicationSide


class NotifyMessage(QFrame):
    m_lastHeight = 0

    def __init__(self, *args, _message, **kwargs):
        super(NotifyMessage, self).__init__(*args, **kwargs)

        self.setProperty('notifyMessage', 1)

        message = QLabel(_message, self)
        message.setProperty("notifyMessage", 1)
        message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        message.setWordWrap(True)
        close = QToolButton(self)
        close.setIcon(QIcon(":icon/logo.png"))

        layout = QHBoxLayout(self)
        layout.addWidget(message)
        layout.addWidget(close)

        close.clicked.connect(self.hideMessage)

        self.setMaximumHeight(0)
        self.m_lastHeight = 0

        timer = QTimer(self)
        def timeout():
            if self.m_lastHeight != self.maximumHeight():
                delta = self.maximumHeight() - self.m_lastHeight
                self.m_lastHeight = self.maximumHeight()
                self.parentWidget().resize(self.parentWidget().width(), self.parentWidget().height() + delta)
                self.parentWidget().move(self.parentWidget().pos().x(), self.parentWidget().pos().y() - delta)
        timer.timeout.connect(timeout)
        timer.start(10)


    def showMessage(self):
        Animation.slideIn(self, AnimationDirection.FromBottomToTop, True, False)
        QTimer.singleShot(2000, lambda :self.hideMessage())

    def hideMessage(self):
        Animation.slideOut(self, AnimationDirection.FromBottomToTop, True, False)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()

    mainToolbar = QFrame(w)
    mainToolbar.setProperty("toolbar", 1)
    mainToolbar.setFrameShape(QFrame.StyledPanel)
    mainToolbarMenuButton = QToolButton(mainToolbar)
    mainToolbarMenuButton.setIcon(QIcon(":icon/logo.png"))
    mainToolbarTitle = QLabel("<b>Widgets Animation Framework demo</b>", mainToolbar)
    mainToolbarLayout = QHBoxLayout(mainToolbar)
    mainToolbarLayout.setContentsMargins(QMargins())
    mainToolbarLayout.setSpacing(10)
    mainToolbarLayout.addWidget(mainToolbarMenuButton)
    mainToolbarLayout.addWidget(mainToolbarTitle)

    tabs = QTabBar(w)
    tabs.addTab("TEXT")
    tabs.addTab("CREDITS")

    pages = QStackedWidget(w)
    textEdit = QTextEdit(w)
    textEdit.document().setDocumentMargin(20)
    textEdit.setHtml(
        "<h1>WAF</h1>"
        "<h2>Widgets Animation Framework</h2>"
        "<p>Let you implement rich user interface interactions "
        "for applications based on Qt Widgets.</p>"
        "<h3>Side Sliding Animation</h3>"
        "<p>Slide widget from side of application and make background little darker for accent attension to slided widget. To do it just call</p>"
        "<p><pre>Animation.sideSlide</pre></p>"
        "<p>with your cool widget for slide and set application side from which their must slide.</p>"
        "<h3>Sliding Animation</h3>"
        "<p>Expand or collapse widgets in it's layout. Just call</p>"
        "<p><pre>Animation.slide</pre></p>"
        "<p>and set sliding direction."
        "<p></p>"
    )
    pages.addWidget(textEdit)

    creditsInfo = QPushButton(w)
    creditsInfo.setText("DimkaNovikov labs.")
    pages.addWidget(creditsInfo)

    mainLayout = QVBoxLayout(w)
    mainLayout.setContentsMargins(QMargins())
    mainLayout.setSpacing(0)
    mainLayout.addWidget(mainToolbar)
    mainLayout.addWidget(tabs)
    mainLayout.addWidget(pages)

    menu = QFrame(w)
    menu.setProperty("menu", 1)
    menu.setFixedWidth(300)

    menuToolbar = QFrame(menu)
    menuToolbar.setFrameShape(QFrame.StyledPanel)
    menuToolbarBackButton = QToolButton(menuToolbar)
    menuToolbarBackButton.setIcon(QIcon(":/arrow-left.png"))
    menuToolbarTitle = QLabel("<b>Menu</b>", menuToolbar)
    menuToolbarLayout = QHBoxLayout(menuToolbar)
    menuToolbarLayout.setContentsMargins(QMargins())
    menuToolbarLayout.setSpacing(10)
    menuToolbarLayout.addWidget(menuToolbarBackButton)
    menuToolbarLayout.addWidget(menuToolbarTitle)

    menuButtonLogin = QPushButton("Login", menu)
    menuButtonLogin.setProperty("menu", 1)
    menuButtonNotify = QPushButton("Notify", menu)
    menuButtonNotify.setProperty("menu", 1)
    menuButtonExit = QPushButton("Exit", menu)
    menuButtonExit.setProperty("menu", 1)
    menuLayout = QVBoxLayout(menu)
    menuLayout.setContentsMargins(QMargins())
    menuLayout.setSpacing(0)
    menuLayout.addWidget(menuToolbar)
    menuLayout.addWidget(menuButtonLogin)
    menuLayout.addWidget(menuButtonNotify)
    menuLayout.addWidget(menuButtonExit)
    menuLayout.addStretch()
    menu.hide()

    auth = QFrame(w)
    auth.setProperty("menu", 0)
    auth.setFrameShape(QFrame.StyledPanel)
    authUserName = QLineEdit(auth)
    authUserName.setPlaceholderText("User Name")
    authPassword = QLineEdit(auth)
    authPassword.setPlaceholderText("Password")
    authPassword.setEchoMode(QLineEdit.Password)
    authLoginButton = QPushButton("Login", auth)
    authCancelButton = QPushButton("Cancel", auth)
    authLayout = QVBoxLayout(auth)
    authLayout.addWidget(authUserName)
    authLayout.addWidget(authPassword)
    authButtonsLayout = QHBoxLayout()
    authButtonsLayout.addWidget(authLoginButton)
    authButtonsLayout.addWidget(authCancelButton)
    authLayout.addLayout(authButtonsLayout)
    auth.hide()

    notify = QFrame(w)
    notify.setProperty("notifyArea", 1)
    notify.setFrameShape(QFrame.NoFrame)
    connectionMessage = NotifyMessage(notify, _message="Connections estabilished")
    subscriptionMessage = NotifyMessage(notify, _message="Subscribe to <b>pro</b> account and get more available features.<br/><br/><a href=\"http://dimkanovikov.pro\">Read more</a>")
    notifyLayout = QVBoxLayout(notify)
    notifyLayout.setContentsMargins(QMargins())
    notifyLayout.setSpacing(1)
    notifyLayout.addWidget(connectionMessage)
    notifyLayout.addWidget(subscriptionMessage)
    notify.hide()

    mainToolbarMenuButton.clicked.connect(lambda: Animation.sideSlideIn(menu, ApplicationSide.LeftSide))

    def func1():
        print(1)
        Animation.sideSlideIn(auth, ApplicationSide.TopSide)
        authUserName.setFocus()
    menuButtonLogin.clicked.connect(func1)
    def func2():
        print(2)
        Animation.sideSlideOut(auth, ApplicationSide.TopSide)
        userName = authUserName.text()
        if userName == "":
            userName = "Noname"
        menuButtonLogin.setText("Logged as " + userName)
        menuButtonLogin.setEnabled(False)
    authLoginButton.clicked.connect(func2)
    authCancelButton.clicked.connect(lambda: Animation.sideSlideOut(auth, ApplicationSide.TopSide))
    def func3():
        print(3)
        Animation.sideSlideOut(menu, ApplicationSide.LeftSide)
        Animation.sideSlideIn(notify, ApplicationSide.BottomSide, False)
        def func4():
            connectionMessage.showMessage()
            QTimer.singleShot(300, lambda: subscriptionMessage.showMessage())
        QTimer.singleShot(420, Qt.PreciseTimer, func4)
    menuButtonNotify.clicked.connect(func3)
    menuButtonExit.clicked.connect(lambda: QApplication.quit)
    def func5(_showWidgetIndex):
        print(5)
        StackedWidgetAnimation.fadeIn(pages, pages.widget(_showWidgetIndex))
    tabs.currentChanged.connect(func5)
    def func6(_currentScrollPosition):
        print(6)
        lastScrollPosition = 0
        lastScrollMaximum = textEdit.verticalScrollBar().maximum()
        if lastScrollMaximum == textEdit.verticalScrollBar().maximum():
            if lastScrollPosition < _currentScrollPosition:
                if mainToolbar.height() > 0:
                    Animation.slideOut(mainToolbar, AnimationDirection.FromTopToBottom, True, False)
                    Animation.slideOut(tabs, AnimationDirection.FromTopToBottom, True, False)
                    pass
            else:
                if mainToolbar.height() == 0:
                    Animation.slideIn(mainToolbar, AnimationDirection.FromTopToBottom, True, False)
                    Animation.slideIn(tabs, AnimationDirection.FromTopToBottom, True, False)
                    pass
        lastScrollPosition = _currentScrollPosition
        lastScrollMaximum = textEdit.verticalScrollBar().maximum()
    textEdit.verticalScrollBar().valueChanged.connect(func6)

    def func7():
        print(7)
        i = 2
        Animation.circleFill(creditsInfo, creditsInfo.rect().topRight(), QColor("#66C966"), _hideAfterFinish=lambda  i:(i % 2 == 0), _in=True)
    creditsInfo.clicked.connect(func7)

    w.setStyleSheet('''
QAbstractButton { outline: none }
QToolButton { border: none; min-width: 40px; min-height: 40px; icon-size: 24px }
QTextEdit { border: none }
QPushButton[menu="1"] { text-align: left; background-color: white; border: none; border-bottom: 1px solid palette(dark); padding: 8px }
QFrame[toolbar="1"] { background-color: #66C966 }
QFrame[menu="0"] { background-color: palette(window) }
QFrame[menu="1"] { background-color: white; border: none; border-right: 1px solid palette(dark) }
QFrame[notifyArea="1"] { background-color: white }
QFrame[notifyMessage="1"] { background-color: #232323; color: white }
QLabel[notifyMessage="1"] { background-color: #232323; color: white }
'''
    )
    w.resize(400, 400)
    w.show()

    sys.exit(app.exec_())
