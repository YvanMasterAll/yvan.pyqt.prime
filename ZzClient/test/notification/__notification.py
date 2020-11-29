import sys
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QPushButton
from qtpy import QtGui
from bloc.app import Bloc_App
from common.loader.resource import ResourceLoader
from config.theme import Theme
from widget.activity.modal.notification.notification_layout import NotificationLayout
from widget.activity.modal.notification.notification_params import NotificationParams

Style = '''
Window {
    background-color: #282C34;   
}
'''

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.resize(500, 500)
        self.setStyleSheet(Style)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.notificationLayout = NotificationLayout()

        btn = QPushButton()
        btn.setText("点我")
        btn.clicked.connect(self.on_pushButton_success_clicked)
        layout.addWidget(btn)

        btn2 = QPushButton()
        btn2.setText("点我")
        btn2.clicked.connect(self.on_pushButton_error_clicked)
        layout.addWidget(btn2)

        btn3 = QPushButton()
        btn3.setText("点我")
        btn3.clicked.connect(self.on_pushButton_hint_clicked)
        layout.addWidget(btn3)

        btn4 = QPushButton()
        btn4.setText("点我")
        btn4.clicked.connect(self.on_pushButton_window_clicked)
        layout.addWidget(btn4)

    def on_pushButton_error_clicked(self):
        params = NotificationParams(title="提示", type=NotificationParams.WARN, message='提示信息。', detailsButtonText='详情', callback=lambda :self.on_pushButton_success_clicked())
        self.notificationLayout.AddNotificationWidget(self, params)

    def on_pushButton_success_clicked(self):
        params = NotificationParams(title="提示", type=NotificationParams.INFO, message='提示信息最经常的工作是将一些项目的数据从数据库导出，然后分门别类的列到excel表格中，领导看起来眼花缭乱。')
        self.notificationLayout.AddNotificationWidget(self, params)

    def on_pushButton_hint_clicked(self):
        params = NotificationParams(title="提示", message='提示信息最经常的工作是将一些项目的数据从数据库导出，然后分门别类的列到excel表格中，领导看起来眼花缭乱。')
        self.notificationLayout.AddNotificationWidget(self, params)

    def on_pushButton_window_clicked(self):
        params = NotificationParams(title="提示", message='提示信息最经常的工作是将一些项目的数据从数据库导出，然后分门别类的列到excel表格中，领导看起来眼花缭乱。')
        self.notificationLayout.AddNotificationWidget(params=params, parent=None)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        Bloc_App().app_closed.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Theme.load()
    app.setFont(ResourceLoader.load_app_font())
    window = Window()
    window.show()

    sys.exit(app.exec_())