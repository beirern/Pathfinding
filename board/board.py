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

        self.sidebar.save_button.bind('<Button-1>', self.saveLevel)

        self.pack()

    def saveLevel(self, event):
        file = open("Level1.txt", "w")
        enemy = self.canvas.enemy
        player = self.canvas.player
        walls = self.canvas.walls
        file.write(str(enemy))

        file = open("Level1.txt", "a")
        file.write("\n" + str(player) + "\n")

        for wall in walls:
            file.write(str(wall))
