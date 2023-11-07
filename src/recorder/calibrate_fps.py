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
        self.sample_data = {}
        self.sample_sleep_time = 5
    
    def run(self):
        self.__get_sample(self.__get_max_monitor_area())
        print(f"Max area done, sample data: {self.sample_data}")
        self.__get_sample(self.__get_max_area_half_height())
        print(f"Half height done, sample data: {self.sample_data}")
        self.__get_sample(self.__get_max_area_half_width())
        print(f"Half width done, sample data: {self.sample_data}")
        self.__get_sample(self.__get_max_area_quarter())
        print(f"Quarter done, sample data: {self.sample_data}")

    def __get_sample(self, area):
        stop_event = threading.Event()
        fps_counts_queue = queue.Queue()
        recorder = Recorder(
            record_video=True,
            record_loopback=True,
            region=area,
            monitor=self.monitor,
            fps=self.fps,
            stop_event=stop_event,
            generate_final_file=False,
            frames_captured_each_second_queue=fps_counts_queue
        )
        recorder.start()
        sleep(self.sample_sleep_time)
        stop_event.set()
        frame_counts = fps_counts_queue.get()
        recorder.join()
        self.sample_data.update({area: frame_counts})
        
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
