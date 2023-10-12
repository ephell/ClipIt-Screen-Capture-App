import threading

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QPushButton, QMainWindow

from gui.main_window.buttons.open_editor_button.editor_window.editor_window import EditorWindow


class DebugButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Print Debug Info")

    @Slot()
    def on_debug_button_clicked(self):
        # self.__print_active_threads()
        # self.__print_all_widgets()
        # self.__find_widget_by_object_name("EditorWindow")
        self.__find_widget_by_type(EditorWindow)

    def __print_active_threads(self):
        print(threading.enumerate())

    def __print_all_widgets(self):
        widgets = self.__get_main_window_widget().app.allWidgets()
        print(
            "----------------------------------------\n"
            + "".join(repr(w) + "\n" for w in widgets)
            + "----------------------------------------"
        )

    def __find_widget_by_object_name(self, object_name: str):
        widgets = [
            w for w in self.__get_main_window_widget().app.allWidgets() \
            if w.objectName() == object_name # or isinstance(w, EditorWindow)
        ]
        print(
            "----------------------------------------\n"
            + "".join(repr(w) + "\n" for w in widgets)
            + "----------------------------------------"
        )

    def __find_widget_by_type(self, widget_type: type):
        widgets = [
            w for w in self.__get_main_window_widget().app.allWidgets() \
            if isinstance(w, widget_type)
        ]
        print(
            "----------------------------------------\n"
            + "".join(repr(w) + "\n" for w in widgets)
            + "----------------------------------------"
        )

    def __print_widget_signals(self, widget):
        cls = widget if isinstance(widget, type) else type(widget)
        signal = type(Signal())
        for subcls in cls.mro():
            clsname = f'{subcls.__module__}.{subcls.__name__}'
            for key, value in sorted(vars(subcls).items()):
                if isinstance(value, signal):
                    print(f'{key} [{clsname}]')

    def __get_main_window_widget(self):
        widget = self.parent()
        while widget is not None and not isinstance(widget, QMainWindow):
            widget = widget.parent()
        if widget is not None:
            return widget
        return None
