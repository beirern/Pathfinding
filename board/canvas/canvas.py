import tkinter as tk
from .functions import buttonOneClick, buttonOneMotion, buttonOneRelease, clearAll, clearLast, load, draw_walls, draw_waypoints, hide_waypoints, valid__movable_area
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
        self.unbind('<Return>', self.start_game)
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
        self.start_game = self.bind('<Return>', self.startGame)
        self.up = self.bind('<Up>', self.move_up)
        self.down = self.bind('<Down>', self.move_down)
        self.left = self.bind('<Left>', self.move_left)
        self.right = self.bind('<Right>', self.move_right)

    def load_level(self, lines):
        load(self, lines)

    def startGame(self, event):
        if self.player != None and self.enemy != None:
            self.kdtree = KDTree(self.pixels, self.waypoints)
            self.astar_graph = AstarGraph(self.pixels, self.waypoints)

            self.find_path()

    def find_path(self):
        start = self.kdtree.nearest(
            self.pixels[self.player.shape.y1][self.player.shape.x1])
        end = self.kdtree.nearest(
            self.pixels[self.enemy.shape.y1][self.enemy.shape.x1])
        pathfinder = PathfinderSolver(self.astar_graph)
        result = pathfinder.findShortestPath(start, end)

        if result.outcome == "SOLVED":
            print("DONE")
            solution = result.solution
            x = self.player.shape.x1
            y = self.player.shape.y1
            solution.insert(0, Pixel(x, y, self.pixels[y][x].index, True))
            self.print_path(solution)

            self.enemy.path = solution
            self.enemy.path_index = len(solution) - 1
            self.movement()
        elif result.outcome == "UNSOLVABLE":
            print("Unsolvable!")
        else:
            print("Timed Out!")

    def print_path(self, solution):
        for i in range(len(solution) - 1):
            self.create_line(solution[i].x, solution[i].y,
                             solution[i+1].x, solution[i+1].y)
        self.create_line(solution[len(solution) - 1].x, solution[len(solution) - 1].y,
                         self.enemy.shape.x1, self.enemy.shape.y1)

    def movement(self):
        if self.enemy.path[self.enemy.path_index].x <= self.enemy.shape.x1 + 3 and self.enemy.path[self.enemy.path_index].x >= self.enemy.shape.x1 - 3 and self.enemy.path[self.enemy.path_index].y <= self.enemy.shape.y1 + 3 and self.enemy.path[self.enemy.path_index].y >= self.enemy.shape.y1 - 3:
            self.enemy.path_index = self.enemy.path_index - 1

        if self.enemy.path_index != -1:
            rise = self.enemy.path[self.enemy.path_index].y - \
                self.enemy.shape.y1
            run = self.enemy.path[self.enemy.path_index].x - \
                self.enemy.shape.x1
            if run == 0:
                slope = rise
            else:
                slope = rise // run
            move_x = 0
            move_y = 0

            if (run < 0):
                move_x = -1
            elif run == 0:
                move_x = 0
            else:
                move_x = 1

            if (rise < 0):
                move_y = -1 * abs(slope)
            else:
                move_y = abs(slope)

            self.move(self.enemy.shape.canvas_id, move_x, move_y)
            self.enemy.shape.x1 = self.enemy.shape.x1 + move_x
            self.enemy.shape.y1 = self.enemy.shape.y1 + move_y
            self.after(100, self.movement)
        elif self.enemy.path_index == -1:
            print('Finished moving')

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
        move = valid__movable_area(
            self, self.player.shape.x1, self.player.shape.y1, 'up', self.player.shape)
        if move != 0:
            self.move(self.player.shape.canvas_id, 0, -1 * move)
            self.player.shape.y1 = self.player.shape.y1 - move
            self.player.shape.y2 = self.player.shape.y2 - move

    # Move Down
    def move_down(self, event):
        move = valid__movable_area(
            self, self.player.shape.x1, self.player.shape.y2, 'down', self.player.shape)
        if move != 0:
            self.move(self.player.shape.canvas_id, 0, move)
            self.player.shape.y1 = self.player.shape.y1 + move
            self.player.shape.y2 = self.player.shape.y2 + move

    # Move Left
    def move_left(self, event):
        move = valid__movable_area(
            self, self.player.shape.x1, self.player.shape.y1, 'left', self.player.shape)
        if move != 0:
            self.move(self.player.shape.canvas_id, -1 * move, 0)
            self.player.shape.x1 = self.player.shape.x1 - move
            self.player.shape.x2 = self.player.shape.x2 - move

    # Move Right
    def move_right(self, event):
        move = valid__movable_area(
            self, self.player.shape.x2, self.player.shape.y1, 'right', self.player.shape)
        if move != 0:
            self.move(self.player.shape.canvas_id, move, 0)
            self.player.shape.x1 = self.player.shape.x1 + move
            self.player.shape.x2 = self.player.shape.x2 + move
