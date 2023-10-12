from configparser import ConfigParser
import os


class Settings:

    SETTINGS_FILE = "src/settings/settings.ini"

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
    def get_audio_preferences(cls):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        return parser["AUDIO_PREFERENCES"]
    
    @classmethod
    def set_audio_preference(cls, preference_name, preference_value):
        parser = ConfigParser()
        parser.read(cls.SETTINGS_FILE)
        parser["AUDIO_PREFERENCES"][preference_name] = preference_value
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
    LOOPBACK_AUDIO_FILE = os.path.join(DIR_PATH, "loopback_audio.wav")
    MICROPHONE_AUDIO_FILE = os.path.join(DIR_PATH, "microphone_audio.wav")
    MERGED_AUDIO_FILE = os.path.join(DIR_PATH, "merged_audio.wav")
    FINAL_FILE = os.path.join(DIR_PATH, "final_file.mp4")
