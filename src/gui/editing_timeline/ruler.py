from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Ruler(QGraphicsWidget):
    
    def __init__(self, media_duration):
        super().__init__()
        self.media_duration = media_duration
        self.width = None
        self.height = None
        
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        tick_positions = self.calculate_tick_positions()

        # Set the font for the tick labels
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Draw the tick marks and labels
        for tick_pos in tick_positions:
            # Draw the tick mark
            painter.drawLine(tick_pos, 0, tick_pos, self.height)

            # Draw the tick label
            text = self.generate_tick_label(tick_pos)
            text_rect = painter.fontMetrics().boundingRect(text)
            text_width = text_rect.width()
            text_height = text_rect.height()
            text_x = tick_pos - text_width // 2
            text_y = self.height + text_height
            painter.drawText(text_x, text_y, text)

    def calculate_tick_positions(self):
        num_ticks = 10
        tick_interval = self.width / num_ticks
        return [int(i * tick_interval) for i in range(num_ticks + 1)]

    def generate_tick_label(self, tick_pos):
        time_value = tick_pos * self.media_duration / self.width
        milliseconds = int(time_value)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"
    
    """Override"""
    def sizeHint(self, which, constraint):
        # Takes into account the position of the widget inside the scene
        self.width = int(self.scene().width() - self.pos().x() * 2)
        self.height = 10
        return QSizeF(self.width, self.height)
