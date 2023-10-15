from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QPushButton, QFileDialog


class BrowseButton(QPushButton):

    new_directory_selected_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.clicked.connect(self.__on_browse_button_clicked)

    @Slot()
    def __on_browse_button_clicked(self):
        directory_path = QFileDialog.getExistingDirectory(
            self, 
            "Select Directory",
            "",
            QFileDialog.ShowDirsOnly
        )
        if directory_path:
            self.new_directory_selected_signal.emit(directory_path)
    