import mss
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox

from gui.area_widgets.area_selector import AreaSelector
from gui.area_widgets.area_border_creator import AreaBorderCreator


class RecordingAreaSelector(QObject):
    
    area_selection_finished_signal = Signal()

    def __init__(self):
        super().__init__()
        self.area_selector = None
        self.recording_area_border = None
        self.recording_area_top_x = None
        self.recording_area_top_y = None
        self.recording_area_bottom_x = None
        self.recording_area_bottom_y = None
        self.recording_area_monitor = None

    def start_selection(self):
        if self.recording_area_border is not None:
            self.recording_area_border.destroy()
        self.area_selector = AreaSelector(self.__get_area_coords)
        self.area_selector.show()

    def get_area_coords(self):
        return (
            self.recording_area_top_x,
            self.recording_area_top_y,
            self.recording_area_bottom_x,
            self.recording_area_bottom_y
        )
    
    def get_monitor(self):
        return self.recording_area_monitor

    def __get_area_coords(self, x0, y0, x1, y1):
        """Callback function for the area selector."""
        if not self.__is_within_single_monitor_bounds(x0, y0, x1, y1):
            self.area_selector.close()
            QMessageBox.critical(
                self, 
                "Invalid Area", 
                "Selected area must not overlap multiple monitors."
            )
            return
        
        self.__draw_recording_area_border(x0, y0, x1, y1, (30, 200, 30))
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

        self.area_selection_finished_signal.emit()

    def __draw_recording_area_border(self, x0, y0, x1, y1, color):
        self.recording_area_border = AreaBorderCreator(x0, y0, x1, y1, color)
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
