import os
from recorder import Recorder

def __create_directories():
    """Creates directories for temporary files and final output."""
    if not os.path.exists("temp"):
        os.makedirs("temp")
    if not os.path.exists("recordings"):
        os.makedirs("recordings")

def main():
    __create_directories()
    recorder = Recorder(
        duration=5,
        record_video=True,
        record_loopback=True,
        record_microphone=True
    )
    recorder.record()
    
if __name__ == '__main__':
    main()
