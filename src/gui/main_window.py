from logger import GlobalLogger
log = GlobalLogger.LOGGER

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout
)

from gui.button_select_area import SelectAreaButton
from recorder.recorder import Recorder


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("My App")
        self.app = app
        
        self.select_area_button = SelectAreaButton()

        start_recording_button = QPushButton()
        start_recording_button.setText("Start Recording")
        start_recording_button.clicked.connect(self.__on_start_clicked)

        stop_recording_button = QPushButton()
        stop_recording_button.setText("Stop Recording")
        stop_recording_button.clicked.connect(self.__on_stop_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.select_area_button)
        layout.addWidget(start_recording_button)
        layout.addWidget(stop_recording_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.select_area_button.area_selector is not None:
                self.select_area_button.update_area_label()
                self.select_area_button.area_selector.close()

    def __on_stop_clicked(self):
        if self.select_area_button.recording_area_border is not None:
            self.select_area_button.recording_area_border.destroy()
            self.select_area_button.recording_area_border = None
            self.select_area_button.update_area_label()

    def __on_start_clicked(self):
        if self.select_area_button.recording_area_border is not None:
            recorder = Recorder(
                duration=3,
                record_video=True,
                record_loopback=True,
                record_microphone=True,
                region=[*self.select_area_button.get_area_coords()],
                fps=30,
            )
            recorder.start()
        else:
            log.error("Recording area not selected.")
