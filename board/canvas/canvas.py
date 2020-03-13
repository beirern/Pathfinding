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

        self.currRect = None

        self.width = width
        self.height = height

        self.walls = []

        # Left Click for making Walls
        self.bind("<Button-1>", self.buttonOneClick)
        self.bind("<B1-Motion>", self.buttonOneMotion)
        self.bind("<ButtonRelease-1>", self.buttonOneRelease)

        # Right Click Deletes Walls
        self.bind("<Button-3>", self.clearLast)
        self.bind("<Double-Button-3>", self.clearAll)

    # Get start x and y on Click
    def buttonOneClick(self, event):
        self.currRect = None
        self.start_x = event.x
        self.start_y = event.y

    # Draw Rectangle as curser is moving

    def buttonOneMotion(self, event):
        if (self.currRect):
            self.delete(self.currRect)
        self.end_x = event.x
        self.end_y = event.y
        self.currRect = self.create_rectangle(self.start_x, self.start_y,
                                              self.end_x, self.end_y, width=1, fill="blue")

    # Draw final wall and save it on Release
    def buttonOneRelease(self, event):
        if (self.currRect):
            self.delete(self.currRect)
        self.end_x = event.x
        self.end_y = event.y
        self.currRect = self.create_rectangle(self.start_x, self.start_y,
                                              self.end_x, self.end_y, width=1, fill="blue")
        self.walls.append(self.currRect)

    # Remove last Drawn Wall
    def clearLast(self, event):
        if (len(self.walls) > 0):
            self.delete(self.walls[-1])
            del self.walls[-1]

        # Removes all Walls
    def clearAll(self, event):
        if (len(self.walls) > 0):
            self.delete(tk.ALL)
            self.walls = []
