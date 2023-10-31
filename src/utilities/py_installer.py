import sys
import os


# https://stackoverflow.com/a/31966932/14787568
def get_absolute_path(relative_path: str):
    """
    Get absolute path to resource.
    
    Needed to properly bundle external files with PyInstaller.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS.
        # Some systems may support _MEIPASS2 instead.
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
