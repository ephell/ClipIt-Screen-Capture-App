# from collections import deque
import queue
from time import sleep

import numpy as np
from moviepy.editor import VideoFileClip
from PySide6.QtCore import Qt, QRect, QThread, Signal, Slot, QTimer
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QBrush


class ThumbnailCreator:

    def __init__(self, media_item):
        self.media_item = media_item
        self.__scaled_q_pixmap_w, self.__scaled_q_pixmap_h = self.__get_scale_dimensions()
        self.__filler_color = QColor(Qt.gray)

        self.__max_sized_thumbnail = None
        self.__q_pixmaps = {}

        self.__extraction_queue = queue.Queue()
        self.__extractor = _QPixmapsExtractor(
            self.media_item,
            self.__scaled_q_pixmap_w,
            self.__scaled_q_pixmap_h,
            self.__extraction_queue
        )
        self.__extractor.extraction_finished_signal.connect(
            self.__on_extraction_finished
        )
        self.__extractor.start()

        self.listas = []

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_timer_expired)
    
    @Slot()
    def on_timer_expired(self):
        frames_to_extract = self.__calculate_amt_of_frames_to_extract()
        if frames_to_extract not in self.__q_pixmaps.keys():
            if frames_to_extract not in self.listas:
                self.listas.append(frames_to_extract)
                self.__extraction_queue.put(frames_to_extract)

    @Slot()
    def __on_extraction_finished(self, amt_extracted, q_pixmaps_list):
        self.__q_pixmaps.update({amt_extracted: q_pixmaps_list})
        self.__max_sized_thumbnail = self.create_thumbnail(amt_extracted)
        self.media_item.update()

    def get_thumbnail(self):
        if self.__max_sized_thumbnail is None:
            return QBrush(self.__filler_color)
        
        amt_of_frames = self.__calculate_amt_of_frames_to_extract()

        if self.__q_pixmaps.get(amt_of_frames) is None:
            amt_of_frames = self.__find_valid_key(amt_of_frames)
            return self.__crop_to_fit(self.create_thumbnail(amt_of_frames))
        else:
            return self.__crop_to_fit(self.create_thumbnail(amt_of_frames))

    def __find_valid_key(self, amt_of_frames):
        keys = self.__q_pixmaps.keys()
        closest_lower = None
        for key in keys:
            if key <= amt_of_frames and (closest_lower is None or key > closest_lower):
                closest_lower = key
        return closest_lower

    def create_thumbnail(self, amt_of_frames):
        q_pixmaps = self.__q_pixmaps.get(amt_of_frames)
        q_pixmaps_with_fillers = self.__add_filler_to_each_q_pixmap(q_pixmaps)
        q_pixmaps_combined = self.__combine_q_pixmaps(q_pixmaps_with_fillers)
        return q_pixmaps_combined

    def on_view_resize(self):
        """Not a slot. Called in MediaItem."""
        self.timer.start(250)






    def __calculate_amt_of_frames_to_extract(self):
        max_width = self.media_item.get_max_possible_width()
        return int(max_width / self.__scaled_q_pixmap_w)


    def __combine_q_pixmaps(self, q_pixmaps: list[QPixmap]):
        """Creates a QPixmap image object that can fully cover the MediaItem."""
        thumbnail_width = q_pixmaps[0].width() * len(q_pixmaps)
        thumbnail_height = q_pixmaps[0].height()
        thumbnail_pixmap = QPixmap(thumbnail_width, thumbnail_height)
        painter = QPainter(thumbnail_pixmap)
        for i, q_pixmap in enumerate(q_pixmaps):
            painter.drawPixmap(i * q_pixmap.width(), 0, q_pixmap)
        painter.end()
        return thumbnail_pixmap

    def __crop_to_fit(self, max_size_thumbnail: QPixmap):
        return max_size_thumbnail.copy(
            QRect(
                self.media_item.scenePos().x() - self.media_item.initial_x,
                0,
                self.media_item.right_handle.scenePos().x() - self.media_item.scenePos().x(),
                # self.__q_pixmaps[0].height()
                self.media_item.initial_height
            )
        )

    def __add_filler_to_each_q_pixmap(self, q_pixmaps: list[QPixmap]):
        q_pixmaps_with_fillers = []
        for q_pixmap in q_pixmaps:
            q_pixmap_with_filler = QPixmap(
                q_pixmap.width() + self.__calculate_filler_width(len(q_pixmaps)),
                q_pixmap.height()
            )
            painter = QPainter(q_pixmap_with_filler)
            q_pixmap_with_filler.fill(self.__filler_color)
            painter.drawPixmap(0, 0, q_pixmap)
            q_pixmaps_with_fillers.append(q_pixmap_with_filler)
            painter.end()
        return q_pixmaps_with_fillers

    def __calculate_filler_width(self, frame_amount):
        max_possible_thumbnail_width = frame_amount * self.__scaled_q_pixmap_w
        width_diff = self.media_item.get_max_possible_width() - max_possible_thumbnail_width
        return max(0, width_diff / frame_amount)



    def __get_scale_dimensions(self):
        """
        Extracts the first frame from the video, scales it to the 
        height of the MediaItem and returns the scaled frame's dimensions.
        """
        # Extract video frame (np.ndarray)
        frame = VideoFileClip(self.media_item.media_player.file_path).get_frame(0)
        # Convert frame to QPixmap
        frame_height, frame_width, _ = frame.shape
        bytes_per_line = 3 * frame_width
        q_image = QImage(
            frame.data, 
            frame_width, 
            frame_height, 
            bytes_per_line, 
            QImage.Format_RGB888
        )
        q_pixmap = QPixmap.fromImage(q_image)
        # Scale QPixmap to height of MediaItem
        scaled_q_pixmap = q_pixmap.scaledToHeight(
            self.media_item.boundingRect().height(),
            mode=Qt.FastTransformation
        )
        return scaled_q_pixmap.width(), scaled_q_pixmap.height()








class _QPixmapsExtractor(QThread):

    extraction_finished_signal = Signal(int, list)

    def __init__(
            self,
            media_item,
            scale_to_w,
            scale_to_h,
            extraction_queue: queue.Queue,
        ):
        super().__init__()
        self.media_item = media_item
        self.extraction_queue = extraction_queue
        self.video_duration = self.media_item.media_duration
        self.video_file_path = self.media_item.media_player.file_path
        self.scale_to_w = scale_to_w
        self.scale_to_h = scale_to_h

    def run(self):
        while True:
            if not self.extraction_queue.empty():

                amt_to_extract = self.extraction_queue.get()

                print(f"Extracting {amt_to_extract} frames")

                timestamps = self.__calculate_extraction_timestamps(amt_to_extract)

                frames = self.__extract_video_frames(self.video_file_path, timestamps)
                q_pixmaps = self.__convert_frames_to_q_pixmaps(frames)
                scaled_q_pixmaps = self.__scale_q_pixmaps(q_pixmaps)

                self.extraction_finished_signal.emit(amt_to_extract, scaled_q_pixmaps)

                print("Finished extracting and emitting")

            else:
                sleep(1)

    def __calculate_extraction_timestamps(self, frame_amount):
        interval = int(self.video_duration / frame_amount)
        return [i * interval for i in range(frame_amount)]

    def __extract_video_frames(self, video_file_path, extraction_timestamps):
        video_clip = VideoFileClip(video_file_path)
        frames = []
        for timestamp in extraction_timestamps:
            frame = video_clip.get_frame(timestamp / 1000.0)
            frames.append(frame)
        return frames

    def __convert_frames_to_q_pixmaps(self, video_frames: list[np.ndarray]):
        frame_height, frame_width, _ = video_frames[0].shape
        bytes_per_line = 3 * frame_width
        q_pixmaps = []
        for frame in video_frames:
            q_image = QImage(
                frame.data, 
                frame_width, 
                frame_height, 
                bytes_per_line, 
                QImage.Format_RGB888
            )
            q_pixmaps.append(QPixmap.fromImage(q_image))
        return q_pixmaps

    def __scale_q_pixmaps(self, q_pixmaps: list[QPixmap]):
        scaled_q_pixmaps = []
        for q_pixmap in q_pixmaps:
            scaled_q_pixmaps.append(
                q_pixmap.scaled(
                    self.scale_to_w,
                    self.scale_to_h,
                    mode=Qt.FastTransformation
                )
            )
        return scaled_q_pixmaps
