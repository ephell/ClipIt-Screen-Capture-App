from logger import GlobalLogger
log = GlobalLogger.LOGGER

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from gui.recording_area_border import RecordingAreaBorder
from gui.region_selector import RegionSelector
from recorder.recorder import Recorder


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("My App")
        self.app = app
        self.region_selector = None
        self.recording_area_border = None

        select_region = QPushButton()
        select_region.setText("Select Area")
        select_region.clicked.connect(self.__on_select_region_clicked)

        start_recording_button = QPushButton()
        start_recording_button.setText("Start Recording")
        start_recording_button.clicked.connect(self.__on_start_clicked)

        stop_recording_button = QPushButton()
        stop_recording_button.setText("Stop Recording")
        stop_recording_button.clicked.connect(self.__on_stop_clicked)

        self.region_label = QLabel()
        self.region_label.setText(f"No region selected.")

        layout = QVBoxLayout()
        layout.addWidget(select_region)
        layout.addWidget(start_recording_button)
        layout.addWidget(stop_recording_button)
        layout.addWidget(self.region_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.region_selector is not None:
                self.region_selector.close()

    def __on_select_region_clicked(self):
        def get_region(x0, y0, x1, y1):
            self.region_label.setText(f"Region: ({x0}, {y0}, {x1}, {y1})")
            self.region_selector.close() 
            draw_recording_area_border(x0, y0, x1, y1)

        def draw_recording_area_border(x0, y0, x1, y1):
            self.recording_area_border = RecordingAreaBorder(x0, y0, x1, y1)
            self.recording_area_border.start()

        if self.recording_area_border is not None:
            self.recording_area_border.destroy()
        self.region_selector = RegionSelector(get_region)
        self.region_selector.show()

    def __on_stop_clicked(self):
        if self.recording_area_border is not None:
            self.recording_area_border.destroy()
            self.recording_area_border = None

    def __on_start_clicked(self):
        recorder = Recorder(
            duration=3,
            record_video=True,
            record_loopback=True,
            record_microphone=True,
            monitor=2,
            region=[60, 216, 1150, 650],
            fps=30,
        )
        recorder.record()
        log.info("All done!")
