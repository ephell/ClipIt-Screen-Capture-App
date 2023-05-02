import win32api, win32con, win32gui


class RecordingAreaBorder:

    def __init__(self):
        win32gui.InitCommonControls()

        # Add 'win32con.WS_EX_TOOLWINDOW' to hide the window from the taskbar.
        dwExStyle = win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW
        lpClassName = "MyWndClass"
        lpWindowName = "WINDOW"
        dwStyle = win32con.WS_VISIBLE | win32con.WS_POPUP | win32con.WS_BORDER
        top_left_x = 0
        top_left_y = 0
        nWidth = 800
        nHeight = 800
        hwndParent = 0
        hMenu = 0
        hInstance = win32api.GetModuleHandle(None)
        lpParam = None

        message_handler = {win32con.WM_DESTROY: self.__on_destroy}
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = message_handler
        wc.lpszClassName = lpClassName
        win32gui.RegisterClass(wc)

        self.hwnd = win32gui.CreateWindowEx(
            dwExStyle,
            lpClassName,
            lpWindowName,
            dwStyle,
            top_left_x,
            top_left_y,
            nWidth,
            nHeight,
            hwndParent,
            hMenu,
            hInstance,
            lpParam
        )
        self.__set_window_region(self.hwnd)
        self.__set_window_always_on_top(self.hwnd)
        win32gui.SetLayeredWindowAttributes(self.hwnd, 0, 128, win32con.LWA_ALPHA)
        win32gui.UpdateWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def __set_window_always_on_top(self, hwnd):
        win32gui.SetWindowPos(
            hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
        )

    def __set_window_region(self, hwnd):
        region = win32gui.CreateRoundRectRgn(0, 0, 800, 800, 0, 0)
        exclude = win32gui.CreateRoundRectRgn(10, 10, 790, 790, 0, 0)
        win32gui.CombineRgn(region, region, exclude, win32con.RGN_DIFF)
        win32gui.SetWindowRgn(hwnd, region, True)

    def __on_destroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True


w = RecordingAreaBorder()
win32gui.PumpMessages()
