from proglog import ProgressBarLogger


class ProgressLoggers:

    def __init__(
            self,
            final_file_rendering_progress_signal,
            temp_cut_video_rendering_progress_signal,
            cropping_progress_signal
        ):
        self.final_file_rendering = _FinalFileRenderingProgressLogger(
            final_file_rendering_progress_signal
        )
        self.temp_cut_video_rendering = _TempCutVideoRenderingProgressLogger(
            temp_cut_video_rendering_progress_signal
        )
        self.cropping = _CroppingProgressLogger(cropping_progress_signal)


class _FinalFileRenderingProgressLogger(ProgressBarLogger):

    def __init__(self, progress_signal):
        super().__init__()
        self.progress_signal = progress_signal

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == "index":
            percentage = (value / self.bars[bar]["total"]) * 100
            self.progress_signal.emit(percentage)


class _TempCutVideoRenderingProgressLogger(ProgressBarLogger):
    """
    Used to emit progress signals when rendering the temporary cut video
    that is used as a source for cropping.
    """
    def __init__(self, progress_signal):
        super().__init__()
        self.progress_signal = progress_signal

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == "index":
            percentage = (value / self.bars[bar]["total"]) * 100
            self.progress_signal.emit(percentage)


class _CroppingProgressLogger:

    def __init__(self, progress_signal):
        self.progress_signal = progress_signal
