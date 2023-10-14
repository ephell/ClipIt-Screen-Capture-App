from abc import abstractmethod

from pynput import keyboard
from PySide6.QtCore import Qt, QObject, Signal, Slot
from PySide6.QtWidgets import QLineEdit


class LineEditBase(QLineEdit):

    stopped_listening_for_key_combos_signal = Signal(str)

    __DEFAULT_TEXT = "Press any key/key combo..."
    __NONE_TEXT = "None"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setReadOnly(True)
        self.key_combo_listener = _KeyComboListener()
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.key_combo_listener.key_combo_changed_signal.connect(
            self.on_key_combo_changed_signal
        )
        self.key_combo_listener.clear_key_pressed_signal.connect(
            self.on_clear_key_pressed_signal
        )
        self.key_combo_listener.all_keys_released_signal.connect(
            self.on_all_keys_released_signal
        )

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.key_combo_listener.running():
                self.key_combo_listener.start()
            if self.key_combo_listener.running():
                self.setText(self.__DEFAULT_TEXT)

    """Override"""
    def focusInEvent(self, event):
        self.setText(self.__DEFAULT_TEXT)
        
    """Override"""
    def focusOutEvent(self, event):
        if self.text() == self.__DEFAULT_TEXT:
            self.setText(self.__NONE_TEXT)
        if self.key_combo_listener.running():
            self.key_combo_listener.stop()
        if not self.key_combo_listener.running():
            self.stopped_listening_for_key_combos_signal.emit(self.text())

    @Slot()
    @abstractmethod
    def on_stopped_listening_for_key_combos(self):
        pass

    @Slot()
    def on_key_combo_changed_signal(self, combo_string):
        self.setText(combo_string)

    @Slot()
    def on_clear_key_pressed_signal(self):
        self.setText(self.__NONE_TEXT)
        self.clearFocus()

    @Slot()
    def on_all_keys_released_signal(self):
        self.clearFocus()

    @Slot()
    def on_left_mouse_button_pressed_on_settings_window(self):
        if self.hasFocus():
            if self.text() == self.__DEFAULT_TEXT:
                self.setText(self.__NONE_TEXT)
            self.clearFocus()


class _KeyComboListener(QObject):

    clear_key_pressed_signal = Signal()
    key_combo_changed_signal = Signal(str)
    all_keys_released_signal = Signal()

    # The dictionary key is the value of 'vk' attribute of the key object
    __NUMPAD_KEYS = {
        96: "Num0",
        97: "Num1",
        98: "Num2",
        99: "Num3",
        100: "Num4",
        101: "Num5",
        102: "Num6",
        103: "Num7",
        104: "Num8",
        105: "Num9"
    }
    # Remove focus from line edit when any of these keys are pressed
    __CLEAR_KEYS = {"esc", "backspace"}
    # Used to format the string representation of key objects' special keys
    __SPECIAL_KEYS = {
            "print_screen": "PrtScr",
            "ctrl_l": "LCtrl",
            "ctrl_r": "RCtrl",
            "alt_l": "LAlt",
            "alt_gr": "RAlt",
            "shift": "LShift",
            "shift_r": "RShift",
            "cmd": "LWin",
            "cmd_r": "RWin",
            "num_lock": "NumLock",
            "caps_lock": "CapsLock",
            "page_up": "PageUp",
            "page_down": "PageDown"
        }

    def __init__(self):
        super().__init__()
        self.__pressed_keys = []
        self.__max_key_amount_in_combo = 3
        self.__listener = None

    def start(self):
        if self.__listener is None:
            self.__listener = keyboard.Listener(
                on_press=self.__on_press, 
                on_release=self.__on_release,
                suppress=True
            )
            self.__listener.start()

    def stop(self):
        if self.__listener is not None:
            self.__listener.stop()
            self.__listener = None

    def running(self):
        return self.__listener is not None and self.__listener.running

    def __on_press(self, key_obj):
        key_str = self.__get_key_obj_string_representation(key_obj)
        if key_str in self.__CLEAR_KEYS:
            self.clear_key_pressed_signal.emit()
            return
        if len(self.__pressed_keys) < self.__max_key_amount_in_combo:
            if key_str is not None and key_str not in self.__pressed_keys:
                self.__pressed_keys.append(key_str)
            self.key_combo_changed_signal.emit(self.__get_key_combo_string())

    def __on_release(self, key_obj):
        key_str = self.__get_key_obj_string_representation(key_obj)
        if key_str in self.__pressed_keys:
            self.__pressed_keys.remove(key_str)
        if len(self.__pressed_keys) <= 0:
            self.all_keys_released_signal.emit()

    def __get_key_obj_string_representation(self, key_obj):
        try:
            key_str = key_obj.char
            if hasattr(key_obj, "vk") and key_obj.vk in self.__NUMPAD_KEYS:
                key_str = self.__NUMPAD_KEYS[key_obj.vk]
        except AttributeError:
            key_str = key_obj.name
        return key_str

    def __format_key_string(self, key):
        return self.__SPECIAL_KEYS.get(key, key.title())

    def __get_key_combo_string(self):
        combo = ""
        for key in self.__pressed_keys:
            key = self.__format_key_string(key)
            combo += key + " + "
        return combo[:-3]
