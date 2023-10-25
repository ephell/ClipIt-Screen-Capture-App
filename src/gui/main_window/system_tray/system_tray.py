from PySide6.QtWidgets import QMenu, QSystemTrayIcon
from PySide6.QtGui import QIcon, QAction


class SystemTray(QSystemTrayIcon):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon("testicon.png"))
        self.__tray_menu = QMenu()
        self.__initialize_actions()
        self.__add_actions_to_tray()
        self.setContextMenu(self.__tray_menu)

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
