import os


class Paths:
    """Various paths."""

    CWD = os.getcwd()
    TEMP_DIR = os.path.join(CWD, "temp")
    RECORDINGS_DIR = os.path.join(CWD, "recordings")


class TempFiles:
    """Names of temporary files."""

    CAPTURED_VIDEO_FILE = "captured_video.mp4"
    REENCODED_VIDEO_FILE = "reencoded_video.mp4"
    LOOPBACK_AUDIO_FILE = "loopback_audio.wav"
    MICROPHONE_AUDIO_FILE = "microphone_audio.wav"
    MERGED_AUDIO_FILE = "merged_audio.wav"
    FINAL_FILE = "final_file.mp4"
