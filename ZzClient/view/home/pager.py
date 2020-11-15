from PyQt5.QtWidgets import QStackedWidget, QWidget
from common.util.route import Navigation
from widget.view import BaseView
import importlib

'''
分页器
'''

class Pager(QStackedWidget, BaseView):

    pages = []

    def __init__(self, *args, **kwargs):
        super(Pager, self).__init__(*args, **kwargs)

    def show_page(self, navigation: Navigation):
        for page in self.pages:
            # 1).页面存在直接显示
            if page.name == navigation.name:
                self.setCurrentWidget(page.widget)
                return
        # 2).添加新的页面
        try:
            module_name = '{view}{path}'.format(view='view', path=navigation.path.replace('/', '.'))
            widget_class = getattr(importlib.import_module(module_name), navigation.name)
            widget = widget_class()
            self.addWidget(widget)
            self.pages.append(Page(navigation.name, widget))
            self.setCurrentWidget(widget)
        except Exception as e:
            print(e)
            pass

class Page:
    name = None
    widget: QWidget = None

    def __init__(self, name, widget):
        self.name = name
        self.widget = widget
