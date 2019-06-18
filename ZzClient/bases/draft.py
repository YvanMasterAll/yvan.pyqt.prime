
"""重写鼠标事件实现窗口拖动"""

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

"""悬停属性"""
# self.setAttribute(Qt.WA_Hover, True)