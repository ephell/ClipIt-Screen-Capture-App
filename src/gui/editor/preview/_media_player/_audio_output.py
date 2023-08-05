from PySide6.QtMultimedia import QAudioOutput


class AudioOutput(QAudioOutput):

    def __init__(self, parent=None):
        super().__init__(parent)
