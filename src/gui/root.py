from tkinter import *
from capture_area_selection import AreaSelector


class App:

    def __init__(self):
        self.root = Tk()
        self.root.attributes('-alpha', 1.0)

        self.width, self.height = 250, 150
        self.root.geometry(f"{self.width}x{self.height}")

        self.area_selector = AreaSelector(self.root)
        self.button_record = Button(
            self.root, 
            width=20,
            height=5,
            text="Record", 
            command=self.area_selector.start
        )
        # ToDo: Figure out how to get all packed widget info so that
        # they can be hidden when selecting the region.
        # self.button_record.pack()
        self.button_record.place(anchor=CENTER, x=self.width//2, y=self.height // 2)
        self.root.bind("<Escape>", func=lambda event: self.root.destroy())

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
