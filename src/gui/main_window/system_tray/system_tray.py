from PySide6.QtCore import Slot, Signal, Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QMenu, QSystemTrayIcon, QMessageBox

from src.utilities.py_installer import get_absolute_path


class SystemTray(QSystemTrayIcon):

    request_exit_signal = Signal()

    __TRAY_ICON_PATH = get_absolute_path("src\\gui\\application\\logo.svg")
    # Action texts
    __ACTION_START_RECORDING_TEXT = "Start Recording"
    __ACTION_STOP_RECORDING_TEXT = "Stop Recording"
    __ACTION_SCREENSHOT_TEXT = "Take A Screenshot"
    __ACTION_OPEN_EDITOR_TEXT = "Open Editor"
    __ACTION_OPEN_CAPTURE_FOLDER_TEXT = "Open Capture Folder"
    __ACTION_SETTINGS_TEXT = "Settings"
    __ACTION_EXIT_TEXT = "Exit"
    # Action icon paths
    __ACTION_START_RECORDING_ICON_PATH = get_absolute_path("src\\gui\\main_window\\system_tray\\icons\\action_start_stop_recording\\1x\\baseline_videocam_white_24dp.png")
    __ACTION_STOP_RECORDING_ICON_PATH = get_absolute_path("src\\gui\\main_window\\system_tray\\icons\\action_start_stop_recording\\1x\\baseline_videocam_off_white_24dp.png")
    __ACTION_SCREENSHOT_ICON_PATH = get_absolute_path("src\\gui\\main_window\\system_tray\\icons\\action_screenshot\\1x\\baseline_camera_alt_white_24dp.png")
    __ACTION_OPEN_EDITOR_ICON_PATH = get_absolute_path("src\\gui\\main_window\\system_tray\\icons\\action_open_editor\\1x\\baseline_movie_edit_white_24dp.png")
    __ACTION_OPEN_CAPTURE_FOLDER_ICON_PATH = get_absolute_path("src\\gui\\main_window\\system_tray\\icons\\action_open_capture_folder\\1x\\baseline_folder_white_24dp.png")
    __ACTION_SETTINGS_ICON_PATH = get_absolute_path("src\\gui\\main_window\\system_tray\\icons\\action_settings\\1x\\baseline_settings_white_24dp.png")
    __ACTION_EXIT_ICON_PATH = get_absolute_path("src\\gui\\main_window\\system_tray\\icons\\action_exit\\1x\\baseline_close_white_24dp.png")

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setIcon(QIcon(self.__TRAY_ICON_PATH))
        self.__tray_menu = QMenu()
        self.__initialize_actions()
        self.__add_actions_to_tray_menu()
        self.__set_action_icons()
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

    def __add_actions_to_tray_menu(self):
        self.__tray_menu.addAction(self.action_start_stop_recording)
        self.__tray_menu.addAction(self.action_screenshot)
        self.__tray_menu.addAction(self.action_open_editor)
        self.__tray_menu.addAction(self.action_open_capture_folder)
        self.__tray_menu.addAction(self.action_settings)
        self.__tray_menu.addSeparator()
        self.__tray_menu.addAction(self.action_exit)

    def __set_action_icons(self):
        self.action_start_stop_recording.setIcon(QIcon(self.__ACTION_START_RECORDING_ICON_PATH))
        self.action_screenshot.setIcon(QIcon(self.__ACTION_SCREENSHOT_ICON_PATH))
        self.action_open_editor.setIcon(QIcon(self.__ACTION_OPEN_EDITOR_ICON_PATH))
        self.action_open_capture_folder.setIcon(QIcon(self.__ACTION_OPEN_CAPTURE_FOLDER_ICON_PATH))
        self.action_settings.setIcon(QIcon(self.__ACTION_SETTINGS_ICON_PATH))
        self.action_exit.setIcon(QIcon(self.__ACTION_EXIT_ICON_PATH))

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
        self.action_start_stop_recording.setIcon(QIcon(self.__ACTION_STOP_RECORDING_ICON_PATH))

    @Slot()
    def on_recording_stopped(self):
        self.action_start_stop_recording.setText(self.__ACTION_START_RECORDING_TEXT)
        self.action_start_stop_recording.setIcon(QIcon(self.__ACTION_START_RECORDING_ICON_PATH))

    @Slot()
    def __on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.main_window.show()
            self.main_window.setWindowState(self.main_window.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
            self.main_window.activateWindow()
