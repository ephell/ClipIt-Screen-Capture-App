import os


class NuitkaCommandGenerator:
    """
    Utility class for generating a compilation command for Nuitka.
    
    - Install 'nuitka' to virtual environment.
    - Activate virtual environment.
    - Generate the command.
    - Run the command.

    """
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
        "src\\settings\\settings.ini",
        "src\\imageio_ffmpeg\\ffmpeg-win64-v4.2.2.exe"
    ]
    _DATA_DIR_RELATIVE_PATHS = [
        "src\\gui\\main_window\\system_tray\\icons",
    ]
    _PLUGINS_TO_ENABLE = [
        "pyside6"
    ]
    _QT_PLUGINS = [
        "multimedia"
    ]
 
    def generate_final_command(self):
        final_command = f"python -m nuitka "
        final_command += f"{self._get_mode()} "
        final_command += f"{self._get_entry_file_name()} "
        final_command += f"{self._generate_app_icon_command()} "
        final_command += f"{self._generate_include_qt_plugins_command()} "
        for command in self._generate_include_data_files_commands():
            final_command += f"{command} "
        for command in self._generate_include_data_dir_commands():
            final_command += f"{command} "
        for enable_plugin_command in self._generate_enable_plugin_commands():
            final_command += f"{enable_plugin_command} "
        return final_command
    
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

    def _generate_include_qt_plugins_command(self):
        command = f"--include-qt-plugins="
        for plugin in self._QT_PLUGINS:
            command += f"{plugin},"
        return command[:-1]

    def _get_absolute_path(self, relative_path):
        return os.path.abspath(relative_path)


if __name__ == "__main__":
    gen = NuitkaCommandGenerator()
    print(gen.generate_final_command())
