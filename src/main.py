from logger import Logger
log = Logger.setup_logger("GLOBAL", Logger.DEBUG, True, False)

import os

from recorder.recorder import Recorder
from settings import Paths


def __create_directories():
    """Creates directories for temporary files and final output."""
    if not os.path.exists(Paths.TEMP_DIR):
        os.makedirs(Paths.TEMP_DIR)
    if not os.path.exists(Paths.RECORDINGS_DIR):
        os.makedirs(Paths.RECORDINGS_DIR)

def main():
    __create_directories()
    recorder = Recorder(
        duration=0.01,
        record_video=True,
        record_loopback=False,
        record_microphone=False,
        monitor=2,
        region=[60, 216, 1150, 650],
        fps=30,
    )
    recorder.record()
    log.info("All done!")
    
if __name__ == '__main__':
    main()
