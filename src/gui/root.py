from tkinter import *
from region_selection import RegionSelector


class App:

    def __init__(self):
        self.root = Tk()
        self.root.attributes('-alpha', 1.0)

        self.width, self.height = 250, 150
        self.root.geometry(f"{self.width}x{self.height}")

        # Make sure width and height are updated.
        self.root.update()

        self.region_selector = RegionSelector(self.root)
        self.button_record = Button(
            self.root, 
            width=20,
            height=5,
            text="Record", 
            command=self.region_selector.select_region
        )
        # ToDo: Figure out how to get all packed widget info so that
        # they can be hidden when selecting the region.
        # self.button_record.pack()
        self.button_record.place(anchor=CENTER, x=self.width//2, y=self.height // 2)
        self.root.bind("<Escape>", func=self.__close_window)

    def run(self):
        self.root.mainloop()

    def __close_window(self, event):
        self.root.destroy()

if __name__ == '__main__':
    app = App()
    app.run()
