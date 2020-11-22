from PyQt5.QtCore import QVariant, Qt, QEvent, QRectF, QRect
from PyQt5.QtGui import QPainter, QPainterPath, QFontMetrics, QPen
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyleOptionButton, QStyle, QCheckBox, \
    QApplication
from qtpy import QtGui, QtCore

from common.loader.resource import ResourceLoader
from common.util.func import calculate_middle_rect

'''
QTableViewDelegate，可以手动绘制单元格
'''

class TableDelegate(QStyledItemDelegate):

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        viewOption = QStyleOptionViewItem(option)
        self.initStyleOption(viewOption, index)
        QStyledItemDelegate.paint(self, painter, viewOption, index)

        item = index.model().data(index, Qt.UserRole)
        if isinstance(item, QVariant):
            return

        value = item['value']
        type = item['type']
        if type == 'checkbox':
            # 数据转换
            value = True if value == 1 else 0
            # 绘制单选框
            checkBoxStyle = QStyleOptionButton()
            checkBoxStyle.state = QStyle.State_On if value else QStyle.State_Off
            checkBoxStyle.state |= QStyle.State_Enabled
            # 计算位置
            size = item['size']
            rect = calculate_middle_rect(option.rect, size, size)
            checkBoxStyle.rect = rect
            checkBox = QCheckBox()
            QApplication.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, checkBoxStyle, painter, checkBox)
        if type == 'tag':
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHints(QPainter.SmoothPixmapTransform)
            path = QPainterPath()

            # 绘制文本
            self.font = ResourceLoader().qt_font_text_tag
            text_color = item['text_color']
            border_color = item['border_color']
            text = value
            padding_v = 2
            padding_h = 4
            border_radius = 2
            border_width = 1
            painter.setFont(item['font'])
            painter.setPen(text_color)
            fm = QFontMetrics(painter.font())
            w = fm.width(text)
            h = fm.height()
            # 计算位置
            rect = calculate_middle_rect(option.rect, w + padding_h * 2, h + padding_v * 2)
            rectf = QRectF(rect.x(), rect.y(), rect.width(), rect.height())
            painter.drawText(QRect(rectf.x() + padding_h, rectf.y() + padding_v, w, h), Qt.TextWordWrap, text)
            # 绘制边框
            path.addRoundedRect(rectf, border_radius, border_radius)
            painter.strokePath(path, QPen(border_color, border_width))

    def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> bool:
        decorationRect = option.rect

        if event.type() == QEvent.MouseButtonPress and calculate_middle_rect(decorationRect, 20, 20).contains(event.pos()):
            item = index.model().data(index, Qt.UserRole)

            if isinstance(item, QVariant):
                return QStyledItemDelegate.editorEvent(self, event, model, option, index)

            value = item['value']
            type = item['type']
            if type == 'checkbox':
                # 数据转换
                value = 1 if value == 0 else 0
                model.setData(index, value, Qt.DisplayRole)

        return QStyledItemDelegate.editorEvent(self, event, model, option, index)