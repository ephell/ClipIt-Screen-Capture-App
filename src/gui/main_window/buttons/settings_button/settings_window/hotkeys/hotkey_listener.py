from pynput import keyboard
from PySide6.QtCore import QObject, Signal

from settings.settings import Settings


class HotkeyListener(QObject):

    hotkey_detected_signal = Signal(str)

    __ASCII_CONTROL_CHARACTERS = {
        "\x00": "CTRL+@",
        "\x01": "CTRL+A",
        "\x02": "CTRL+B",
        "\x03": "CTRL+C",
        "\x04": "CTRL+D",
        "\x05": "CTRL+E",
        "\x06": "CTRL+F",
        "\x07": "CTRL+G",
        "\x08": "CTRL+H",
        "\t"  : "CTRL+I",
        "\n"  : "CTRL+J",
        "\x0b": "CTRL+K",
        "\x0c": "CTRL+L",
        "\r"  : "CTRL+M",
        "\x0e": "CTRL+N",
        "\x0f": "CTRL+O",
        "\x10": "CTRL+P",
        "\x11": "CTRL+Q",
        "\x12": "CTRL+R",
        "\x13": "CTRL+S",
        "\x14": "CTRL+T",
        "\x15": "CTRL+U",
        "\x16": "CTRL+V",
        "\x17": "CTRL+W",
        "\x18": "CTRL+X",
        "\x19": "CTRL+Y",
        "\x1a": "CTRL+Z",
        "\x1b": "CTRL+[",
        "\x1c": "CTRL+\\",
        "\x1d": "CTRL+]",
        "\x1e": "CTRL+^",
        "\x1f": "CTRL+_"
    }

    __SPECIAL_KEYS = {
        "Ctrl" : {"ctrl_l", "ctrl_r"},
        "Alt"  : {"alt_l", "alt_gr"},
        "Shift": {"shift", "shift_r"},
        "Win": {"cmd", "cmd_r"},
        "PrtScr": {"print_screen"},
        "NumLock": {"num_lock"},
        "CapsLock": {"caps_lock"},
        "PageUp": {"page_up"},
        "PageDown": {"page_down"}
    }

    def __init__(self):
        super().__init__()
        self.__listener = None
        self.__pressed_keys = []
        self.__trackable_keys_limit = 3

    def start(self):
        if self.__listener is None:
            self.__listener = keyboard.Listener(
                on_press=self.__on_press, 
                on_release=self.__on_release
            )
            self.__listener.start()

    def stop(self):
        if self.__listener is not None:
            self.__listener.stop()
            self.__listener = None

    def __on_press(self, key):
        """Callback for listener on_press event."""
        if len(self.__pressed_keys) == self.__trackable_keys_limit:
            self.__pressed_keys.clear()
        key = self.__get_key_as_str(key)
        if key is not None:
            for key in key.split("+"):
                if key not in self.__pressed_keys:
                    self.__pressed_keys.append(key)
        if self.__is_combo_detected():
            self.hotkey_detected_signal.emit(self.__get_combo_name())

    def __on_release(self, key):
        """Callback for listener on_release event."""
        key = self.__get_key_as_str(key)
        if key is not None:
            for key in key.split("+"):
                if key in self.__pressed_keys:
                    self.__pressed_keys.remove(key)

    def __get_key_as_str(self, key: keyboard.KeyCode | keyboard.Key):
        if isinstance(key, keyboard.Key):
            return key.name.upper()
        elif isinstance(key, keyboard.KeyCode):
            return (
                self.__ASCII_CONTROL_CHARACTERS.get(key.char)
                or key.char.upper() if key.char else None
            )
        return None

    def __is_combo_detected(self):
        for _, combos in self.__generate_valid_combos().items():
            for combo in combos:
                if (
                    len(combo) == len(self.__pressed_keys) 
                    and all(v_key == p_key for v_key, p_key in zip(combo, self.__pressed_keys))
                ):
                    return True
        return False
    
    def __get_combo_name(self):
        for name, combos in self.__generate_valid_combos().items():
            for c in combos:
                if self.__pressed_keys == c:
                    return name
        return None

    def __generate_valid_combos(self):
        """
        Generate valid key combinations for each hotkey defined in the settings.

        Returns:
        -----------
        dict : {hotkey_name: [[variation_1], ...]]}
            A dictionary where keys are hotkey names, and values are lists of 
            possible variations for the combination. There are multiple 
            variations for some key combinations, because some keys like "Ctrl"
            return different values depending on which side of the keyboard they
            are pressed on. 

        Example:
        -----------
        If 'screenshot' hotkey is defined as "Ctrl + A" in the settings,
        then the returned dictionary will look like this:
        {"screenshot": [["CTRL_L", "A"], ["CTRL_R", "A"]]}

        """
        result_dict = {}
        for hotkey, combination in dict(Settings.get_hotkeys().items()).items():
            keys = combination.split(" + ")
            variations = [[]]
            for key in keys:
                if key in self.__SPECIAL_KEYS:
                    variations = [var + [special_key.upper()] for var in variations for special_key in self.__SPECIAL_KEYS[key]]
                else:
                    variations = [var + [key.upper()] for var in variations]
            result_dict[hotkey] = variations
        return result_dict
