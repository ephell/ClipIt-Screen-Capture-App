from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QFileDialog

from .Ui_Settings import Ui_Settings


class Settings(QWidget, Ui_Settings):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.browse_button.clicked.connect(self.__on_browse_button_clicked)

    @Slot()
    def __on_browse_button_clicked(self):
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Select Directory", 
            "",
            QFileDialog.ShowDirsOnly
        )
        if directory:
            self.dir_path_line_edit.setText(directory)
