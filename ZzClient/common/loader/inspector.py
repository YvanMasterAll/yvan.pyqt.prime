from qtpy.QtWidgets import QShortcut
from qtpy.QtCore import Qt

'''
样式注入器
'''

class ConnectStyleSheetInspector(object):

    def __init__(self, main_window, shortcut):
        self.shortcut = shortcut
        self.main_window = main_window
        shortcut_ = QShortcut(self.shortcut, main_window)
        shortcut_.setContext(Qt.ApplicationShortcut)

        def ShowStyleSheetEditor():
            style_sheet_inspector_class = GetStyleSheetInspectorClass()
            style_sheet_inspector = [
                c for c in self.main_window.children() if
                isinstance(c, style_sheet_inspector_class)]
            if style_sheet_inspector:
                style_sheet_inspector = style_sheet_inspector[0]
            else:
                style_sheet_inspector = style_sheet_inspector_class(self.main_window)
                style_sheet_inspector.setFixedSize(600, 400)
            style_sheet_inspector.show()

        shortcut_.activated.connect(ShowStyleSheetEditor)

def GetStyleSheetInspectorClass():
    """
    Indirection mostly to simplify test.
    """
    try:
        from qt_style_sheet_inspector import StyleSheetInspector
    except ImportError as error:
        msg = 'You need to Install qt_style_sheet_inspector.'
        raise RuntimeError(msg)
    return StyleSheetInspector