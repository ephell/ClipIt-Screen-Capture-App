import mss
import queue
import threading
from time import sleep

from PySide6.QtCore import QObject

from src.recorder.recorder import Recorder
from src.settings.settings import Settings


class AvgFPSPerAreaGetter(QObject, threading.Thread):

    def __init__(self):
        super().__init__()
        self.fps = 30
        self.monitor = 1
        self.avg_fps_per_area = {}
        self.sample_sleep_time = 5
    
    def run(self):
        self.__get_avg_area_fps(self.__get_max_area())
        self.__get_avg_area_fps(self.__get_max_area_half())
        self.__get_avg_area_fps(self.__get_max_area_quarter())
        Settings.set_video_recorder_setting("avg_fps_per_area", f"{self.avg_fps_per_area}")

    def __get_avg_area_fps(self, area):
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
            video_fps_counts_queue=fps_counts_queue
        )
        recorder.start()
        sleep(self.sample_sleep_time)
        stop_event.set()
        self.avg_fps_per_area.update({area: self.__calculate_avg(fps_counts_queue.get())})
        recorder.join()
        
    def __get_max_area(self):
        mon = mss.mss().monitors[1]
        return (mon["left"], mon["top"], mon["width"], mon["height"])
    
    def __get_max_area_half(self):
        mon = mss.mss().monitors[1]
        return (mon["left"], mon["top"], mon["width"] // 2, mon["height"])
    
    def __get_max_area_quarter(self):
        mon = mss.mss().monitors[1]
        return (mon["left"], mon["top"], mon["width"] // 2, mon["height"] // 2)

    def __calculate_avg(self, frame_counts):
        return int(sum(frame_counts) / len(frame_counts))
