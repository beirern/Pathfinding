import tkinter as tk
import numpy as np
from .pixel import Pixel

# TODO
# Remove the draw method and replace with a method for click and for release
# Figure out design for array, having 1 array or one grid array and one wall array...


class Canvas(tk.Canvas):
    def __init__(self, master=None, width=0, height=0):
        super().__init__(master=master, width=width, height=height)
        self.pack()

        self.rect = None

        self.width = width
        self.height = height

        self.walls = []

        self.bind("<B1-Motion>", self.draw)
        self.bind("<Button-1>", self.draw)

        # self.array = np.empty((height, width), np.int)
        # print(self.array)

    def draw(self, event):
        if event.state == 0:
            self.start_x = event.x
            self.start_y = event.y
        elif event.state == 256:
            self.end_x = event.x
            self.end_y = event.y
            self.create_rectangle(self.start_x, self.start_y,
                                  self.end_x, self.end_y, fill="black")
            self.walls.append(
                [self.start_x, self.start_y, self.end_x, self.end_y])

    def test2(self, event):
        print('Hi:', event.x)
