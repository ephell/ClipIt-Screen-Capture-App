from logger import GlobalLogger
log = GlobalLogger.LOGGER

import mss
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

from gui.recording_area_border import RecordingAreaBorder
from gui.area_selector import AreaSelector


class SelectAreaButton(QWidget):
    
    def __init__(self):
        super().__init__()
        self.area_selector = None
        self.recording_area_border = None
        self.recording_area_top_x = None
        self.recording_area_top_y = None
        self.recording_area_bottom_x = None
        self.recording_area_bottom_y = None
        self.recording_area_monitor = None

        button = QPushButton()
        button.setText("Select Area")
        button.clicked.connect(self.__on_select_area_clicked)

        self.area_label = QLabel()
        self.area_label.setText(f"No area selected.")

        layout = QVBoxLayout()
        layout.addWidget(self.area_label)
        layout.addWidget(button)
        self.setLayout(layout)

    def get_area_coords(self):
        return (
            self.recording_area_top_x,
            self.recording_area_top_y,
            self.recording_area_bottom_x,
            self.recording_area_bottom_y
        )
    
    def get_monitor(self):
        return self.recording_area_monitor

    def update_area_label(self, value=None):
        if isinstance(value, str):
            self.area_label.setText(value)
        elif isinstance(value, tuple):
            self.area_label.setText(f"Area: {value}")
        else:
            self.area_label.setText(f"No area selected.")

    def __on_select_area_clicked(self):
        """Callback function for the select area button."""
        if self.recording_area_border is not None:
            self.recording_area_border.destroy()
        self.area_selector = AreaSelector(
            self.__get_area_coords,
            self.update_area_label
        )
        self.area_selector.show()

    def __get_area_coords(self, x0, y0, x1, y1):
        """Callback function for the area selector."""
        if not self.__is_within_single_monitor_bounds(x0, y0, x1, y1):
            self.update_area_label(
                "Invalid selection. Area must be within a single monitor."
            )
            self.area_selector.close()
            return
        
        self.update_area_label((x0, y0, x1, y1))
        self.__draw_recording_area_border(x0, y0, x1, y1)
        self.area_selector.close()

        self.recording_area_monitor = self.__get_monitor_by_point(x0, y0)
        coords = self.__calculate_coords_within_monitor(
            self.recording_area_monitor,
            x0, y0, x1, y1
        )
        self.recording_area_top_x = coords[0]
        self.recording_area_top_y = coords[1]
        self.recording_area_bottom_x = coords[2]
        self.recording_area_bottom_y = coords[3]

    def __draw_recording_area_border(self, x0, y0, x1, y1):
        self.recording_area_border = RecordingAreaBorder(x0, y0, x1, y1)
        self.recording_area_border.start()

    def __is_within_single_monitor_bounds(self, x0, y0, x1, y1):
        """
        Check if top left and bottom right coordinates of the area 
        are within bounds of a single monitor.
        """
        with mss.mss() as sct:
            monitors = sct.monitors
            monitor_index_1 = None
            monitor_index_2 = None
            for i in range(1, len(monitors)):
                m = monitors[i]
                if (m["left"] <= x0 < m["left"] + m["width"] 
                    and m["top"] <= y0 < m["top"] + m["height"]):
                    monitor_index_1 = i
                if (m["left"] <= x1 < m["left"] + m["width"] 
                    and m["top"] <= y1 < m["top"] + m["height"]):
                    monitor_index_2 = i

            if monitor_index_1 == monitor_index_2:
                return True
            else:
                return False

    def __get_monitor_by_point(self, x, y):
        """Get the index of the monitor that contains the point (x, y)."""
        with mss.mss() as sct:
            monitors = sct.monitors
            for i in range(1, len(monitors)):
                m = monitors[i]
                if (m["left"] <= x < m["left"] + m["width"] 
                    and m["top"] <= y < m["top"] + m["height"]):
                    return i
            return None

    def __calculate_coords_within_monitor(self, monitor_index, x0, y0, x1, y1):
        """Calculate coordinates within the bounds of a single monitor."""
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_index]
            top_left_x = x0
            top_left_y = y0
            bottom_right_x = (x1 - monitor["left"]) - (x0 - monitor["left"])
            bottom_right_y = (y1 - monitor["top"]) - (y0 - monitor["top"])
            return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)