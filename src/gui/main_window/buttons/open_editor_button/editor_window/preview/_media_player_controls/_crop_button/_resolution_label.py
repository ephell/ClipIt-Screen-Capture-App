from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel


class ResolutionLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.label_text = "Width: {} | Height: {}"
        self.setText(self.label_text.format(0, 0))

    @Slot()
    def on_cropper_resized_signal(self, top_x, top_y, width, height):
        self.setText(self.label_text.format(width, height))

    @Slot()
    def on_video_output_native_size_changed_signal(self, width, height):
        """Sets the initial width and height of the video output."""
        self.setText(self.label_text.format(width, height))
