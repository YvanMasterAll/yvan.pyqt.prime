from PyQt5.QtCore import QPoint, QEasingCurve, Qt, QPropertyAnimation
from PyQt5.QtWidgets import QScrollArea, QWidget

from widget.frame.card.zoom_card import ZoomCard

'''
网格布局
'''

class GridLayout(QScrollArea):
    item_spacing_h = 10
    item_spacing_v = 10
    fixed_width = 140
    fixed_height = 240
    widgets = []

    def __init__(self, *args, **kwargs):
        super(GridLayout, self).__init__(*args, **kwargs)

        self.center_widget = QWidget(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.center_widget)

    def load(self, items):
        '''
        加载组件
        '''
        for widget in self.widgets:
            widget.deleteLater()
        self.widgets = []

        for item in items:
            item.setFixedWidth(self.fixed_width)
            item.setFixedHeight(self.fixed_height)
            self.widgets.append(item)

        self.resizeLayout()

    def resizeLayout(self):
        if len(self.widgets) == 0:
            return
        gpw_width = self.fixed_width
        gpw_height = self.fixed_height
        bar_width = self.verticalScrollBar().width()
        # 一列数量
        col_count = max((self.center_widget.width()-self.item_spacing_h-bar_width) / (gpw_width + self.item_spacing_h), 1)
        if col_count > len(self.widgets):
            col_count = len(self.widgets)
        # 行数
        row_count = max((len(self.widgets) + col_count - 1) / col_count, 1)
        total_height = row_count * (gpw_height + self.item_spacing_v) + self.item_spacing_v*2
        self.center_widget.setMinimumHeight(total_height)
        self.center_widget.resize(self.center_widget.width(), total_height)
        total_left = (self.center_widget.width() - col_count * (gpw_width + self.item_spacing_h)) / 2
        total_top = self.item_spacing_v

        cur_row = 0
        cur_col = 0
        for widget in self.widgets:
            pos = QPoint(total_left + cur_col * (gpw_width + self.item_spacing_h), total_top + cur_row * (gpw_height + self.item_spacing_v))
            ani = QPropertyAnimation(widget, b"pos", self)
            ani.setStartValue(widget.pos())
            ani.setEndValue(pos)
            ani.setDuration(300)
            ani.setEasingCurve(QEasingCurve.OutQuad)
            ani.finished.connect(ani.deleteLater)
            ani.start()

            cur_col += 1
            if cur_col >= col_count:
                cur_col = 0
                cur_row += 1

    def startAnimation(self):
        pass

    def resizeEvent(self, event):
        super(GridLayout, self).resizeEvent(event)
        self.center_widget.setFixedWidth(self.width())
        self.resizeLayout()