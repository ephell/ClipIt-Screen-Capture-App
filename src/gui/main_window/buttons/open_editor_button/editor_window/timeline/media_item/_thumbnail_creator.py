import queue
import threading

from moviepy.editor import VideoFileClip
import numpy as np
from PySide6.QtCore import Qt, QRect, Signal, Slot, QTimer, QObject
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QBrush, QPen


class ThumbnailCreator:

    def __init__(self, media_item):
        self.media_item = media_item
        self.__q_pixmaps = {}
        self.__q_pixmap_w, self.__q_pixmap_h = self.__get_scaled_q_pixmap_dimensions()
        self.__resize_event_timer = QTimer()
        self.__resize_event_timer.setSingleShot(True)
        self.__resize_event_timer.timeout.connect(self.__on_resize_event_timer_expired)
        self.__resize_event_timer_interval = 250
        self.__extractor = _QPixmapsExtractor(
            self.media_item,
            self.__q_pixmap_w,
            self.__q_pixmap_h
        )
        self.__extractor.finished_signal.connect(self.__on_extraction_finished)
        self.__extractor.start()
        self.__filler_color = QColor(135, 135, 135)
        self.__filler_line_color = QColor(255, 255, 255)
        self.__filler_line_width = 2

    def get_thumbnail(self):
        if len(self.__q_pixmaps) == 0:
            return QBrush(self.__filler_color)
        
        frame_amount = self.__calculate_required_frame_amount()
        if not self.__is_key_valid(frame_amount):
            return self.__crop_to_fit(
                        self.__create_thumbnail(
                            self.__get_closest_valid_key(frame_amount)
                        )
                    )
        return self.__crop_to_fit(self.__create_thumbnail(frame_amount))

    def kill_extraction_thread(self):
        self.__extractor.kill()

    def __calculate_required_frame_amount(self):
        return max(
            1,
            int(self.media_item.get_max_possible_width() / self.__q_pixmap_w)
        )

    def __is_key_valid(self, key):
        return key in self.__q_pixmaps.keys()

    def __get_closest_valid_key(self, invalid_key):
        closest_lower = None
        for key in self.__q_pixmaps.keys():
            if key <= invalid_key and (closest_lower is None or key > closest_lower):
                closest_lower = key
        return closest_lower

    def __crop_to_fit(self, max_size_thumbnail: QPixmap):
        return max_size_thumbnail.copy(
            QRect(
                self.media_item.scenePos().x() - self.media_item.initial_x,
                0,
                self.media_item.boundingRect().width(),
                self.media_item.boundingRect().height()
            )
        )

    def __create_thumbnail(self, frame_amount):
        q_pixmaps = self.__q_pixmaps.get(frame_amount)
        q_pixmaps_with_fillers = self.__add_filler_to_each_q_pixmap(q_pixmaps)
        thumbnail = self.__combine_q_pixmaps(q_pixmaps_with_fillers)
        if not thumbnail.width() == self.media_item.get_max_possible_width():
            thumbnail = self.__add_filler_to_end(thumbnail)
        return thumbnail

    def __add_filler_to_each_q_pixmap(self, q_pixmaps: list[QPixmap]):
        q_pixmaps_with_fillers = []
        for q_pixmap in q_pixmaps:
            q_pixmap_with_filler = QPixmap(
                q_pixmap.width() + self.__calculate_filler_width(len(q_pixmaps)),
                q_pixmap.height()
            )
            painter = QPainter(q_pixmap_with_filler)
            
            painter.fillRect(
                0, 0, 
                q_pixmap_with_filler.width(), q_pixmap_with_filler.height(), 
                self.__filler_color
            )
            
            pen = QPen()
            pen.setColor(self.__filler_line_color)
            pen.setWidth(self.__filler_line_width)
            painter.setPen(pen)
            painter.drawLine(
                0, q_pixmap.height() // 2, 
                q_pixmap_with_filler.width(), q_pixmap.height() // 2
            )
            
            painter.drawPixmap(0, 0, q_pixmap)
            q_pixmaps_with_fillers.append(q_pixmap_with_filler)
            painter.end()
        return q_pixmaps_with_fillers

    def __combine_q_pixmaps(self, q_pixmaps: list[QPixmap]):
        final_q_pixmap = QPixmap(
            q_pixmaps[0].width() * len(q_pixmaps),
            q_pixmaps[0].height()
        )
        painter = QPainter(final_q_pixmap)
        for i, q_pixmap in enumerate(q_pixmaps):
            painter.drawPixmap(i * q_pixmap.width(), 0, q_pixmap)
        painter.end()
        return final_q_pixmap

    def __add_filler_to_end(self, thumbnail: QPixmap):
        """
        Adds a filler to the end of the thumbnail to fully cover the MediaItem.

        Typically, '__add_filler_to_each_q_pixmap()' creates QPixmaps with 
        equal widths that when combined can fully cover the MediaItem. However, 
        in some cases, these combined QPixmaps fall slightly short of the 
        MediaItem's maximum width. This discrepancy arises from the way each 
        QPixmap's width is determined during creation. The method 
        '__calculate_filler_width()' may return a float value, but the 
        QPixmap() constructor only accepts integer values for width and height, 
        causing the decimal portion to be truncated. This results in each 
        QPixmap being slightly shorter than needed, ultimately causing the 
        combined QPixmaps to be narrower than the MediaItem's maximum width. 
        In such situations, calling this function becomes necessary to fill 
        the remaining space.

        """
        extended_thumbnail = QPixmap(
            thumbnail.width() + self.media_item.get_max_possible_width() - thumbnail.width(),
            thumbnail.height()
        )
        painter = QPainter(extended_thumbnail)
        painter.fillRect(
            0, 
            0, 
            extended_thumbnail.width(), 
            extended_thumbnail.height(), 
            self.__filler_color
        )

        pen = QPen()
        pen.setColor(self.__filler_line_color)
        pen.setWidth(self.__filler_line_width)
        painter.setPen(pen)
        painter.drawLine(
            0, 
            extended_thumbnail.height() // 2,
            extended_thumbnail.width(), 
            extended_thumbnail.height() // 2
        )

        painter.drawPixmap(0, 0, thumbnail)
        painter.end()
        return extended_thumbnail

    def __calculate_filler_width(self, frame_amount):
        max_possible_thumbnail_width = frame_amount * self.__q_pixmap_w
        width_diff = self.media_item.get_max_possible_width() - max_possible_thumbnail_width
        return max(0, width_diff / frame_amount)

    def __get_scaled_q_pixmap_dimensions(self):
        """
        Extracts the first frame from the video, scales it to the 
        height of the MediaItem and returns the scaled frame's dimensions.
        """
        with VideoFileClip(self.media_item.media_player.file_path) as video_clip:
            frame = video_clip.get_frame(0)
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
            scaled_q_pixmap = q_pixmap.scaledToHeight(
                self.media_item.boundingRect().height(),
                mode=Qt.FastTransformation
            )
            # This condition triggers when 'media_item.boundingRect().height()' is 
            # lower than the height of the video. When that happens only one
            # frame is extracted and used as a thumbnail.
            if frame_width < scaled_q_pixmap.width():
                return frame_width, scaled_q_pixmap.height()
            return scaled_q_pixmap.width(), scaled_q_pixmap.height()

    @Slot()
    def __on_resize_event_timer_expired(self):
        self.__extractor.put_in_queue(self.__calculate_required_frame_amount())

    @Slot()
    def __on_extraction_finished(self, frame_amount, q_pixmaps_list):
        self.__q_pixmaps.update({frame_amount: q_pixmaps_list})
        self.media_item.update()

    def on_view_resize(self):
        """Not a slot. Called in MediaItem."""
        self.__resize_event_timer.start(self.__resize_event_timer_interval)


class _QPixmapsExtractor(QObject, threading.Thread):

    finished_signal = Signal(int, list)

    def __init__(
            self,
            media_item,
            scale_q_pixmap_to_w,
            scale_q_pixmap_to_h,
        ):
        super().__init__()
        self.setDaemon(True)
        self.__media_item = media_item
        self.__scale_q_pixmap_to_w = scale_q_pixmap_to_w
        self.__scale_q_pixmap_to_h = scale_q_pixmap_to_h
        self.__video_duration = self.__media_item.media_duration
        self.__video_file_path = self.__media_item.media_player.file_path
        self.__frame_amount_queue = queue.Queue()
        self.__work_available_flag = threading.Event()
        self.__extracted_frame_amounts = []
        self.is_kill_flag_set = False

    def run(self):
        while not self.is_kill_flag_set:
            self.__work_available_flag.wait()
            if not self.__frame_amount_queue.empty():
                frame_amount = self.__frame_amount_queue.get()
                timestamps = self.__calculate_extraction_timestamps(frame_amount)
                frames = self.__extract_video_frames(self.__video_file_path, timestamps)
                q_pixmaps = self.__convert_frames_to_q_pixmaps(frames)
                scaled_q_pixmaps = self.__scale_q_pixmaps(q_pixmaps)
                self.finished_signal.emit(frame_amount, scaled_q_pixmaps)
            else:
                self.__work_available_flag.clear()

    def put_in_queue(self, frame_amount):
        if frame_amount not in self.__extracted_frame_amounts:
            self.__extracted_frame_amounts.append(frame_amount)
            self.__frame_amount_queue.put(frame_amount)
            if not self.__work_available_flag.is_set():
                self.__work_available_flag.set()

    def kill(self):
        self.is_kill_flag_set = True
        self.__work_available_flag.set()

    def __calculate_extraction_timestamps(self, frame_amount):
        interval = int(self.__video_duration / frame_amount)
        return [i * interval for i in range(frame_amount)]

    def __extract_video_frames(self, video_file_path, extraction_timestamps):
        with VideoFileClip(video_file_path) as video_clip:        
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
                    self.__scale_q_pixmap_to_w,
                    self.__scale_q_pixmap_to_h,
                    mode=Qt.FastTransformation
                )
            )
        return scaled_q_pixmaps
