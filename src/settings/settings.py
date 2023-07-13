from configparser import ConfigParser
import os


class Settings:

    @staticmethod
    def get_capture_dir_path():
        parser = ConfigParser()
        parser.read("src/settings/settings.ini")
        return parser["PATHS"]["CAPTURE_DIR_PATH"]
    
    @staticmethod
    def get_temp_dir_path():
        return _TempFilePaths.DIR_PATH

    @staticmethod
    def get_temp_file_paths():
        return _TempFilePaths


class _TempFilePaths:

    DIR_PATH = os.path.join(os.getcwd(), "temp")
    CAPTURED_VIDEO_FILE = os.path.join(DIR_PATH, "captured_video.mp4")
    REENCODED_VIDEO_FILE = os.path.join(DIR_PATH, "reencoded_video.mp4")
    LOOPBACK_AUDIO_FILE = os.path.join(DIR_PATH, "loopback_audio.wav")
    MICROPHONE_AUDIO_FILE = os.path.join(DIR_PATH, "microphone_audio.wav")
    MERGED_AUDIO_FILE = os.path.join(DIR_PATH, "merged_audio.wav")
    FINAL_FILE = os.path.join(DIR_PATH, "final_file.mp4")
