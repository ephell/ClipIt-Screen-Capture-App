from pynput import keyboard
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit


class LineEditBase(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.key_combo_listener = _KeyComboListener(self.setText)

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setText("Press any key/combo...")
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
        self.pressed_keys = []
        self.max_key_amount_in_combo = 3
        self.key_combo = ""
        self.listener = None

    def start(self):
        if self.listener is None:
            self.listener = keyboard.Listener(
                on_press=self.__on_press, 
                on_release=self.__on_release,
                suppress=True
            )
            self.listener.start()

    def stop(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

    def get_key_combo_string(self):
        combo = ""
        for key in self.pressed_keys:
            key = self.__format_key_string(key)
            combo += key + " + "
        return combo[:-3]

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
                "caps_lock": "CapsLock"
            }
        return special_keys.get(key, key.title())

    def __convert_key_obj_to_string(self, key):
        try:
            key_string = key.char
            if hasattr(key, "vk") and key.vk in self.NUMPAD_KEYS:
                key_string = self.NUMPAD_KEYS[key.vk]
        except AttributeError:
            key_string = key.name
        return key_string

    def __on_press(self, key):
        key_string = self.__convert_key_obj_to_string(key)
        if len(self.pressed_keys) < self.max_key_amount_in_combo:
            if key_string not in self.pressed_keys:
                self.pressed_keys.append(key_string)
        else:
            print("Max key combo length reached")

        print(f"Pressed keys: {self.pressed_keys}")
        print(f"Key combo: {self.get_key_combo_string()}")
        if self.set_text_callback is not None:
            self.set_text_callback(self.get_key_combo_string())

    def __on_release(self, key):
        key_string = self.__convert_key_obj_to_string(key)
        if key_string in self.pressed_keys:
            self.pressed_keys.remove(key_string)
        if key == keyboard.Key.esc:
            return False
