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

from region_selector import RegionSelector


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("My App")
        self.app = app
        self.region_selector = None
        self.region_top_left_x = None
        self.region_top_left_y = None
        self.region_bottom_right_x = None
        self.region_bottom_right_y = None


        record_button = QPushButton()
        record_button.setText("Select Area")
        record_button.clicked.connect(self.__on_record_button_clicked)

        self.region_label = QLabel()
        self.region_label.setText(f"No region selected.")

        layout = QVBoxLayout()
        layout.addWidget(record_button)
        layout.addWidget(self.region_label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def __on_record_button_clicked(self):
        self.region_selector = RegionSelector(
            self.__on_rectangle_coordinates_received
        )
        self.region_selector.show()

    def __on_rectangle_coordinates_received(self, x0, y0, x1, y1):
        """Get the coordinates of the region to record (callback)."""
        self.region_top_left_x = x0
        self.region_top_left_y = y0
        self.region_bottom_right_x = x1
        self.region_bottom_right_y = y1
        self.region_label.setText(
            f"Region selected: ({x0}, {y0}) ({x1}, {y1})"
        )
        self.region_selector.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.region_selector is not None:
                self.region_selector.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()
