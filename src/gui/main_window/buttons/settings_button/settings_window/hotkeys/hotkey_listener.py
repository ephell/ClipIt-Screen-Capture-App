from pynput import keyboard


class HotkeyListener:

    ASCII_CONTROL_CHARACTERS = {
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

    VALID_COMBINATIONS = [
        ["SHIFT", "A", "B"],
        ["SHIFT_R", "A", "B"],
        ["CTRL_L", "A"],
        ["CTRL_R", "A"],
    ]

    def __init__(self):
        self.__listener = None
        self.pressed_keys = []

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

    def execute(self, key_combo):
        print(f"Combo pressed: {key_combo}")

    def __on_press(self, key):
        """Callback for listener on_press event."""
        key = self.__get_key_as_str(key)
        if key is not None:
            for key in key.split("+"):
                if self.__is_valid_key(key) and key not in self.pressed_keys:
                    self.pressed_keys.append(key)
        if self.__combo_detected():
            self.execute(self.pressed_keys)
            self.pressed_keys.clear()

    def __on_release(self, key):
        """Callback for listener on_release event."""
        key = self.__get_key_as_str(key)
        if key is not None:
            for key in key.split("+"):
                if key in self.pressed_keys:
                    self.pressed_keys.remove(key)

    def __get_key_as_str(self, key: keyboard.KeyCode | keyboard.Key):
        if isinstance(key, keyboard.Key):
            return key.name.upper()
        elif isinstance(key, keyboard.KeyCode):
            return (
                self.ASCII_CONTROL_CHARACTERS.get(key.char)
                or key.char.upper() if key.char else None
            )
        return None

    def __is_valid_key(self, key_str):
        if any([key_str.upper() in combo for combo in self.VALID_COMBINATIONS]):
            return True
        return False

    def __combo_detected(self):
        for v_combo in self.VALID_COMBINATIONS:
            if (
                len(v_combo) == len(self.pressed_keys) 
                and all(v_key == p_key for v_key, p_key in zip(v_combo, self.pressed_keys))
            ):
                return True
        return False
