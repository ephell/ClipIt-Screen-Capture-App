from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog

from .Ui_RenderingProgressDialog import Ui_RenderingProgressDialog


class RenderingProgressDialog(QDialog, Ui_RenderingProgressDialog):
    """Shows progress of rendering when saving from the editor."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(self.size())
        self.close_button.clicked.connect(self.close)
        self.is_rendering_complete = False

    """Override"""
    def keyPressEvent(self, event):
        if not self.is_rendering_complete:
            if event.key() == Qt.Key_Escape:
                event.ignore()
        else:
            super().keyPressEvent(event)

    @Slot()
    def on_rendering_complete(self):
        self.status_message_label.setText("File successfully rendered and saved!")
        self.close_button.setEnabled(True)
        self.is_rendering_complete = True
