import tkinter as tk
from .canvas import Canvas
from .sidebar import Sidebar


class Board(tk.Frame):

    # Initialize empty board, UI sidebar
    def __init__(self, master=None, height=0, width=0):
        super().__init__(master, width=width, height=height)
        self.master = master

        self.height = height
        self.width = width

        self.canvas = Canvas(self, width=int(width*0.8), height=height)
        self.canvas.pack(side=tk.LEFT)

        self.sidebar = Sidebar(self, width=int(width*0.2), height=height)
        self.sidebar.pack(side=tk.LEFT)

        self.pack()
