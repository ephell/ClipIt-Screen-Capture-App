from abc import abstractmethod

from pynput import keyboard
from PySide6.QtCore import Qt, QObject, Signal, Slot
from PySide6.QtWidgets import QLineEdit

from settings.settings import Settings


class LineEditBase(QLineEdit):

    focus_in_event_signal = Signal()
    focus_out_event_signal = Signal(str)

    __DEFAULT_TEXT = "Press any key/key combo..."
    __NONE_TEXT = "None"
    __IN_USE_TEXT = "({}) already in use!"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setReadOnly(True)
        self.key_combo_listener = _KeyComboListener()
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.key_combo_listener.clear_key_pressed_signal.connect(
            self.__on_clear_key_pressed
        )
        self.key_combo_listener.all_keys_released_signal.connect(
            self.__on_all_keys_released
        )
        self.key_combo_listener.combo_valid_signal.connect(
            self.__on_key_combo_valid
        )
        self.key_combo_listener.combo_invalid_signal.connect(
            self.__on_key_combo_invalid
        )
        self.key_combo_listener.combo_in_use_signal.connect(
            self.__on_key_combo_in_use
        )
        self.key_combo_listener.max_combo_length_reached_signal.connect(
            self.__on_max_combo_length_reached
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
        self.focus_in_event_signal.emit()
        
    """Override"""
    def focusOutEvent(self, event):
        if self.text() == self.__DEFAULT_TEXT:
            self.setText(self.__NONE_TEXT)
        if self.key_combo_listener.running():
            self.key_combo_listener.stop()
        self.focus_out_event_signal.emit(self.text())

    @abstractmethod
    def load_hotkey_from_settings(self, hotkey_name):
        pass

    @Slot()
    @abstractmethod
    def on_key_combo_listener_started(self):
        pass

    @Slot()
    @abstractmethod
    def on_key_combo_valid(self, combo_string):
        pass

    @Slot()
    @abstractmethod
    def on_key_combo_in_use(self):
        pass

    @Slot()
    def on_left_mouse_button_pressed_on_settings_window(self):
        if self.hasFocus():
            if self.text() == self.__DEFAULT_TEXT:
                self.setText(self.__NONE_TEXT)
            self.clearFocus()

    @Slot()
    def __on_clear_key_pressed(self):
        self.setText(self.__NONE_TEXT)
        self.clearFocus()

    @Slot()
    def __on_all_keys_released(self):
        self.clearFocus()

    @Slot()
    def __on_key_combo_valid(self, combo_string):
        self.setText(combo_string)

    @Slot()
    def __on_key_combo_invalid(self):
        self.clearFocus()

    @Slot()
    def __on_key_combo_in_use(self, combo_string):
        self.setText(self.__IN_USE_TEXT.format(combo_string))

    @Slot()
    def __on_max_combo_length_reached(self):
        self.clearFocus()


class _KeyComboListener(QObject):

    clear_key_pressed_signal = Signal()
    all_keys_released_signal = Signal()
    combo_valid_signal = Signal(str)
    combo_invalid_signal = Signal()
    combo_in_use_signal = Signal(str)
    max_combo_length_reached_signal = Signal()
    listener_started_signal = Signal()

    # Remove focus from line edit and clear its text if these keys are pressed
    __CLEAR_KEYS = {"esc", "backspace"}
    # Used to format the string representation of key objects' special keys
    __SPECIAL_KEYS = {
            "ctrl_l": "Ctrl",
            "ctrl_r": "Ctrl",
            "alt_l": "Alt",
            "alt_gr": "Alt",
            "shift": "Shift",
            "shift_r": "Shift",
            "cmd": "Win",
            "cmd_r": "Win",
            "print_screen": "PrtScr",
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
            self.listener_started_signal.emit()

    def stop(self):
        if self.__listener is not None:
            self.__listener.stop()
            self.__listener = None

    def running(self):
        return self.__listener is not None and self.__listener.running

    def __on_press(self, key):
        key = self.__get_key_as_str(key)
        if key in self.__CLEAR_KEYS:
            self.clear_key_pressed_signal.emit()
            return
        if key is not None and key not in self.__pressed_keys:
            self.__pressed_keys.append(key)
            if self.__is_combo_in_valid_format():
                if not self.__is_combo_in_use():
                    self.combo_valid_signal.emit(self.__get_key_combo_as_str())
                else:
                    self.combo_in_use_signal.emit(self.__get_key_combo_as_str())
                    self.__pressed_keys.clear()
            else:
                self.combo_invalid_signal.emit()
                self.__pressed_keys.clear()
            if len(self.__pressed_keys) >= self.__max_key_amount_in_combo:
                self.max_combo_length_reached_signal.emit()
                self.__pressed_keys.clear()
                return

    def __on_release(self, key):
        key = self.__get_key_as_str(key)
        if key in self.__pressed_keys:
            self.__pressed_keys.remove(key)
        if len(self.__pressed_keys) <= 0:
            self.all_keys_released_signal.emit()

    def __get_key_as_str(self, key: keyboard.KeyCode | keyboard.Key):
        if isinstance(key, keyboard.Key):
            return key.name
        elif isinstance(key, keyboard.KeyCode):
            return key.char.upper() if key.char else None
        return None

    def __get_key_combo_as_str(self):
        combo = ""
        for key in self.__pressed_keys:
            key = self.__SPECIAL_KEYS.get(key, key.title())
            combo += key + " + "
        return combo[:-3]

    def __is_combo_in_valid_format(self):
        """
        Combo is considered invalid if it contains a regular key that
        is followed by a special key. For example "Ctrl + A" is valid, 
        but "A + Ctrl" is not.
        """
        combo = self.__pressed_keys
        special_keys = set(self.__SPECIAL_KEYS.keys())
        for i in range(0, len(combo) - 1):
            if combo[i] not in special_keys:
                if combo[i+1] in special_keys:
                    return False
        return True

    def __is_combo_in_use(self):
        """Check if combo is already used by another hotkey."""
        return self.__get_key_combo_as_str() in list(dict(Settings.get_hotkeys().items()).values())
