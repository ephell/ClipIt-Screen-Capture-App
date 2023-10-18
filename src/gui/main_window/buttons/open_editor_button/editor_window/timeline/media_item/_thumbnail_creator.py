import numpy as np
from moviepy.editor import VideoFileClip
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor


class ThumbnailCreator:

    def __init__(self, media_item):
        self.media_item = media_item
        self.__scene = media_item.scene
        self.__frames_to_extract = 5
        self.__initial_thumbnail_width = media_item.initial_width
        self.__initial_scene_width = self.__scene.width()
        self.__previous_scene_width = self.__initial_scene_width
        self.__filler_color = QColor(Qt.gray)
        self.__q_pixmaps = self.__get_q_pixmaps()
        self.__current_thumbnail = self.__create_max_size_thumbnail()

    def create_thumbnail(self):
        if self.__previous_scene_width != self.__scene.width():
            self.__previous_scene_width = self.__scene.width()
            self.__current_thumbnail = self.__create_max_size_thumbnail()
        return self.__crop_to_fit(self.__current_thumbnail)

    def __create_max_size_thumbnail(self):
        """Creates a QPixmap image object that can fully cover the MediaItem."""
        q_pixmaps = self.__draw_fillers_on_q_pixmaps(self.__q_pixmaps)
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
                self.__q_pixmaps[0].height()
            )
        )

    def __draw_fillers_on_q_pixmaps(self, q_pixmaps: list[QPixmap]):
        q_pixmaps_with_fillers = []
        for q_pixmap in q_pixmaps:
            q_pixmap_with_filler = QPixmap(
                q_pixmap.width() + self.__calculate_filler_width(),
                q_pixmap.height()
            )
            painter = QPainter(q_pixmap_with_filler)
            q_pixmap_with_filler.fill(self.__filler_color)
            painter.drawPixmap(0, 0, q_pixmap)
            q_pixmaps_with_fillers.append(q_pixmap_with_filler)
            painter.end()
        return q_pixmaps_with_fillers

    def __get_q_pixmaps(self):
        video_frames = self.__extract_video_frames(self.media_item.media_player.file_path)
        q_pixmaps = self.__convert_frames_to_q_pixmaps(video_frames)
        return self.__scale_q_pixmaps(q_pixmaps)

    def __extract_video_frames(self, video_file_path: str):
        video_clip = VideoFileClip(video_file_path)
        frames = []
        for timestamp in self.__calculate_frame_extraction_timestamps():
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
                    self.media_item.boundingRect().width() / len(q_pixmaps),
                    self.media_item.boundingRect().height(),
                    mode=Qt.FastTransformation
                )
            )
        return scaled_q_pixmaps

    def __calculate_frame_extraction_timestamps(self):
        interval = int(self.media_item.media_duration / self.__frames_to_extract)
        return [i * interval for i in range(self.__frames_to_extract)]

    def __calculate_filler_width(self):
        width_diff = self.media_item.get_max_possible_width() - self.__initial_thumbnail_width
        return max(0, width_diff / len(self.__q_pixmaps))
