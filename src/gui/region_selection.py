from tkinter import *


class RegionSelector:

    def __init__(self, root):
        self.root = root

        self.all_widget_info = self.root.winfo_children()
        print(self.all_widget_info)

        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()

    def restore_original_attributes(self, event):
        # self.__restore_all_widgets()
        self.root.bind("<Escape>", func=self.__close_window) 
        self.root.geometry(f"{self.width}x{self.height}")
        # ToDo: Don't use normal to restore the window. Move the window
        # back manually to original position, width and height.
        self.root.state("normal")
        self.root.attributes('-alpha', 1.0)
        self.root.attributes('-topmost', False)
        self.root.overrideredirect(False)
        # Make sure it's impossible to draw a rectangle again.
        self.canvas.pack_forget()

    def __close_window(self, event):
        self.root.destroy()

    def select_region(self):
        # self.__remove_all_widgets()
        self.canvas = Canvas(self.root)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", func=self.__on_button_press)
        self.canvas.bind("<B1-Motion>", func=self.__on_move_press)
        self.canvas.bind("<ButtonRelease-1>", func=self.__on_button_release)
        self.root.bind("<Escape>", func=self.restore_original_attributes)
        self.root.geometry(f"{1920}x{1080}")
        # ToDo: Don't use zoomed to fill out the entire screen. Move
        # the window to x0, y0 and set the width and height to the
        # width and height of the screen (all screens if there are
        # multiple).
        self.root.wm_state('zoomed')
        self.root.attributes('-alpha', 0.5)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)

    def __on_button_press(self, event):
        self.canvas.start_x = event.x
        self.canvas.start_y = event.y

    def __on_move_press(self, event):
        self.canvas.delete("rect")
        self.canvas.create_rectangle(
            self.canvas.start_x, 
            self.canvas.start_y, 
            event.x, 
            event.y, 
            fill='', 
            outline='red',
            width=3, 
            tags="rect"
        )

    def __on_button_release(self, event):
        self.canvas.create_rectangle(
            self.canvas.start_x, 
            self.canvas.start_y, 
            event.x, 
            event.y,
            fill='', 
            width=3, 
            outline='red', 
            tags="rect"
        )
        # Save the coordinates of the rectangle
        x1 = min(self.canvas.start_x, event.x)
        y1 = min(self.canvas.start_y, event.y)
        x2 = max(self.canvas.start_x, event.x)
        y2 = max(self.canvas.start_y, event.y)
        self.rect_coords = (x1, y1, x2, y2)
        self.canvas.delete("rect")
        self.canvas.pack_forget()
        self.restore_original_attributes(event=None)
        print(self.rect_coords)

    def __remove_all_widgets(self):
        for widget in self.all_widget_info:
            widget.destroy()

    def __restore_all_widgets(self):
        for widget in self.all_widget_info:
            widget.pack()
