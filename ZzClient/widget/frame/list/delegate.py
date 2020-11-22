from PyQt5.QtCore import QVariant, QRectF, QEvent, QSize, Qt
from PyQt5.QtGui import QPainter, QImage, QPainterPath, QPen
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle
from qtpy import QtGui, QtCore

from common.loader.resource import ResourceLoader
from common.util.func import calculate_text_rect, calculate_middle_rect, toDateStr

'''
QListView代理，手动绘制列表项
'''

class ListDelegate(QStyledItemDelegate):
    loading_rotate = 0

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        if not index.isValid():
            return
        if option.state & QStyle.State_Selected:
            pass
        if option.state & QStyle.State_MouseOver:
            pass

        item = index.model().data(index, Qt.UserRole)
        if isinstance(item, QVariant):
            return

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)

        value = item['value']
        type = item['type']
        x = option.rect.x()
        y = option.rect.y()
        w = option.rect.width()
        h = option.rect.height()
        if type == 'device_activity':
            painter.save()
            # 图标
            icon = QImage(ResourceLoader().icon_path(value['icon']))
            rect_icon = QRectF(x + 20, y + 13, 44, 44)
            painter.drawImage(rect_icon, icon)
            # 设备标签
            painter.setFont(ResourceLoader().qt_font_text_xs)
            rect = calculate_text_rect('设备', painter=painter, x=x + 70, y=y + 15)
            painter.drawText(rect, Qt.TextSingleLine, '设备')
            # 设备编号
            painter.setPen(ResourceLoader().qt_color_label_link)
            painter.setFont(ResourceLoader().qt_font_text_xs)
            rect = calculate_text_rect(value['device'], painter=painter, x=x+110, y=y+15)
            painter.drawText(rect, Qt.TextSingleLine, value['device'])
            # 活动内容
            painter.setPen(ResourceLoader().qt_color_sub_text)
            painter.setFont(ResourceLoader().qt_font_text_xss)
            content = value['content'] + '，' + toDateStr()
            rect = calculate_text_rect(content, painter=painter, x=x + 70, y=y + 40)
            painter.drawText(rect, Qt.TextSingleLine, content)
            # 绘制边框
            path = QPainterPath()
            path.addRoundedRect(QRectF(x + 4, y + 4, w - 8, h - 8), 4, 4)
            painter.strokePath(path, QPen(ResourceLoader().qt_color_background, 1))

            painter.restore()
        elif type == 'load_more':
            # 绘制加载图标
            # painter.save()
            # painter.translate(x+16, y+16)
            # self.loading_rotate += 5
            # painter.rotate(self.loading_rotate%360)
            # icon = qtawesome.icon('mdi.loading', color=ResourceLoader().qt_color_sub_text)
            # icon_pixmap = icon.pixmap(QSize(32, 32))
            # painter.drawPixmap(QRect(-16, -16, 32, 32), icon_pixmap)
            # painter.restore()
            # 绘制加载信息
            painter.save()
            painter.setFont(ResourceLoader().qt_font_text_xs)
            painter.setPen(ResourceLoader().qt_color_sub_text)
            _rect = calculate_text_rect('~~~ 正在努力加载 ~~~', painter=painter)
            rect = calculate_middle_rect(option.rect, width=_rect.width(), height=_rect.height())
            painter.drawText(rect, Qt.TextSingleLine, '~~~ 正在努力加载 ~~~')
            painter.restore()
        elif type == 'no_more':
            painter.save()
            painter.setFont(ResourceLoader().qt_font_text_xs)
            painter.setPen(ResourceLoader().qt_color_sub_text)
            _rect = calculate_text_rect('--- 我是有底线的 ---', painter=painter)
            rect = calculate_middle_rect(option.rect, width=_rect.width(), height=_rect.height())
            painter.drawText(rect, Qt.TextSingleLine, '--- 我是有底线的 ---')
            painter.restore()
        else:
            self.initStyleOption(option, index)
            QStyledItemDelegate.paint(self, painter, option, index)

    def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> bool:
        decorationRect = option.rect

        if event.type() == QEvent.MouseButtonPress:
            item = index.model().data(index, Qt.UserRole)
            if isinstance(item, QVariant):
                return QStyledItemDelegate.editorEvent(self, event, model, option, index)

            type = item['type']
            value = item['value']
            if type == 'device_activity':
                text_rect = calculate_text_rect(value['device'], font=ResourceLoader().qt_font_text_xs)
                if calculate_middle_rect(decorationRect, text_rect.width(), text_rect.height(), x=110, y=15).contains(event.pos()):
                    print('点击了设备{device}'.format(device=value['device']))

        return QStyledItemDelegate.editorEvent(self, event, model, option, index)

    def sizeHint(self, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtCore.QSize:
        if not index.isValid():
            return QSize()
        item = index.model().data(index, Qt.UserRole)
        type = item['type']
        if type == 'string':
            return QSize(0, 50)
        if type == 'device_activity':
            return QSize(0, 70)
        if type == 'load_more':
            return QSize(0, 40)
        if type == 'no_more':
            return QSize(0, 40)