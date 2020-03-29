import tkinter as tk
from .functions import buttonOneClick, buttonOneMotion, buttonOneRelease, clearAll, clearLast, load, draw_walls, draw_waypoints, hide_waypoints
from .enemy import Enemy
from .player import Player
from .shape import Shape
from .pathfinding import AstarGraph
from .pathfinding import Pixel
from .pathfinding import PathfinderSolver
from .pathfinding import KDTree


class Canvas(tk.Canvas):
    def __init__(self, master=None, width=0, height=0):
        super().__init__(master=master, width=width, height=height)
        self.pack()

        # Holds whether WALL or WAYPOINT
        self.object = 'PLAYER'

        # Whether to allow editing
        self.editable = True

        self.currRect = None

        self.width = width
        self.height = height

        self.walls = []
        self.waypoints = {}

        # Set up array of Pixels
        self.pixels = []
        for i in range(self.height):
            self.pixels.append([])
            for j in range(self.width):
                self.pixels[-1].append(Pixel(j,
                                             i, i * len(self.pixels[0]) + j, True))

        # Bind everything
        # Bind and Unbind Tab to hold variable
        self.start_game = None
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.set_binds()

        self.player = None
        self.enemy = None

    def set_binds(self):
        # Left Click for making Objects
        self.left_click = self.bind(
            "<Button-1>", lambda event: buttonOneClick(self, event))
        self.left_motion = self.bind(
            "<B1-Motion>", lambda event: buttonOneMotion(self, event))
        self.left_release = self.bind(
            "<ButtonRelease-1>", lambda event: buttonOneRelease(self, event))

        # Right Click Deletes Objects
        self.right_click = self.bind(
            '<Button-3>', lambda event: clearLast(self, event))
        self.right_double_click = self.bind(
            '<Double-Button-3>', lambda event: clearAll(self, event))

        # Unbind Tab (opposite to mouse binds)
        self.unbind('<Tab>', self.start_game)
        self.unbind('<Up>', self.up)
        self.unbind('<Down>', self.down)
        self.unbind('<Left>', self.left)
        self.unbind('<Right>', self.right)

    def set_unbinds(self):
        if self.left_click != None:
            # Unbind Left Click
            self.unbind('<Button-1>', self.left_click)
            self.unbind('<B1-Motion>', self.left_motion)
            self.unbind('<ButtonRelease-1>', self.left_release)

            # Unbind Right Click
            self.unbind('<Button-3>', self.right_click)
            self.unbind('<Double-Button-3>', self.right_double_click)

        # Tab to Start Game (Works opposite of mouse binds)
        self.start_game = self.bind('<Tab>', self.startGame)
        self.up = self.bind('<Up>', self.move_up)
        self.down = self.bind('<Down>', self.move_down)
        self.left = self.bind('<Left>', self.move_left)
        self.right = self.bind('<Right>', self.move_right)

    def load_level(self, lines):
        load(self, lines)

    def startGame(self, event):
        if self.player != None and self.enemy != None:
            kdtree = KDTree(self.pixels, self.waypoints)
            self.astar(kdtree.nearest(self.pixels[self.player.shape.y1 + self.player.shape.height][self.player.shape.x1 + self.player.shape.width]),
                       kdtree.nearest(self.pixels[self.enemy.shape.y1 + self.enemy.shape.height][self.enemy.shape.x1 + self.enemy.shape.width]))

    def astar(self, start, end):
        graph = AstarGraph(self.pixels, self.waypoints)
        pathfinder = PathfinderSolver(graph)
        result = pathfinder.findShortestPath(start, end)

        if result.outcome == "SOLVED":
            print("DONE")
            self.print_path(result.solution)
        elif result.outcome == "UNSOLVABLE":
            print("Unsolvable!")
        else:
            print("Timed Out!")

    def print_path(self, solution):
        self.create_line(self.player.shape.x1 + self.player.shape.width,
                         self.player.shape.y1 + self.player.shape.height, solution[0].x, solution[0].y)
        for i in range(len(solution) - 1):
            self.create_line(solution[i].x, solution[i].y,
                             solution[i+1].x, solution[i+1].y)
        self.create_line(solution[len(solution) - 1].x, solution[len(solution) - 1].y,
                         self.enemy.shape.x1 + self.enemy.shape.width, self.enemy.shape.y1 + self.enemy.shape.height)

    def set_editable(self):
        self.editable = not self.editable

        if self.editable:
            self.set_binds()
            draw_waypoints(self)
        else:
            self.set_unbinds()
            hide_waypoints(self)

    # Move Up
    def move_up(self, event):
        self.delete(self.player.shape.canvas_id)
        player = self.player.shape
        player.y1 = player.y1 - 10
        player.y2 = player.y2 - 10
        new_player = self.create_rectangle(
            player.x1, player.y1, player.x2, player.y2, width=1, fill="green")
        self.player.shape.canvas_id = new_player

    # Move Down
    def move_down(self, event):
        self.delete(self.player.shape.canvas_id)
        player = self.player.shape
        player.y1 = player.y1 + 10
        player.y2 = player.y2 + 10
        new_player = self.create_rectangle(
            player.x1, player.y1, player.x2, player.y2, width=1, fill="green")
        self.player.shape.canvas_id = new_player

    # Move Left
    def move_left(self, event):
        self.delete(self.player.shape.canvas_id)
        player = self.player.shape
        player.x1 = player.x1 - 10
        player.x2 = player.x2 - 10
        new_player = self.create_rectangle(
            player.x1, player.y1, player.x2, player.y2, width=1, fill="green")
        self.player.shape.canvas_id = new_player

    # Move Right
    def move_right(self, event):
        self.delete(self.player.shape.canvas_id)
        player = self.player.shape
        player.x1 = player.x1 + 10
        player.x2 = player.x2 + 10
        new_player = self.create_rectangle(
            player.x1, player.y1, player.x2, player.y2, width=1, fill="green")
        self.player.shape.canvas_id = new_player
