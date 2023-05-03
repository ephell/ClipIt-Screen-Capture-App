import tkinter as tk

import mss
from PIL import Image, ImageTk, ImageEnhance


class AreaSelector:

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
        self.left_click_coords = None
        self.left_drag_coords = None

    def start(self):
        self.canvas.bind("<Button-1>", self.__on_left_mouse_click)
        self.canvas.bind("<B1-Motion>", self.__on_left_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.__on_left_mouse_release)

    def get_selection_coords(self):
        return (self.left_click_coords, self.left_drag_coords)

    def __on_left_mouse_click(self, event):
        self.left_click_coords = (event.x, event.y)  

    def __on_left_mouse_drag(self, event):
        self.left_drag_coords = (event.x, event.y)
        self.__draw(self.left_click_coords, self.left_drag_coords) 

    def __on_left_mouse_release(self, event):
        print(self.get_selection_coords())

    def __draw(self, start, end):
        x0, y0, x1, y1 = self.__determine_corners(start, end)
        self.canvas.coords(self.selection_area, x0, y0, x1, y1),
        self.canvas.itemconfigure(self.selection_area, state=tk.NORMAL)

    def __determine_corners(self, start, end):
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

        self.sa = AreaSelector(self.canvas)
        self.sa.start()

    def run(self):
        self.root.mainloop()

    def __close_window(self, event):
        self.root.destroy()

if __name__ == '__main__':
    app = Application()
    app.run()




