from logger import GlobalLogger
log = GlobalLogger.LOGGER

import mss
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
        self.recording_area_top_x = None
        self.recording_area_top_y = None
        self.recording_area_bottom_x = None
        self.recording_area_bottom_y = None

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
        """Callback function for the select region button."""
        def get_region(x0, y0, x1, y1):
            """Callback function for the region selector."""
            if not is_within_single_monitor_bounds(x0, y0, x1, y1):
                log.error("Region must be within a single monitor.")
                self.region_selector.close()
                return
            
            self.region_label.setText(f"Region: ({x0}, {y0}, {x1}, {y1})")
            self.region_selector.close() 
            draw_recording_area_border(x0, y0, x1, y1)
            self.recording_area_top_x = x0
            self.recording_area_top_y = y0
            self.recording_area_bottom_x = x1
            self.recording_area_bottom_y = y1

        def is_within_single_monitor_bounds(x0, y0, x1, y1):
            with mss.mss() as sct:
                monitors = sct.monitors
                monitor_index_1 = None
                monitor_index_2 = None
                for i in range(1, len(monitors)):
                    m = monitors[i]
                    if (m["left"] <= x0 < m["left"] + m["width"] 
                        and m["top"] <= y0 < m["top"] + m["height"]):
                        monitor_index_1 = i
                    if (m["left"] <= x1 < m["left"] + m["width"] 
                        and m["top"] <= y1 < m["top"] + m["height"]):
                        monitor_index_2 = i

                if monitor_index_1 == monitor_index_2:
                    return True
                else:
                    return False

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
        if self.recording_area_border is not None:
            recorder = Recorder(
                duration=5,
                record_video=True,
                record_loopback=True,
                record_microphone=True,
                region=[
                    self.recording_area_top_x,
                    self.recording_area_top_y,
                    self.recording_area_bottom_x - self.recording_area_top_x,
                    self.recording_area_bottom_y - self.recording_area_top_y
                ],
                fps=30,
            )
            recorder.start()
        else:
            log.error("No region selected.")
