import tkinter as tk
import numpy as np
from .pixel import Pixel


class Canvas(tk.Canvas):
    def __init__(self, master=None, width=0, height=0):
        super().__init__(master=master, width=width, height=height)
        self.pack()

        self.width = width
        self.height = height

        # self.array = np.empty((height, width), np.int)
        # print(self.array)
