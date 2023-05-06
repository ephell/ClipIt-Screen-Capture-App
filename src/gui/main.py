import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
)

from region_selector import RegionSelector


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.region_selector = None
        self.setWindowTitle("My App")

        record_button = QPushButton()
        record_button.setText("Record")
        record_button.clicked.connect(self.__on_record_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(record_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def __on_record_button_clicked(self):
        self.region_selector = RegionSelector()
        self.region_selector.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.region_selector is not None:
                self.region_selector.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()
