from PySide6.QtCore import Slot, Signal, Qt, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMenu, QSystemTrayIcon, QMessageBox


class SystemTray(QSystemTrayIcon):

    request_exit_signal = Signal()

    __ICON_PATH = "src/gui/application/logo.svg"
    __ACTION_START_RECORDING_TEXT = "Start Recording"
    __ACTION_STOP_RECORDING_TEXT = "Stop Recording"
    __ACTION_SCREENSHOT_TEXT = "Take A Screenshot"
    __ACTION_OPEN_EDITOR_TEXT = "Open Editor"
    __ACTION_OPEN_CAPTURE_FOLDER_TEXT = "Open Capture Folder"
    __ACTION_SETTINGS_TEXT = "Settings"
    __ACTION_EXIT_TEXT = "Exit"

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setIcon(QIcon(self.__ICON_PATH))
        self.__tray_menu = QMenu()
        self.__initialize_actions()
        self.__add_actions_to_tray()
        self.setContextMenu(self.__tray_menu)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.activated.connect(self.__on_tray_icon_activated)
        self.action_exit.triggered.connect(self.__request_exit)

    def __initialize_actions(self):
        self.action_start_stop_recording = QAction(self.__ACTION_START_RECORDING_TEXT)
        self.action_screenshot = QAction(self.__ACTION_SCREENSHOT_TEXT)
        self.action_open_editor = QAction(self.__ACTION_OPEN_EDITOR_TEXT)
        self.action_open_capture_folder = QAction(self.__ACTION_OPEN_CAPTURE_FOLDER_TEXT)
        self.action_settings = QAction(self.__ACTION_SETTINGS_TEXT)
        self.action_exit = QAction(self.__ACTION_EXIT_TEXT)

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

    @Slot()
    def on_recording_started(self):
        self.action_start_stop_recording.setText(self.__ACTION_STOP_RECORDING_TEXT)

    @Slot()
    def on_recording_stopped(self):
        self.action_start_stop_recording.setText(self.__ACTION_START_RECORDING_TEXT)

    @Slot()
    def __on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.main_window.show()
            self.main_window.setWindowState(self.main_window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
            self.main_window.activateWindow()
