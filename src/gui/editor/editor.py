from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from .preview.preview import Preview
from .timeline.timeline import Timeline


class Editor(QWidget):

    editor_position_changed_signal = Signal()

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

    """Override"""
    def closeEvent(self, event):
        super().closeEvent(event)
        if self.parent() is not None:
            for attr_name, attr_value in vars(self.parent()).items():
                if isinstance(attr_value, Editor):
                    setattr(self.parent(), attr_name, None)
                    break

    """Override"""
    def moveEvent(self, event):
        super().moveEvent(event)
        self.editor_position_changed_signal.emit()

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
