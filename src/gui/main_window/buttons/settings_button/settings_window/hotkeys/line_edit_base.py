from pynput import keyboard
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit

import random

class LineEditBase(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setReadOnly(True)
        self.key_combo_listener = _KeyComboListener(self.setText)

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setText("Press any key/key combo...")
            if self.hasFocus():
                self.clearFocus()
            self.setFocus()

    """Override"""
    def focusInEvent(self, event):
        self.key_combo_listener.start()
        
    """Override"""
    def focusOutEvent(self, event):
        self.key_combo_listener.stop()


class _KeyComboListener:

    # The dictionary key is the value of 'vk' attribute of the key object
    NUMPAD_KEYS = {
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

    def __init__(self, set_text_callback=None):
        self.set_text_callback = set_text_callback
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

    def __on_press(self, key_obj):
        key_str = self.__get_key_obj_string_representation(key_obj)
        if len(self.__pressed_keys) < self.__max_key_amount_in_combo:
            if key_str is not None and key_str not in self.__pressed_keys:
                self.__pressed_keys.append(key_str)
        else:
            print("Max key combo length reached")
        print(f"Key combo: {self.__get_key_combo_string()}")
        if self.set_text_callback is not None:
            self.set_text_callback(self.__get_key_combo_string())

    def __on_release(self, key_obj):
        key_str = self.__get_key_obj_string_representation(key_obj)
        if key_str in self.__pressed_keys:
            self.__pressed_keys.remove(key_str)
        if len(self.__pressed_keys) <= 0:
            self.stop()

    def __get_key_obj_string_representation(self, key_obj):
        try:
            key_str = key_obj.char
            if hasattr(key_obj, "vk") and key_obj.vk in self.NUMPAD_KEYS:
                key_str = self.NUMPAD_KEYS[key_obj.vk]
        except AttributeError:
            key_str = key_obj.name
        return key_str

    def __format_key_string(self, key):
        special_keys = {
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
        return special_keys.get(key, key.title())

    def __get_key_combo_string(self):
        combo = ""
        for key in self.__pressed_keys:
            key = self.__format_key_string(key)
            combo += key + " + "
        return combo[:-3]
