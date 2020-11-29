from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel
from common.loader.resource import ResourceLoader

class SysDialog(QObject):
    INFO, ERROR, WARN, PROMOT, WARN_PROMOT = range(5)

    @staticmethod
    def show(type=0, msg='空对话框', confirm=None, cancel=None):
        if type == SysDialog.INFO:
            message = QMessageBox(QMessageBox.Information, "消息提示框", msg)
            qyes = message.addButton("确定", QMessageBox.YesRole)
            message.setWindowIcon(ResourceLoader().qt_icon_project_ico)
            if confirm:
                qyes.clicked.connect(confirm)
            message.exec_()
        elif type == SysDialog.WARN:
            message = QMessageBox(QMessageBox.Warning, "警告提示框", msg)
            qyes = message.addButton("确定", QMessageBox.YesRole)
            if confirm:
                qyes.clicked.connect(confirm)
            message.setWindowIcon(ResourceLoader().qt_icon_project_ico)
            message.exec_()
        elif type == SysDialog.WARN_PROMOT:
            message = QMessageBox(QMessageBox.Warning, "警告确认框", msg)
            qyes = message.addButton("确定", QMessageBox.YesRole)
            qno = message.addButton("取消", QMessageBox.NoRole)
            message.setWindowIcon(ResourceLoader().qt_icon_project_ico)
            if cancel:
                qno.clicked.connect(cancel)
            if confirm:
                qyes.clicked.connect(confirm)
            message.exec_()
        elif type == SysDialog.ERROR:
            message = QMessageBox(QMessageBox.Critical, "错误提示框", msg)
            qyes = message.addButton("确定", QMessageBox.YesRole)
            message.setWindowIcon(ResourceLoader().qt_icon_project_ico)
            if confirm:
                qyes.clicked.connect(confirm)
            message.exec_()
        elif type == SysDialog.PROMOT:
            message = QMessageBox(QMessageBox.Question, "确认提示框", msg)
            qyes = message.addButton("确定", QMessageBox.YesRole)
            qno = message.addButton("取消", QMessageBox.NoRole)
            if cancel:
                qno.clicked.connect(cancel)
            if confirm:
                qyes.clicked.connect(confirm)
            message.setWindowIcon(ResourceLoader().qt_icon_project_ico)
            message.exec_()