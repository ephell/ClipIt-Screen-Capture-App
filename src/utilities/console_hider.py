import threading

import win32gui
import win32con


class ConsoleHider(threading.Thread):

    def __init__(self, console_title: str):
        super().__init__()
        self.console_title = console_title

    def run(self):
        while True:
            hwnd = self.__get_hwnd(self.console_title)
            if hwnd is not None and hwnd != 0:
                self.__make_fully_transparent(hwnd)
                self.__make_clickthrough(hwnd)
                self.__disable_input(hwnd)
                self.__hide_from_taskbar(hwnd)
                break

    def __get_hwnd(self, title):
        return win32gui.FindWindowEx(None, None, None, title) or None

    def __make_fully_transparent(self, hwnd):
        win32gui.SetWindowLong(
            hwnd, 
            win32con.GWL_EXSTYLE, 
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
        )
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA)

    def __make_clickthrough(self, hwnd):
        win32gui.SetWindowLong(
            hwnd, 
            win32con.GWL_EXSTYLE, 
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT
        )
        win32gui.EnableWindow(hwnd, False)

    def __disable_input(self, hwnd):
        win32gui.EnableWindow(hwnd, False)

    def __hide_from_taskbar(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        win32gui.SetWindowLong(
            hwnd, 
            win32con.GWL_EXSTYLE, 
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOOLWINDOW
        )
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
