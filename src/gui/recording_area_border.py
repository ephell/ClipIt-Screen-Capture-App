import threading

import win32api, win32con, win32gui


class RecordingAreaBorder:

    def __init__(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.bottom_right_x = bottom_right_x
        self.bottom_right_y = bottom_right_y
        self.hwnd = self.__generate_hwnd(
            top_left_x=self.top_left_x,
            top_left_y=self.top_left_y,
            width=self.bottom_right_x - self.top_left_x,
            height=self.bottom_right_y - self.top_left_y
        )
        self.__create_border_region (self.hwnd)
        self.__set_opacity(self.hwnd, 255)
        self.__set_color(self.hwnd)
        self.__set_always_on_top(self.hwnd)
        self.__show_window(self.hwnd)
        
    def run(self):
        """Listen for window messages until the window is destroyed."""
        win32gui.PumpMessages()

    def __generate_hwnd(self, top_left_x, top_left_y, width, height):
        message_handler = {
            win32con.WM_DESTROY: self.__on_destroy,
            win32con.WM_PAINT: self.__on_paint
        }
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = message_handler
        wc.lpszClassName = "BorderClass"
        win32gui.RegisterClass(wc)
        hwnd = win32gui.CreateWindowEx(
            # ToDo: Uncomment second tag' to hide the window from the taskbar.
            win32con.WS_EX_LAYERED, #| win32con.WS_EX_TOOLWINDOW
            "BorderClass",
            "RECORDING AREA BORDER",
            win32con.WS_VISIBLE | win32con.WS_POPUP,
            top_left_x,
            top_left_y,
            width,
            height,
            0,
            0,
            win32api.GetModuleHandle(None),
            None
        )
        return hwnd

    def __create_border_region(self, hwnd):
        """
        Modify the window region of the given window handle `hwnd` to 
        remove the interior area and leave only a border. 
        
        Specifically, this method creates a round rectangular region 
        covering the entire window area, then subtracts another round 
        rectangular region with smaller dimensions to carve out the 
        interior border. The resulting region is then set as the new 
        window region for `hwnd`.
        """
        border_width = 2
        x0, y0, x1, y1 = win32gui.GetClientRect(hwnd)
        region = win32gui.CreateRoundRectRgn(x0, y0, x1, y1, 0, 0)
        exclude = win32gui.CreateRoundRectRgn(
            x0 + border_width, 
            y0 + border_width, 
            x1 - border_width, 
            y1 - border_width, 
            0, 
            0
        )
        win32gui.CombineRgn(region, region, exclude, win32con.RGN_DIFF)
        win32gui.SetWindowRgn(hwnd, region, True)

    def __set_opacity(self, hwnd, opacity):
        win32gui.SetLayeredWindowAttributes(hwnd, 0, opacity, win32con.LWA_ALPHA)

    def __set_color(self, hwnd):
        """Post a WM_PAINT message to the given window handle `hwnd`."""
        win32gui.UpdateWindow(hwnd)

    def __set_always_on_top(self, hwnd):
        win32gui.SetWindowPos(
            hwnd, 
            win32con.HWND_TOPMOST,
            0, 
            0, 
            0, 
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

    def __show_window(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    def __on_paint(self, hwnd, message, wparam, lparam):
        """Callback for the WM_PAINT message."""
        hdc, paint_struct = win32gui.BeginPaint(hwnd)
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        print(left, top, right, bottom)
        brush = win32gui.CreateSolidBrush(win32api.RGB(30, 200, 30))
        win32gui.FillRect(hdc, (left, top, right, bottom), brush)
        win32gui.EndPaint(hwnd, paint_struct)
        return 0

    def __on_destroy(self, hwnd, message, wparam, lparam):
        """Callback for the WM_DESTROY message."""
        win32gui.PostQuitMessage(0)
        return True
