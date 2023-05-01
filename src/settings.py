import os


class Paths:
    """Various paths."""

    __PARENT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    TEMP_DIR = os.path.join(__PARENT_DIR, "temp")
    RECORDINGS_DIR = os.path.join(__PARENT_DIR, "recordings")
    LOGS_DIR = os.path.join(__PARENT_DIR, "logs")


class TempFiles:
    """Names of temporary files."""

    CAPTURED_VIDEO_FILE = "captured_video.mp4"
    LOOPBACK_AUDIO_FILE = "loopback_audio.wav"
    MICROPHONE_AUDIO_FILE = "microphone_audio.wav"
    MERGED_AUDIO_FILE = "merged_audio.wav"
    FINAL_FILE = "final_file.mp4"
