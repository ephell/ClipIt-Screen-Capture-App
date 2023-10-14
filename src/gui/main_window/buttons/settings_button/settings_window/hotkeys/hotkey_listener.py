from pynput import keyboard


class HotkeyListener:

    VALID_COMBINATIONS = [
        ["SHIFT", "A"],
        ["CTRL_L", "A"]
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
            if self.__is_valid_key(key) and key not in self.pressed_keys:
                self.pressed_keys.append(key)
        if self.__combo_detected():
            self.execute(self.pressed_keys)
            self.pressed_keys.clear()

    def __on_release(self, key):
        """Callback for listener on_release event."""
        key = self.__get_key_as_str(key)
        if key is not None and key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def __get_key_as_str(self, key: keyboard.KeyCode | keyboard.Key):
        if isinstance(key, keyboard.Key):
            return key.name.upper()
        elif isinstance(key, keyboard.KeyCode):
            return key.char.upper() if key.char else None
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
