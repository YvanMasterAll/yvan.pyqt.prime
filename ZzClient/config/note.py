
'''
重写鼠标事件实现窗口拖动
'''

# def mousePressEvent(self, event):
#     if event.buttons() == Qt.LeftButton:
#         self.parent.m_drag = True
#         self.parent.m_DragPosition = event.globalPos() - self.parent.pos()
#         event.accept()
#
# def mouseMoveEvent(self, event):
#     try:
#         if event.buttons() and Qt.LeftButton:
#             self.parent.move(event.globalPos() - self.parent.m_DragPosition)
#             event.accept()
#     except AttributeError:
#         pass
#
# def mouseReleaseEvent(self, event):
#     if event.buttons() == Qt.LeftButton:
#         self.m_drag = False

'''
悬停属性
'''
# self.setAttribute(Qt.WA_Hover, True)

'''
父类函数
'''
# super(ToolTip, self).eventFilter(widget, event)

'''
判断系统类型
'''
# if not family:
# if platform.system().lower() == 'darwin':
# family = ".AppleSystemUIFont"
# else:
# family = "Microsoft Yahei"

'''
画圆角
'''

# QPainterPath path;
# path.moveTo(rect.topRight() - QPointF(radius, 0));
# path.lineTo(rect.topLeft() + QPointF(radius, 0));
# path.quadTo(rect.topLeft(), rect.topLeft() + QPointF(0, radius));
# path.lineTo(rect.bottomLeft() + QPointF(0, -radius));
# path.quadTo(rect.bottomLeft(), rect.bottomLeft() + QPointF(radius, 0));
# path.lineTo(rect.bottomRight() - QPointF(radius, 0));
# path.quadTo(rect.bottomRight(), rect.bottomRight() + QPointF(0, -radius));
# path.lineTo(rect.topRight() + QPointF(0, radius));
# path.quadTo(rect.topRight(), rect.topRight() + QPointF(-radius, -0));