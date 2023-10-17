from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from .preview.preview import Preview
from .timeline.timeline import Timeline


class EditorWindow(QWidget):

    editor_position_changed_signal = Signal()
    editor_resized_signal = Signal()
    source_file_changed_signal = Signal(str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ClipIt - Editor")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlag(Qt.Window)
        self.preview = Preview(file_path, self)
        self.timeline = Timeline(self.preview.media_player.duration(), self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.preview)
        self.layout.addWidget(self.timeline)
        self.setLayout(self.layout)
        self.__connect_signals_and_slots()
        # Used to track changes done to the uploaded file.
        self.__initial_start_time = 0
        self.__initial_end_time = self.preview.media_player.duration()
        self.__initial_video_width = 0
        self.__initial_video_height = 0

    def __connect_signals_and_slots(self):
        self.timeline.scene.ruler_handle_time_changed.connect(
            self.__on_ruler_handle_time_changed
        )
        self.preview.media_player.positionChanged.connect(
            self.__on_media_player_position_changed
        )
        self.preview.media_player.positionChanged.connect(
            self.__on_reaching_media_end_time
        )
        self.timeline.scene.media_item_start_time_changed.connect(
            self.__on_media_item_start_time_changed
        )
        self.timeline.scene.media_item_end_time_changed.connect(
            self.__on_media_item_end_time_changed
        )
        self.editor_position_changed_signal.connect(
            self.preview.media_player_controls.volume_button.on_editor_position_changed
        )
        self.editor_resized_signal.connect(
            self.preview.media_player_controls.volume_button.on_editor_resized
        )
        self.preview.media_player_controls.upload_button.upload_file_signal.connect(
            self.__on_upload_file_signal
        )
        self.preview.media_player_controls.render_and_save_button.file_rendered_signal.connect(
            self.__on_file_rendered_signal
        )
        self.preview.scene.video_output_native_size_changed_signal.connect(
            self.__on_video_output_native_size_changed
        )
        self.preview.media_player.finished_collecting_media_item_thumbnail_frames.connect(
            self.timeline.media_item.on_finished_collecting_media_item_thumbnail_frames
        )

    """Override"""
    def closeEvent(self, event):
        if self.__has_file_been_edited():
            user_choice = QMessageBox.question(
                self,
                "Confirm Close",
                "Unsaved changes detected. \n"
                "Are you sure you want to close the editor without saving?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if user_choice == QMessageBox.Yes:
                event.accept()
                super().closeEvent(event)
            else:
                event.ignore()

        # Delete the editor object from the parent if parent exists.
        if self.parent() is not None:
            for attr_name, attr_value in vars(self.parent()).items():
                if isinstance(attr_value, EditorWindow):
                    setattr(self.parent(), attr_name, None)
                    break

    """Override"""
    def moveEvent(self, event):
        super().moveEvent(event)
        self.editor_position_changed_signal.emit()

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.editor_resized_signal.emit()

    @Slot()
    def __on_ruler_handle_time_changed(self, time_ms):
        self.preview.media_player.setPosition(time_ms)

    @Slot()
    def __on_media_player_position_changed(self, time_ms):
        self.timeline.ruler.ruler_handle.on_media_player_position_changed(
            time_ms
        )

    @Slot()
    def __on_reaching_media_end_time(self, current_time):
        end_time = self.timeline.media_item.end_time
        if current_time >= end_time:
            self.preview.media_player.pause()
            self.preview.media_player.setPosition(end_time)

    @Slot()
    def __on_media_item_start_time_changed(self, new_start_time):
        self.preview.media_player.update_start_time(new_start_time)

    @Slot()
    def __on_media_item_end_time_changed(self, new_end_time):
        self.preview.media_player.update_end_time(new_end_time)

    @Slot()
    def __on_upload_file_signal(self, path):
        """
        Emitting a signal to main window instead of redrawing all editor's
        widgets, because the update() calls don't provide the expected
        results.
        """
        if self.__has_file_been_edited():
            user_choice = QMessageBox.question(
                self,
                "Confirm Upload",
                "Unsaved changes detected. \n"
                "Are you sure you want to upload another file without saving?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if user_choice == QMessageBox.Yes:
                self.source_file_changed_signal.emit(path)
        else:
            self.source_file_changed_signal.emit(path)

    @Slot()
    def __on_video_output_native_size_changed(self, width, height):
        """Set the video resolution values when it's first loaded."""
        self.__initial_video_width = width
        self.__initial_video_height = height

    @Slot()
    def __on_file_rendered_signal(self):
        """Update initial values of media item to ones after rendering."""
        self.__initial_start_time = self.timeline.media_item.start_time
        self.__initial_end_time = self.timeline.media_item.end_time
        self.__initial_video_width = self.preview.media_player.video_output.width
        self.__initial_video_height = self.preview.media_player.video_output.height

    def __has_file_been_edited(self):
        if self.__has_duration_changed():
            return True
        if self.__has_resolution_changed():
            return True

    def __has_duration_changed(self):
        return (
            self.timeline.media_item.start_time != self.__initial_start_time
            or self.timeline.media_item.end_time != self.__initial_end_time
        )
    
    def __has_resolution_changed(self):
        return (
            self.preview.media_player.video_output.width != self.__initial_video_width
            or self.preview.media_player.video_output.height != self.__initial_video_height
        )
