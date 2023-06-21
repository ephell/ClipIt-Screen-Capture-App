from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Ruler(QGraphicsItem):
    
    def __init__(self, scene, view, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.view = view
        self.initial_x = self.scene.ruler_x
        self.initial_y = self.scene.ruler_y
        self.setPos(self.initial_x, self.initial_y)
        self.media_duration = media_duration
        self.initial_width = self.scene.width() - self.pos().x() * 2
        self.initial_height = 10
        self.width = self.initial_width
        self.height = self.initial_height
        self.tick_amount = 10

    """Override"""
    def paint(self, painter, option, widget):
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        tick_positions = self.__get_tick_positions(self.width, self.tick_amount)
        for tick_pos in tick_positions:
            # Draw the tick mark
            painter.drawLine(tick_pos, 0, tick_pos, self.height)
            # Draw the tick label
            text = self.__generate_tick_label(tick_pos)
            text_rect = painter.fontMetrics().boundingRect(text)
            text_width = text_rect.width()
            text_height = text_rect.height()
            text_x = tick_pos - text_width // 2
            text_y = self.height + text_height
            painter.drawText(text_x, text_y, text)

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    @Slot()
    def on_view_resize(self):
        new_scene_width = self.__find_proportionate_scene_width(
            self.view.width(),
            self.view.minimumWidth(),
            self.view.maximumWidth(),
        )
        self.view.resize_scene(new_scene_width)
        self.width = new_scene_width - self.__get_x_padding()
        self.update()

    def __find_proportionate_scene_width(
            self, 
            view_width, 
            min_view_width,
            max_view_width
        ):
        max_interval_time = self.media_duration / self.tick_amount
        for width in range(view_width, min_view_width - 1, -1):
            max_ruler_width = width - self.__get_x_padding()
            time_per_interval = self.__get_time_per_interval(max_ruler_width)
            if time_per_interval == max_interval_time:
                return width
        else:
            # In case there's no suitable width between the last 
            # proportional width and the minimum width.
            for width in range(min_view_width, max_view_width + 1):
                max_ruler_width = width - self.__get_x_padding()
                time_per_interval = self.__get_time_per_interval(max_ruler_width)
                if time_per_interval == max_interval_time:
                    return width

    def __generate_tick_label(self, tick_pos):
        time_value = tick_pos * self.__get_one_pixel_time_value(
            self.media_duration,
            self.width
        )
        milliseconds = int(time_value)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    
    def __get_tick_positions(self, width, tick_amount):
        return [
            int(i * self.__get_pixels_per_interval(width, tick_amount)) 
            for i in range(int(tick_amount) + 1)
        ]

    def __get_pixels_per_interval(self, width, tick_amount):
        return int(width / tick_amount)
    
    def __get_one_pixel_time_value(self, media_duration, width):
        return media_duration / width

    def __get_time_per_interval(self, width):
        pixel_time_value = self.__get_one_pixel_time_value(self.media_duration, width)
        pixels_per_interval = self.__get_pixels_per_interval(width, self.tick_amount)
        return pixel_time_value * pixels_per_interval

    def __get_x_padding(self):
        return self.scene.ruler_x * 2
