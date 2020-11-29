import sys
from PyQt5.QtCore import QSize, Qt, QObject, QPoint, QTimer, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPixmap, QColor, QFontDatabase, QFont, QBrush, QIcon, QLinearGradient, QGradient, \
    QGuiApplication, QPainter
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton, QHBoxLayout, QSpacerItem, QLabel

class Toast(QWidget):
    m_opacity = 1
    fade_in:QPropertyAnimation
    fade_out:QPropertyAnimation

    def __init__(self, *args, **kwargs):
        super(Toast, self).__init__(*args, **kwargs)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.Tool) # 无边框，无任务栏
        self.setAttribute(Qt.WA_TranslucentBackground, True) # 背景透明
        self.set_ui()

    def set_ui(self):
        # 1).样式为什么设置不了
        # 2).为什么我写的代码不设置父窗口就直接消失
        self.setObjectName('Toast')
        self.setStyleSheet('background-color:#0F1012;border-radius:6px;padding:10px;')
        layout = QHBoxLayout(self)
        self.label = QLabel()
        layout.addWidget(self.label)

    def setText(self, msg):
        self.label.setText(msg)

    def showAnimation(self, timeout=2000):
        # 开始动画
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(200)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()
        self.show()

        def finish():
            # 结束动画
            self.fade_out = QPropertyAnimation(self, b"windowOpacity")
            self.fade_out .setDuration(200)
            self.fade_out .setStartValue(1)
            self.fade_out .setEndValue(0)
            self.fade_out .start()

            def _finish():
                self.close()
                self.deleteLater()  # 关闭后析构

            self.fade_out .finished.connect(_finish)

        QTimer.singleShot(timeout, finish)

    @staticmethod
    def showTip(text, parent=None):
        toast = Toast(parent)
        toast.setWindowFlags(toast.windowFlags() | Qt.WindowStaysOnTopHint)  # 置顶
        toast.setText(text)
        toast.adjustSize()  # 设置完文本后调整下大小

        # 测试显示位于主屏的65%高度位置
        pScreen = QGuiApplication.primaryScreen()
        toast.move((pScreen.size().width() - toast.width()) / 2, pScreen.size().height() * 6.5 / 10)
        toast.showAnimation()