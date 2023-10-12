from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QPushButton, QMainWindow, QMessageBox, QFileDialog

from .editor_window.editor_window import EditorWindow
from settings.settings import Settings


class OpenEditorButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)

    def on_open_editor_button_clicked(self):
        if self.__get_editor_window_widget() is None:
            file_dialog = _OpenFileInEditorDialog(self)
            while True:
                if file_dialog.exec() == QFileDialog.Accepted:
                    file_path = file_dialog.selectedFiles()[0]
                    if file_path.lower().endswith(".mp4"):
                        self.editor = EditorWindow(file_path)
                        self.editor.source_file_changed_signal.connect(
                            self.__on_editor_source_file_changed
                        )
                        self.editor.show()
                        break
                    else:
                        QMessageBox.critical(
                            self, 
                            "Invalid File Type", 
                            "Please select a file with '.mp4' extension."
                        )
                else:
                    break
            file_dialog.deleteLater()
        else:
            _EditorAlreadyOpenMessageBox(self).exec()

    def __get_main_window_widget(self):
        widget = self.parent()
        while widget is not None and not isinstance(widget, QMainWindow):
            widget = widget.parent()
        if widget is not None:
            return widget
        return None

    def __get_editor_window_widget(self):
        for widget in self.__get_main_window_widget().app.allWidgets():
            if isinstance(widget, EditorWindow):
                return widget
        return None

    @Slot()
    def on_file_generation_finished(self, file_path):
        if self.__get_editor_window_widget() is None:
            self.editor = EditorWindow(file_path)
            self.editor.source_file_changed_signal.connect(
                self.__on_editor_source_file_changed
            )
            self.editor.show()
        else:
            _EditorAlreadyOpenMessageBox(self).exec()

    @Slot()
    def __on_editor_source_file_changed(self, path):
        self.editor = EditorWindow(path)
        self.editor.source_file_changed_signal.connect(
            self.__on_editor_source_file_changed
        )
        self.editor.show()            


class _OpenFileInEditorDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a file to open ...")
        self.setNameFilter("Video Files (*.mp4)")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory(Settings.get_capture_dir_path())


class _EditorAlreadyOpenMessageBox(QMessageBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Editor Already Open")
        self.setText("Editor is already open.")
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.setIcon(QMessageBox.Information)
