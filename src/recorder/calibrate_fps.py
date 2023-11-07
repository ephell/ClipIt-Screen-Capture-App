import mss
import threading
from time import sleep
import queue

from PySide6.QtCore import QObject

from src.recorder.recorder import Recorder


class SampleGetter(QObject, threading.Thread):

    def __init__(self):
        super().__init__()
        self.fps = 30
        self.monitor = 1
    
    def run(self):
        self.full_screen_recorder_stop_event = threading.Event()
        self.frames_captured_each_second_queue = queue.Queue()
        self.full_screen_recorder = Recorder(
            record_video=True,
            record_loopback=True,
            region=self.__get_max_monitor_area(),
            monitor=self.monitor,
            fps=self.fps,
            stop_event=self.full_screen_recorder_stop_event,
            generate_final_file=False,
            frames_captured_each_second_queue=self.frames_captured_each_second_queue
        )
        self.full_screen_recorder.start()
        sleep(5)
        self.full_screen_recorder_stop_event.set()
        print(f"Frame info: {self.frames_captured_each_second_queue.get()}")
        self.full_screen_recorder.join()
        print("Sample getter stopped")

    def __get_max_monitor_area(self):
        mon = mss.mss().monitors[1]
        return (mon["left"], mon["top"], mon["width"], mon["height"])
    
    def __get_max_area_half_height(self):
        mon = mss.mss().monitors[1]
        return (mon["left"], mon["top"], mon["width"], mon["height"] // 2)
    
    def __get_max_area_half_width(self):
        mon = mss.mss().monitors[1]
        return (mon["left"], mon["top"], mon["width"] // 2, mon["height"])
    
    def __get_max_area_quarter(self):
        mon = mss.mss().monitors[1]
        return (mon["left"], mon["top"], mon["width"] // 2, mon["height"] // 2)

