from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QFileDialog

from .Ui_Settings import Ui_Settings
from settings.settings import Settings as SettingsConfig


class Settings(QWidget, Ui_Settings):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.__connect_signals_and_slots()
        self.__load_capture_dir_path_to_line_edit()

    def __connect_signals_and_slots(self):
        self.browse_button.clicked.connect(self.__on_browse_button_clicked)
        self.dir_path_line_edit.textChanged.connect(
            self.__on_dir_path_line_edit_text_changed
        )

    def __load_capture_dir_path_to_line_edit(self):
        self.dir_path_line_edit.setText(SettingsConfig.get_capture_dir_path())

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

    @Slot()
    def __on_dir_path_line_edit_text_changed(self):
        SettingsConfig.set_capture_dir_path(self.dir_path_line_edit.text())
