import math, sys
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QRect
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTextEdit, QGridLayout, QPushButton
from qtpy.QtGui import QPalette, QPainter, QBrush, QPen, QColor

from ZzClient.widget.activity.modal import Loading, Spinner

'''
菊花测试
'''

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        widget = QWidget(self)
        self.editor = QTextEdit()
        self.editor.setPlainText("0123456789" * 100)
        layout = QGridLayout(widget)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        button = QPushButton("Wait")
        layout.addWidget(button, 1, 1, 1, 1)

        self.setCentralWidget(widget)
        self.overlay = Loading(self.centralWidget())
        self.overlay.hide()
        button.clicked.connect(self.show_loading)

    def show_loading(self):
        self.timer = QTimer()
        self.timer.start(20000)
        self.timer.timeout.connect(self.close_loading)
        self.overlay.show()

    def close_loading(self):
        self.overlay.hide()

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()

class MainWindow2(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        widget = QWidget(self)
        self.editor = QTextEdit()
        self.editor.setPlainText("0123456789" * 100)
        layout = QGridLayout(widget)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        self.button = QPushButton("Wait")
        layout.addWidget(self.button, 1, 1, 1, 1)

        self.setCentralWidget(widget)

        self.setObjectName("Window")
        self.centralWidget().setObjectName("Widget")
        self.spinner = Spinner(self)
        self.spinner.setRoundness(70.0)
        self.spinner.setMinimumTrailOpacity(15.0)
        self.spinner.setTrailFadePercentage(70.0)
        self.spinner.setNumberOfLines(10)
        self.spinner.setLineLength(10)
        self.spinner.setLineWidth(5)
        self.spinner.setInnerRadius(10)
        self.spinner.setRevolutionsPerSecond(1)
        self.spinner.setColor(QColor(81, 4, 71))
        self.button.setObjectName("button")
        self.button.clicked.connect(self.show_loading)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_loading)

    def show_loading(self):
        self.timer.start(2000)
        self.setDisabled(True)
        self.spinner.start()

    def close_loading(self):
        self.spinner.stop()

if __name__ == "__main__":
    # Loading
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec_())

    # Spinner
    app = QApplication(sys.argv)
    window = MainWindow2()
    window.show()
    sys.exit(app.exec_())
