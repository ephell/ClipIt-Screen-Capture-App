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
        tickPositions = self.calculateTickPositions()

        # Set the font for the tick labels
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        # Draw the tick marks and labels
        for tickPos in tickPositions:
        
            # Draw the tick mark
            painter.drawLine(tickPos, 0, tickPos, self.height)

            # Draw the tick label
            text = str(tickPos)
            textRect = painter.fontMetrics().boundingRect(text)
            textWidth = textRect.width()
            textHeight = textRect.height()
            textX = tickPos - textWidth // 2
            textY = self.height + textHeight
            painter.drawText(textX, textY, text)

    def calculateTickPositions(self):
        interval = 50
        return [i * interval for i in range(int(self.width / interval) + 1)]
    
    """Override"""
    def sizeHint(self, which, constraint):
        # Has extra padding to the width so that last tick label
        # is not cut off when the handle is dragged over it.
        return QSizeF(self.width + 25, self.height)
