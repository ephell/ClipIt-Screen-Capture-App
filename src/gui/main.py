import sys

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
        self.screenshot_holder = RegionSelector()
        self.screenshot_holder.show()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()
