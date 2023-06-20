from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class GraphicsSceneBorder(QGraphicsRectItem):

    def __init__(self, scene):
        super().__init__(scene.sceneRect())
        self.scene = scene
        self.scene.addItem(self)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.green, 1))
        painter.drawRect(0, 0, self.scene.width(), self.scene.height())


class GraphicsScene(QGraphicsScene):

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        self.media_item_x = 50
        self.media_item_y = 55
        self.ruler_x = 50
        self.ruler_y = 20
        self.ruler_handle_x = 50
        self.ruler_handle_y = 0


class GraphicsView(QGraphicsView):

    view_resized = Signal()

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setScene(scene)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumHeight(self.scene.height())
        self.setMinimumWidth(self.scene.width())

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view_resized.emit()

    def resize_scene(self, new_width):
        self.scene.setSceneRect(0, 0, new_width, self.scene.height())


class RulerHandle(QGraphicsRectItem):

    def __init__(self, scene, view, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.view = view
        self.setRect(0, 0, 10, 100)
        self.setBrush(QBrush(Qt.red))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.media_duration = media_duration
        self.delta_needed_to_move = 20
        self.move_by_ms = 50
        self.initial_x = 50
        self.initial_y = 0
        self.setPos(self.initial_x, self.initial_y)

    """Override"""
    def mouseMoveEvent(self, event):
        delta_x = event.scenePos().x() - self.scenePos().x()
        new_x = self.__calculate_new_x(delta_x)
        self.setPos(new_x, self.scenePos().y())

        current_time = self.__convert_scene_x_to_time(new_x)

        print(
            f"Self scene pos x: {self.scenePos().x()} | "
            f"Current time: {current_time} | "
            f"New x: {new_x} | "
        )

    def __calculate_new_x(self, delta_x):
        if delta_x >= self.delta_needed_to_move:
            new_x = self.__calculate_new_x_when_delta_increasing(self.move_by_ms)
        elif delta_x <= -self.delta_needed_to_move:
            new_x = self.__calculate_new_x_when_delta_decreasing(self.move_by_ms)
        elif -self.delta_needed_to_move < delta_x < self.delta_needed_to_move:
            new_x = self.scenePos().x()
        return new_x

    def __calculate_new_x_when_delta_increasing(self, move_by_ms):
        new_x = self.scenePos().x() + self.__convert_time_to_pixels(move_by_ms)
        if new_x >= self.__get_max_possible_x():
            new_x = self.__get_max_possible_x()
        return new_x

    def __calculate_new_x_when_delta_decreasing(self, move_by_ms):
        new_x = self.scenePos().x() - self.__convert_time_to_pixels(move_by_ms)
        if new_x <= self.__get_min_possible_x():
            new_x = self.__get_min_possible_x()
        # Removing remainder of time if it exists so that the handle
        # moves in equal increments of time.
        if self.scenePos().x() == self.__get_max_possible_x():
            current_time = self.__convert_pixels_to_time(
                self.__get_max_possible_width()
            )
            time_remainder = current_time % move_by_ms
            if time_remainder != 0:
                closest_whole_time = current_time - time_remainder
                new_x = self.__convert_time_to_scene_x(closest_whole_time)
                
        return new_x
        
    def __get_one_pixel_time_value(self):
        return self.media_duration / self.__get_max_possible_width()

    def __convert_time_to_pixels(self, time):
        return time / self.__get_one_pixel_time_value()
    
    def __convert_pixels_to_time(self, pixels):
        return round(pixels * self.__get_one_pixel_time_value())
    
    def __convert_time_to_scene_x(self, time):
        return self.__convert_time_to_pixels(time) + self.__get_min_possible_x()
    
    def __convert_scene_x_to_time(self, scene_x):
        return self.__convert_pixels_to_time(scene_x - self.__get_min_possible_x())

    def __get_max_possible_x(self):
        return self.__get_min_possible_x() + self.__get_max_possible_width()
    
    def __get_min_possible_x(self):
        return self.initial_x

    def __get_padding(self):
        return self.initial_x * 2

    def __get_max_possible_width(self):
        return self.scene.width() - self.__get_padding()

    @Slot()
    def on_view_resized(self):
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        scene_width = 577
        scene_height = 200
        self.setGeometry(500, 500, scene_width + 30, scene_height)

        self.scene = GraphicsScene(scene_width, scene_height)
        self.view = GraphicsView(self.scene)
            
        self.scene_borders = GraphicsSceneBorder(self.scene)
        self.ruler_handle = RulerHandle(self.scene, self.view, 5397)

        # self.view.view_resized.connect(self.ruler_handle.on_view_resized)

        self.setCentralWidget(self.view)


if __name__ == '__main__':
    app = QApplication([])
    # app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.show()
    app.exec()
