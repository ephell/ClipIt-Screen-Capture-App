from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from .Ui_Settings import Ui_Settings


class Settings(QWidget, Ui_Settings):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlag(Qt.Window)
