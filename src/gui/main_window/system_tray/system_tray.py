from PySide6.QtCore import Slot, Signal
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMenu, QSystemTrayIcon, QMessageBox


class SystemTray(QSystemTrayIcon):

    request_exit_signal = Signal()

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setIcon(QIcon("testicon.png"))
        self.__tray_menu = QMenu()
        self.__initialize_actions()
        self.__add_actions_to_tray()
        self.setContextMenu(self.__tray_menu)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.action_exit.triggered.connect(self.__request_exit)

    def __initialize_actions(self):
        self.action_start_stop_recording = QAction("Start/Stop Recording")
        self.action_screenshot = QAction("Take A Screenshot")
        self.action_open_editor = QAction("Open Editor")
        self.action_open_capture_folder = QAction("Open Capture Folder")
        self.action_settings = QAction("Settings")
        self.action_exit = QAction("Exit")

    def __add_actions_to_tray(self):
        self.__tray_menu.addAction(self.action_start_stop_recording)
        self.__tray_menu.addAction(self.action_screenshot)
        self.__tray_menu.addAction(self.action_open_editor)
        self.__tray_menu.addAction(self.action_open_capture_folder)
        self.__tray_menu.addAction(self.action_settings)
        self.__tray_menu.addSeparator()
        self.__tray_menu.addAction(self.action_exit)

    def __request_exit(self):
        msg_box = QMessageBox.question(
            self.main_window,
            "Exit",
            "Are you sure you want to exit the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if msg_box == QMessageBox.Yes:
            self.request_exit_signal.emit()

    @Slot()
    def on_ready_to_exit(self):
        self.main_window.app.quit()
