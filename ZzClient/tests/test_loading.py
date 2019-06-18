import math, sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTextEdit, QGridLayout, QPushButton
from qtpy.QtGui import QPalette, QPainter, QBrush, QPen, QColor
from tooltip import Loading

# 测试菊花

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
