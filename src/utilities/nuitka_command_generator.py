import os


class NuitkaCommandGenerator:
    """Utility class for generating a compilation command for Nuitka."""

    _MODE = "--standalone"
    _ENTRY_FILE_NAME = "main.py"
    _APP_ICON_RELATIVE_PATH = "src\\gui\\application\\logo.ico" # Must be .ico file
    _DATA_FILES_RELATIVE_PATHS = [
        "src\\gui\\application\\logo.ico",
        "src\\gui\\application\\logo.svg",
        "src\\gui\\main_window\\MainWindow.qss",
        "src\\gui\\main_window\\buttons\\open_editor_button\\editor_window\\preview\\_media_player_controls\\MediaPlayerControls.qss",
        "src\\gui\\main_window\\buttons\\open_editor_button\\editor_window\\timeline\\media_item\\media_item_handle.jpg",
        "src\\gui\\main_window\\buttons\\open_editor_button\\editor_window\\timeline\\media_item\\media_item_handle_in_focus.jpg",
        "src\\gui\\main_window\\buttons\\screenshot_button\\camera-click.wav",
        "src\\settings\\settings.ini"
    ]
    _DATA_DIR_RELATIVE_PATHS = [
        "src\\gui\\main_window\\system_tray\\icons",
    ]
    _PLUGINS_TO_ENABLE = [
        "pyside6"
    ]
 
    def generate_final_command(self):
        mode = self._get_mode()
        entry_file_name = self._get_entry_file_name()
        app_icon_command = self._generate_app_icon_command()
        include_data_files_commands = self._generate_include_data_files_commands()
        include_data_dir_commands = self._generate_include_data_dir_commands()
        enable_plugin_commands = self._generate_enable_plugin_commands()
        command = f"python -m nuitka {mode} {entry_file_name} {app_icon_command} "
        for include_data_files_command in include_data_files_commands:
            command += f"{include_data_files_command} "
        for include_data_dir_command in include_data_dir_commands:
            command += f"{include_data_dir_command} "
        for enable_plugin_command in enable_plugin_commands:
            command += f"{enable_plugin_command} "
        return command
    
    def _get_mode(self):
        return self._MODE

    def _get_entry_file_name(self):
        return self._ENTRY_FILE_NAME

    def _generate_app_icon_command(self):
        return f"--windows-icon-from-ico='{self._get_absolute_path(self._APP_ICON_RELATIVE_PATH)}'"

    def _generate_include_data_files_commands(self):
        commands = []
        for relative_path in self._DATA_FILES_RELATIVE_PATHS:
            absolute_path = self._get_absolute_path(relative_path)
            commands.append(f"--include-data-files='{absolute_path}'='{relative_path}'")
        return commands

    def _generate_include_data_dir_commands(self):
        commands = []
        for relative_path in self._DATA_DIR_RELATIVE_PATHS:
            absolute_path = self._get_absolute_path(relative_path)
            commands.append(f"--include-data-dir='{absolute_path}'='{relative_path}'")
        return commands

    def _generate_enable_plugin_commands(self):
        commands = []
        for plugin in self._PLUGINS_TO_ENABLE:
            commands.append(f"--enable-plugin={plugin}")
        return commands

    def _get_absolute_path(self, relative_path):
        return os.path.abspath(relative_path)


if __name__ == "__main__":
    gen = NuitkaCommandGenerator()
    print(gen.generate_final_command())
