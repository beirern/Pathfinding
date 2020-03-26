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
        self.sidebar.load_button.bind('<Button-1>', self.loadLevel)
        self.sidebar.wall.bind('<Button-1>', self.set_wall)
        self.sidebar.waypoint.bind('<Button-1>', self.set_waypoint)
        self.sidebar.editable.bind('<Button-1>', self.set_editable)
        self.sidebar.player.bind('<Button-1>', self.set_player)
        self.sidebar.enemy.bind('<Button-1>', self.set_enemy)

        self.pack()

    def saveLevel(self, event):
        file = open('Level1.txt', 'w')
        enemy = self.canvas.enemy
        player = self.canvas.player
        walls = self.canvas.walls
        waypoints = self.canvas.waypoints
        file.write(str(player) + '\n')

        file = open('Level1.txt', 'a')
        file.write(str(enemy) + '\n')

        file.write('Walls:')
        for wall in walls:
            file.write('\n' + str(wall))

        file.write('\n' + 'Waypoints:')
        for waypoint in waypoints:
            file.write('\n' + str(waypoint))

        file.close()

    def loadLevel(self, event):
        file = open('Level1.txt', 'r')
        lines = file.readlines()

        if self.sidebar.v1.get() == 0:
            self.sidebar.v1.set(1)
        elif self.sidebar.v1.get() == 1:
            self.sidebar.v1.set(0)

        self.canvas.load_level(lines)

    def set_wall(self, event):
        self.canvas.object = 'WALL'

    def set_waypoint(self, event):
        self.canvas.object = 'WAYPOINT'

    def set_player(self, event):
        self.canvas.object = 'PLAYER'

    def set_enemy(self, event):
        self.canvas.object = 'ENEMY'

    def set_editable(self, event):
        self.canvas.set_editable()
