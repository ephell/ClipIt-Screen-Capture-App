from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .preview.preview import Preview
from .timeline.timeline import Timeline


class Editor(QWidget):

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlag(Qt.Window)
        self.preview = Preview(file_path)
        self.timeline = Timeline(self.preview.media_player.duration())
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.preview)
        self.layout.addWidget(self.timeline)
        self.setLayout(self.layout)

        self.timeline.scene.ruler_handle_time_changed.connect(
            self.on_ruler_handle_time_changed
        )
        self.preview.media_player.positionChanged.connect(
            self.on_media_player_position_changed
        )
        self.preview.media_player.positionChanged.connect(
            self.on_reaching_media_end_time
        )
        self.timeline.scene.media_item_start_time_changed.connect(
            self.on_media_item_start_time_changed
        )
        self.timeline.scene.media_item_end_time_changed.connect(
            self.on_media_item_end_time_changed
        )

    """Override"""
    def closeEvent(self, event):
        super().closeEvent(event)
        if self.parent() is not None:
            for attr_name, attr_value in vars(self.parent()).items():
                if isinstance(attr_value, Editor):
                    setattr(self.parent(), attr_name, None)
                    break

    @Slot()
    def on_ruler_handle_time_changed(self, time_ms):
        self.preview.media_player.setPosition(time_ms)

    @Slot()
    def on_media_player_position_changed(self, time_ms):
        self.timeline.ruler.ruler_handle.on_media_player_position_changed(
            time_ms
        )

    @Slot()
    def on_reaching_media_end_time(self, current_time):
        end_time = self.timeline.media_item.end_time
        if current_time >= end_time:
            self.preview.media_player.pause()
            self.preview.media_player.setPosition(end_time)

    @Slot()
    def on_media_item_start_time_changed(self, new_start_time):
        self.preview.media_player.update_start_time(new_start_time)

    @Slot()
    def on_media_item_end_time_changed(self, new_end_time):
        self.preview.media_player.update_end_time(new_end_time)
