import ctypes
import threading
from time import perf_counter, sleep

import win32gui
import win32con


class ConsoleHider(threading.Thread):

    def __init__(self):
        super().__init__()
        self.setDaemon(True)
        self.__console_title = "ClipIt-Console"
        ctypes.windll.kernel32.SetConsoleTitleW(self.__console_title)
        self.__thread_timeout = 30
        self.__is_hidden_hwnd_kernel32 = False
        self.__is_hidden_hwnd_win32gui = False

    def run(self):
        start_time = perf_counter()
        while perf_counter() - start_time <= self.__thread_timeout:
            if not self.__is_hidden_hwnd_kernel32:
                self.__hide(ctypes.windll.kernel32.GetConsoleWindow())
                self.__is_hidden_hwnd_kernel32 = True
            if not self.__is_hidden_hwnd_win32gui:
                hwnd = self.__get_hwnd(self.__console_title)
                if hwnd is not None and hwnd != 0:
                    self.__hide(hwnd)
                    self.__is_hidden_hwnd_win32gui = True
            if self.__is_hidden_hwnd_kernel32 and self.__is_hidden_hwnd_win32gui:
                break
            sleep(0.25)
            
    def __hide(self, hwnd):
        self.__make_fully_transparent(hwnd)
        self.__make_clickthrough(hwnd)
        self.__disable_input(hwnd)
        self.__hide_from_taskbar(hwnd)

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
