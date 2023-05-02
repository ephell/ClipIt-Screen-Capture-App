import win32api, win32con, win32gui


class RecordingAreaBorder:

    def __init__(self):
        win32gui.InitCommonControls()

        # Add 'win32con.WS_EX_TOOLWINDOW' to hide the window from the taskbar.
        dwExStyle = win32con.WS_EX_LAYERED #| win32con.WS_EX_TOOLWINDOW
        lpClassName = "MyWndClass"
        lpWindowName = "WINDOW"
        dwStyle = win32con.WS_VISIBLE | win32con.WS_POPUP
        top_left_x = 0
        top_left_y = 0
        nWidth = 800
        nHeight = 800
        hwndParent = 0
        hMenu = 0
        hInstance = win32api.GetModuleHandle(None)
        lpParam = None

        message_handler = {
            win32con.WM_DESTROY: self.__on_destroy,
            win32con.WM_PAINT: self.__on_paint
        }
        wc = win32gui.WNDCLASS()
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
        self.__carve_out_border(self.hwnd)
        self.__set_border_always_on_top(self.hwnd)
        win32gui.SetLayeredWindowAttributes(self.hwnd, 0, 255, win32con.LWA_ALPHA)
        win32gui.UpdateWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

    def __carve_out_border(self, hwnd):
        """
        Modify the window region of the given window handle `hwnd` to 
        remove the interior area and leave only a border. 
        
        Specifically, this method creates a round rectangular region 
        covering the entire window area, then subtracts another round 
        rectangular region with smaller dimensions to carve out the 
        interior border. The resulting region is then set as the new 
        window region for `hwnd`.
        """
        region = win32gui.CreateRoundRectRgn(0, 0, 800, 800, 0, 0)
        exclude = win32gui.CreateRoundRectRgn(3, 3, 797, 797, 0, 0)
        win32gui.CombineRgn(region, region, exclude, win32con.RGN_DIFF)
        win32gui.SetWindowRgn(hwnd, region, True)

    def __set_border_always_on_top(self, hwnd):
        win32gui.SetWindowPos(
            hwnd, 
            win32con.HWND_TOPMOST,
            0, 
            0, 
            0, 
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
        )

    def __on_paint(self, hwnd, message, wparam, lparam):
        """Fill the window background with a solid color."""
        hdc, paint_struct = win32gui.BeginPaint(hwnd)
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        brush = win32gui.CreateSolidBrush(win32api.RGB(30, 200, 30))
        win32gui.FillRect(hdc, (left, top, right, bottom), brush)
        win32gui.EndPaint(hwnd, paint_struct)
        return 0

    def __on_destroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True


w = RecordingAreaBorder()
win32gui.PumpMessages()
