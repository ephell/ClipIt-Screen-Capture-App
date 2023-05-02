import win32api, win32con, win32gui

class MyWindow:

    def __init__(self):
        win32gui.InitCommonControls()

        dwExStyle = win32con.WS_EX_LAYERED
        lpClassName = "MyWndClass"
        lpWindowName = "WINDOW"
        dwStyle = win32con.WS_POPUP | win32con.WS_VISIBLE | win32con.WS_THICKFRAME
        top_left_x = 0
        top_left_y = 0
        nWidth = 500
        nHeight = 500
        hwndParent = 0
        hMenu = 0
        hInstance = win32api.GetModuleHandle(None)
        lpParam = None

        message_map = {
            win32con.WM_DESTROY: self.__on_destroy,
            win32con.WM_NCHITTEST: self.__on_nchittest,
        }
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = message_map
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
        win32gui.SetLayeredWindowAttributes(self.hwnd, 0, 128, win32con.LWA_ALPHA)
        win32gui.UpdateWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def __on_destroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True

    def __on_nchittest(self, hwnd, message, wparam, lparam):
        x, y = win32api.LOWORD(lparam), win32api.HIWORD(lparam)
        if self.__is_point_in_client_rect(x, y):
            return win32con.HTTRANSPARENT
        else:
            return win32con.HTCLIENT

    def __is_point_in_client_rect(self, x, y):
        rect = win32gui.GetClientRect(self.hwnd)
        left, top, right, bottom = rect
        return left <= x < right and top <= y < bottom

w = MyWindow()
win32gui.PumpMessages()
