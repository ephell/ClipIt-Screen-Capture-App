from logger import Logger

import os


class Paths:
    """Various paths."""

    __PARENT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    TEMP_DIR = os.path.join(__PARENT_DIR, "temp")
    RECORDINGS_DIR = os.path.join(__PARENT_DIR, "recordings")


class TempFiles:
    """Names of temporary files."""

    CAPTURED_VIDEO_FILE = "captured_video.mp4"
    LOOPBACK_AUDIO_FILE = "loopback_audio.wav"
    MICROPHONE_AUDIO_FILE = "microphone_audio.wav"
    MERGED_AUDIO_FILE = "merged_audio.wav"
    FINAL_FILE = "final_file.mp4"


class GlobalLogger:
    """Contains the global logger object."""
    
    LOGGER = Logger.setup_logger(
        logger_name="GLOBAL",
        log_level=Logger.DEBUG,
        log_to_console=True,
        log_to_file=False
    )
