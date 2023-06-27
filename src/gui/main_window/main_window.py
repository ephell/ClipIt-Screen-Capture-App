from typing import Optional
from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from .buttons.select_area_button.main_logic import SelectAreaButtonLogic
from recorder.recorder import Recorder
from .Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("ClipIt")
        self.app = app

        self._select_area_button_logic = SelectAreaButtonLogic()
        self.select_area_button.clicked.connect(
            self._select_area_button_logic.on_select_area_clicked
        )

        self.start_recording_button.clicked.connect(self.__on_start_clicked)
        self.stop_event = None
        self.is_recording = False

        self.stop_recording_button.clicked.connect(self.__on_stop_clicked)


    """Override"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self._select_area_button_logic.area_selector is not None:
                self._select_area_button_logic.area_selector.close()

    def __on_stop_clicked(self):
        if self._select_area_button_logic.recording_area_border is not None:
            self._select_area_button_logic.recording_area_border.destroy()
            self._select_area_button_logic.recording_area_border = None
            self.stop_event.set()
            self.stop_event = None
            self.is_recording = False

    def __on_start_clicked(self):
        if not self.is_recording:
            if self._select_area_button_logic.recording_area_border is not None:
                self.is_recording = True
                self.stop_event = mp.Event()
                recorder = Recorder(
                    record_video=True,
                    record_loopback=True,
                    record_microphone=True,
                    stop_event=self.stop_event,
                    region=[*self._select_area_button_logic.get_area_coords()],
                    monitor=self._select_area_button_logic.get_monitor(),
                    fps=30
                )
                recorder.start()
        else:
            log.error("Recording process is already running.")
