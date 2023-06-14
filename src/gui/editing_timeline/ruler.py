from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class Ruler(QGraphicsWidget):
    
    def __init__(self):
        super().__init__()
        self.width = 750
        self.height = 10
        
    """Override"""
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        tick_positions = self.calculate_tick_positions()

        # Set the font for the tick labels
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        # Draw the tick marks and labels
        for tick_pos in tick_positions:
        
            # Draw the tick mark
            painter.drawLine(tick_pos, 0, tick_pos, self.height)

            # Draw the tick label
            text = str(tick_pos)
            text_rect = painter.fontMetrics().boundingRect(text)
            text_width = text_rect.width()
            text_height = text_rect.height()
            text_x = tick_pos - text_width // 2
            text_y = self.height + text_height
            painter.drawText(text_x, text_y, text)

    def calculate_tick_positions(self):
        interval = 50
        return [i * interval for i in range(int(self.width / interval) + 1)]
    
    """Override"""
    def sizeHint(self, which, constraint):
        # Has extra padding to the width so that last tick label
        # is not cut off when the handle is dragged over it.
        return QSizeF(self.width + 25, self.height)
