import tkinter as tk

import mss
from PIL import Image, ImageTk, ImageEnhance


class MousePositionTracker:

    def __init__(self, canvas):
        self.canvas = canvas
        self.left_click_coords = None
        self.left_drag_coords = None
        self.reset()

    def get_selection_coords(self):
        return (self.left_click_coords, self.left_drag_coords)

    def __on_left_mouse_click(self, event):
        self.left_click_coords = (event.x, event.y)  

    def __on_left_mouse_drag(self, event):
        self.left_drag_coords = (event.x, event.y)
        # User callback.
        self._command(self.left_click_coords, self.left_drag_coords) 

    def reset(self):
        self.left_click_coords = self.left_drag_coords = None

    def autodraw(self, command=lambda *args: None):
        """Setup automatic drawing; supports command option"""
        self.reset()
        self._command = command
        self.canvas.bind("<Button-1>", self.__on_left_mouse_click)
        self.canvas.bind("<B1-Motion>", self.__on_left_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.quit)

    def quit(self, event):
        self.reset()


class SelectionAreaDrawer:
    """Widget to display a rectangular selection area on a canvas."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.selection_area = self.canvas.create_rectangle(
            0, 
            0, 
            0, 
            0, 
            dash=(2, 2),
            outline="white",
            state=tk.HIDDEN
        )

    def draw(self, start, end):
        """Draw a rectangular area on the canvas."""
        x0, y0, x1, y1 = self.__get_coords(start, end)
        self.canvas.coords(self.selection_area, x0, y0, x1, y1),
        self.canvas.itemconfigure(self.selection_area, state=tk.NORMAL)

    def __get_coords(self, start, end):
        """ 
        Determine top left and bottom right coordinates of the selection
        area.
        """
        return (min((start[0], end[0])), min((start[1], end[1])),
                max((start[0], end[0])), max((start[1], end[1])))


class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.root.bind("<Escape>", func=self.__close_window)
        self.root.title("Region Selector")
        # self.root.geometry(f"{1920}x{800}")
        self.root.overrideredirect(True)
        self.root.configure(background="grey")

        with mss.mss() as sct:
            screenshot = Image.open(sct.shot(mon=-1))
            enhancer = ImageEnhance.Brightness(screenshot)
            screenshot = enhancer.enhance(0.7)

        self.root.geometry(f"{screenshot.width}x{screenshot.height}+0+0")

        self.screenshot = ImageTk.PhotoImage(screenshot)
        self.canvas = tk.Canvas(
            master=self.root,
            width=self.screenshot.width(),
            height=self.screenshot.height(),
            borderwidth=0,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.image = self.screenshot
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas.image)

        # Create selection object to show current selection boundaries.
        self.selection_area = SelectionAreaDrawer(self.canvas)

        # Callback function to update it given two points of its diagonal.
        def on_drag(start, end):  # Must accept these arguments.
            self.selection_area.draw(start, end)

        # Create mouse position tracker that uses the function.
        self.posn_tracker = MousePositionTracker(self.canvas)
        self.posn_tracker.autodraw(command=on_drag)  # Enable callbacks.

    def run(self):
        self.root.mainloop()

    def __close_window(self, event):
        self.root.destroy()

if __name__ == '__main__':
    app = Application()
    app.run()




