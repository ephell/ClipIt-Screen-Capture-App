import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from recording_area_border import RecordingAreaBorder
from region_selector import RegionSelector


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

    def __on_stop_clicked(self):
        if self.recording_area_border is not None:
            self.recording_area_border.destroy()
            self.recording_area_border = None

    def __on_select_region_clicked(self):
        if self.recording_area_border is not None:
            self.recording_area_border.destroy()
        self.region_selector = RegionSelector(self.__get_region)
        self.region_selector.show()

    def __get_region(self, x0, y0, x1, y1):
        self.region_label.setText(
            f"Region selected: ({x0}, {y0}) ({x1}, {y1})"
        )
        self.region_selector.close() 
        self.__draw_recording_area_border(x0, y0, x1, y1)

    def __draw_recording_area_border(self, x0, y0, x1, y1):
        self.recording_area_border = RecordingAreaBorder(x0, y0, x1, y1)
        self.recording_area_border.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()
