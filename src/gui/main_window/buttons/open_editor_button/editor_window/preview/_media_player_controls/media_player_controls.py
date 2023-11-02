from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from .MediaPlayerControls_ui import Ui_MediaPlayerControls


class MediaPlayerControls(Ui_MediaPlayerControls, QWidget):

    def __init__(self, media_player, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.__set_stylesheet("src\\gui\\main_window\\buttons\\open_editor_button\\editor_window\\preview\\_media_player_controls\\MediaPlayerControls.qss")
        self.media_player = media_player
        self.render_and_save_button.set_media_player(self.media_player)
        self.crop_button.set_media_player(self.media_player)
        if not self.media_player.hasAudio():
            self.volume_button.setEnabled(False)
        self.__connect_signals_and_slots()

    def __set_stylesheet(self, qss_file_path: str):
        with open(qss_file_path, "r") as qss_file:
            self.setStyleSheet(qss_file.read())

    def __connect_signals_and_slots(self):
        self.play_button.clicked.connect(self.media_player.play)
        self.pause_button.clicked.connect(self.media_player.pause)
        self.reset_button.clicked.connect(self.media_player.stop)
        self.render_and_save_button.clicked.connect(
            self.render_and_save_button.on_click
        )
        self.volume_button.volume_slider_container.slider.valueChanged.connect(
            self.__on_volume_slider_value_changed
        )
        self.upload_button.clicked.connect(self.upload_button.on_click)
        
    @Slot()
    def __on_volume_slider_value_changed(self, value):
        self.media_player.audio_output.setVolume(value / 100.0)
