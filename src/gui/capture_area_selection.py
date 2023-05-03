import tkinter as tk

import mss
from PIL import Image, ImageTk, ImageEnhance


class AreaSelector:

    def __init__(self, root):
        self.root = root
        self.left_click_coords = None
        self.left_drag_coords = None
        self.canvas = None
        self.selection_area = None
        self.original_root_x = None
        self.original_root_y = None
        self.original_root_width = None
        self.original_root_height = None

    def start(self):
        self.root.overrideredirect(True)
        self.canvas = self.__initialize_canvas(self.root)
        self.__assign_binds(self.root, self.canvas)
        self.__save_root_dimensions(self.root)

    def get_selection_coords(self):
        return (self.left_click_coords, self.left_drag_coords)

    def __initialize_canvas(self, root):
        with mss.mss() as sct:
            screenshot = Image.open(sct.shot(mon=-1))
        enhancer = ImageEnhance.Brightness(screenshot)
        screenshot = enhancer.enhance(0.7)
        screenshot = ImageTk.PhotoImage(screenshot)
        root.geometry(f"{screenshot.width()}x{screenshot.height()}+0+0")
        canvas = tk.Canvas(
            master=root,
            width=screenshot.width(),
            height=screenshot.height(),
            borderwidth=0,
            highlightthickness=0
        )
        canvas.image = screenshot
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)
        self.selection_area = canvas.create_rectangle(
            0, 
            0, 
            0, 
            0, 
            dash=(2, 2),
            outline="white",
            state=tk.HIDDEN
        )
        canvas.pack(fill=tk.BOTH, expand=True)
        return canvas

    def __assign_binds(self, root, canvas):
        canvas.bind("<Button-1>", self.__on_left_mouse_click)
        canvas.bind("<B1-Motion>", self.__on_left_mouse_drag)
        canvas.bind("<ButtonRelease-1>", self.__on_left_mouse_release)
        root.bind("<Escape>", func=self.__on_escape)

    def __save_root_dimensions(self, root):
        self.original_root_x = root.winfo_x()
        self.original_root_y = root.winfo_y()
        self.original_root_width = root.winfo_width()
        self.original_root_height = root.winfo_height()

    def __on_left_mouse_click(self, event):
        self.left_click_coords = (event.x, event.y)  

    def __on_left_mouse_drag(self, event):
        self.left_drag_coords = (event.x, event.y)
        self.__draw(self.left_click_coords, self.left_drag_coords) 

    def __on_left_mouse_release(self, event):
        print(self.get_selection_coords())
        self.canvas.destroy()
        self.__restore_root_attributes()
        print(self.original_root_x, self.original_root_y)
        print(self.original_root_width, self.original_root_height)

    def __on_escape(self, event):
        self.__restore_root_attributes()
        self.canvas.destroy()

    def __restore_root_attributes(self):
        self.root.geometry(
            f"{self.original_root_width}x{self.original_root_height}"
            f"+{self.original_root_x}+{self.original_root_y}"
        )
        self.root.overrideredirect(False)
        self.root.bind("<Escape>", func=lambda event: self.root.destroy())

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

        self.sa = AreaSelector(self.root)
        self.sa.start()

    def run(self):
        self.root.mainloop()

    def __close_window(self, event):
        self.root.destroy()

if __name__ == '__main__':
    app = Application()
    app.run()




