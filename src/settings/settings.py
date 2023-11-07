from configparser import ConfigParser
import os


class Settings:

    SETTINGS_FILE = "src\\settings\\settings.ini"

    @classmethod
    def get_capture_dir_path(cls):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        return parser["PATHS"]["CAPTURE_DIR_PATH"]
    
    @staticmethod
    def get_temp_dir_path():
        return _TempFilePaths.DIR_PATH

    @staticmethod
    def get_temp_file_paths():
        return _TempFilePaths
    
    @classmethod
    def get_hotkeys(cls):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        return parser["HOTKEYS"]
    
    @classmethod
    def get_video_recorder_settings(cls):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        return parser["VIDEO_RECORDER"]
    
    @classmethod
    def set_video_recorder_setting(cls, setting_name, setting_value):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        parser["VIDEO_RECORDER"][setting_name] = setting_value
        with open(cls.SETTINGS_FILE, "w") as configfile:
            parser.write(configfile)

    @classmethod
    def set_hotkey(cls, hotkey_name, hotkey_value):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        parser["HOTKEYS"][hotkey_name] = hotkey_value
        with open(cls.SETTINGS_FILE, "w") as configfile:
            parser.write(configfile)

    @classmethod
    def set_capture_dir_path(cls, path):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        parser["PATHS"]["CAPTURE_DIR_PATH"] = path
        with open(cls.SETTINGS_FILE, "w") as configfile:
            parser.write(configfile)


class _TempFilePaths:

    DIR_PATH = os.path.join(os.getcwd(), "temp")
    CAPTURED_VIDEO_FILE = os.path.join(DIR_PATH, "captured_video.mp4")
    REENCODED_VIDEO_FILE = os.path.join(DIR_PATH, "reencoded_video.mp4")
    CUT_VIDEO_FILE = os.path.join(DIR_PATH, "cut_video.mp4")
    CROPPED_VIDEO_FILE = os.path.join(DIR_PATH, "cropped_video.mp4")
    LOOPBACK_AUDIO_FILE = os.path.join(DIR_PATH, "loopback_audio.wav")
    FINAL_FILE = os.path.join(DIR_PATH, "final_file.mp4")
