from pynput import keyboard


class HotkeyListener:

    combos_to_add = [
        ["shift", "A"],
        ["shift", "a"],
    ]
    VALID_COMBINATIONS = []

    def __init__(self):
        self.__listener = None
        self.pressed_keys = []
        for combo_str in self.combos_to_add:
            self.VALID_COMBINATIONS.append(
                self.__convert_to_keyboard_objects(combo_str)
            )

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
        if (
            any([key in COMBO for COMBO in self.VALID_COMBINATIONS]) 
            and not key in self.pressed_keys
        ):
            if isinstance(key, keyboard.KeyCode):
                self.__handle_press_keycode_obj(key)
            elif isinstance(key, keyboard.Key):
                self.__handle_press_key_obj(key)
            if self.__is_valid_combination(self.VALID_COMBINATIONS, self.pressed_keys):
                self.execute(self.pressed_keys)

    def __on_release(self, key):
        """Callback for listener on_release event."""
        if any([key in COMBO for COMBO in self.VALID_COMBINATIONS]):
            if isinstance(key, keyboard.KeyCode):
                self.__handle_release_keycode_obj(key)
            elif isinstance(key, keyboard.Key):
                self.__handle_release_key_obj(key)

    def __handle_press_key_obj(self, key: keyboard.Key):
        self.pressed_keys.append(key)

    def __handle_release_key_obj(self, key: keyboard.Key):
        self.pressed_keys.remove(key)

    def __handle_press_keycode_obj(self, key: keyboard.KeyCode):
        all_keys_as_str = {
            k.char for k in self.pressed_keys if isinstance(k, keyboard.KeyCode)
        }
        current_key_as_str = key.char
        if (
            current_key_as_str.lower() not in all_keys_as_str 
            and current_key_as_str.upper() not in all_keys_as_str
        ):
            self.pressed_keys.append(keyboard.KeyCode.from_char(current_key_as_str))

    def __handle_release_keycode_obj(self, key: keyboard.KeyCode):
        all_keys_as_str = {
            k.char for k in self.pressed_keys if isinstance(k, keyboard.KeyCode)
        }
        current_key_as_str = key.char
        if current_key_as_str.upper() in all_keys_as_str:
            self.pressed_keys.remove(keyboard.KeyCode.from_char(current_key_as_str.upper()))
        elif current_key_as_str.lower() in all_keys_as_str:
            self.pressed_keys.remove(keyboard.KeyCode.from_char(current_key_as_str.lower()))

    @staticmethod
    def __is_valid_combination(all_combos: list[list[str]], pressed_keys: list[str]):
        for combo in all_combos:
            if (
                len(combo) == len(pressed_keys) 
                and all(combo_key == pressed_key for combo_key, pressed_key in zip(combo, pressed_keys))
            ):
                return True
        return False

    @staticmethod
    def __convert_to_keyboard_objects(combo_str):
        result = []
        for key_str in combo_str:
            if key_str == "shift":
                result.append(keyboard.Key.shift)
            else:
                result.append(keyboard.KeyCode(char=key_str))
        return result
