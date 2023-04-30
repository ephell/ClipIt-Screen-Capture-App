import os

from recorder.recorder import Recorder

def __create_directories():
    """Creates directories for temporary files and final output."""
    if not os.path.exists("temp"):
        os.makedirs("temp")
    if not os.path.exists("recordings"):
        os.makedirs("recordings")

def main():
    __create_directories()
    recorder = Recorder(
        duration=10,
        record_video=True,
        record_loopback=True,
        record_microphone=True,
        monitor=2,
        region=[60, 216, 1150, 650],
        fps=30,
    )
    recorder.record()
    print("All done!")
    
if __name__ == '__main__':
    main()
