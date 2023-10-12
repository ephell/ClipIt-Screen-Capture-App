import random
import string
import threading

import win32api, win32con, win32gui


class AreaBorderCreator(threading.Thread):

    def __init__(
            self, 
            top_left_x, 
            top_left_y,
            bottom_right_x, 
            bottom_right_y,
            color: tuple
        ):
        super().__init__()
        self.daemon = True
        self.hwnd = None
        self.border_width = 1
        self.top_left_x = int(top_left_x) - self.border_width
        self.top_left_y = int(top_left_y) - self.border_width
        self.bottom_right_x = int(bottom_right_x) + self.border_width + 1
        self.bottom_right_y = int(bottom_right_y) + self.border_width + 1
        self.color = color

    def run(self):
        """
        Create the border and start listening for messages. 
        
        Window creation must be done in the thread and not in the 
        constructor because to be able to listen for messages the 
        thread must own the window. If the window is created in the
        constructor, the thread that initialized the object will own
        the window instead and the messages will not be received.
        """
        self.hwnd = self.__create_window(
            top_left_x=self.top_left_x,
            top_left_y=self.top_left_y,
            width=self.bottom_right_x - self.top_left_x,
            height=self.bottom_right_y - self.top_left_y
        )
        self.__crop_window(self.hwnd)
        self.__set_opacity(self.hwnd, 255)
        self.__set_color(self.hwnd)
        self.__set_always_on_top(self.hwnd)
        self.__show_window(self.hwnd)
        win32gui.PumpMessages()

    def destroy(self):
        win32gui.SendMessage(self.hwnd, win32con.WM_QUIT, 0, 0)
        return True

    def update_color(self, color):
        win32gui.InvalidateRect(self.hwnd, None, True)
        self.color = color
        self.__set_color(self.hwnd)

    def __generate_class_name(self):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(20))

    def __create_window(self, top_left_x, top_left_y, width, height):
        message_handler = {
            win32con.WM_PAINT: self.__on_paint,
            win32con.WM_QUIT: self.__on_quit
        }
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = message_handler
        wc.lpszClassName = self.lpszClassName = self.__generate_class_name()
        win32gui.RegisterClass(wc)
        hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TOOLWINDOW,
            self.lpszClassName,
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

    def __crop_window(self, hwnd):
        """
        Modify the window region of the given window handle `hwnd` to 
        remove the interior area and leave only a custom border.
        
        Specifically, this method creates a round rectangular region 
        covering the entire window area, then subtracts another round 
        rectangular region with smaller dimensions to carve out the 
        interior border. The resulting region is then set as the new 
        window region for `hwnd`.
        """
        x0, y0, x1, y1 = win32gui.GetClientRect(hwnd)
        region = win32gui.CreateRoundRectRgn(x0, y0, x1, y1, 0, 0)
        exclude = win32gui.CreateRoundRectRgn(
            x0 + self.border_width, 
            y0 + self.border_width, 
            x1 - self.border_width, 
            y1 - self.border_width, 
            0, 
            0
        )
        win32gui.CombineRgn(region, region, exclude, win32con.RGN_DIFF)
        win32gui.SetWindowRgn(hwnd, region, True)

    def __set_opacity(self, hwnd, opacity):
        win32gui.SetLayeredWindowAttributes(hwnd, 0, opacity, win32con.LWA_ALPHA)

    def __set_color(self, hwnd):
        """Post a WM_PAINT message."""
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
        brush = win32gui.CreateSolidBrush(win32api.RGB(*self.color))
        win32gui.FillRect(hdc, (left, top, right, bottom), brush)
        win32gui.EndPaint(hwnd, paint_struct)
        return 0

    def __on_quit(self, hwnd, message, wparam, lparam):
        """Callback for the WM_QUIT message."""
        win32gui.PostQuitMessage(0)
        return True
