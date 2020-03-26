import tkinter as tk
import re
import numpy as np
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
        self.object = 'WALL'

        self.currRect = None

        self.width = width
        self.height = height

        self.walls = []
        self.waypoints = []

        # Set up array of Pixels
        self.pixels = []
        for i in range(self.height):
            self.pixels.append([])
            for j in range(self.width):
                self.pixels[-1].append(Pixel(j,
                                             i, i * len(self.pixels[0]) + j, True))

        # Left Click for making Walls
        self.bind("<Button-1>", self.buttonOneClick)
        self.bind("<B1-Motion>", self.buttonOneMotion)
        self.bind("<ButtonRelease-1>", self.buttonOneRelease)

        # Right Click Deletes Walls
        self.bind("<Button-3>", self.clearLast)
        self.bind("<Double-Button-3>", self.clearAll)

        self.player = Player(Shape(800, 400, 824, 424, 'RECTANGLE'))
        self.enemy = Enemy(Shape(50, 50, 74, 74, 'RECTANGLE'))
        # self.drawPlayers()

        # Enter to Start Game
        self.bind("<Tab>", self.startGame)

    # Get start x and y on Click
    def buttonOneClick(self, event):
        if self.object == 'WALL':
            self.currRect = None
            self.currRect_start_x = event.x
            self.currRect_start_y = event.y

    # Draw Rectangle as curser is moving

    def buttonOneMotion(self, event):
        if self.object == 'WALL':
            if (self.currRect):
                self.delete(self.currRect)
            self.currRect_end_x = event.x
            self.currRect_end_y = event.y
            self.currRect = self.create_rectangle(self.currRect_start_x, self.currRect_start_y,
                                                  self.currRect_end_x, self.currRect_end_y, width=1, fill="blue")

    # Draw final wall and save it on Release

    def buttonOneRelease(self, event):
        if self.object == 'WALL':
            if (self.currRect):
                self.delete(self.currRect)

            self.currRect_end_x = max(event.x, 0)
            self.currRect_end_y = max(event.y, 0)
            self.currRect_end_x = min(self.currRect_end_x, self.width - 1)
            self.currRect_end_y = min(self.currRect_end_y, self.height - 1)

            if (self.valid_wall()):
                self.currRect = self.create_rectangle(self.currRect_start_x, self.currRect_start_y,
                                                      self.currRect_end_x, self.currRect_end_y, width=1, fill="blue")
                self.walls.append(Shape(self.currRect_start_x, self.currRect_start_y,
                                        self.currRect_end_x, self.currRect_end_y, 'RECTANGLE', self.currRect))

                for j in range(self.walls[-1].x1, self.walls[-1].x2 + 1):
                    for i in range(self.walls[-1].y1, self.walls[-1].y2 + 1):
                        self.pixels[i][j].is_movable_to = False

        if self.object == 'WAYPOINT':
            x = max(event.x, 0)
            x = min(x, self.width - 1)
            y = max(event.y, 0)
            y = min(y, self.height - 1)

            if self.valid_waypoint(Shape(x, y, x, y, 'RECTANGLE')):
                waypoint = self.create_rectangle(
                    x, y, x, y, fill="yellow")
                self.waypoints.append(
                    Shape(x, y, x, y, 'RECTANGLE', waypoint))

                self.pixels[y][x].is_movable_to = False

    # Helper Method to check if a wall will cover up a player
    def valid_wall(self):
        # Get X Points
        if (self.currRect_start_x == self.currRect_end_x):
            x_points = [self.currRect_start_x]
        elif (self.currRect_start_x > self.currRect_end_x):
            x_points = [n for n in range(
                self.currRect_end_x, self.currRect_start_x)]
        else:
            x_points = [n for n in range(
                self.currRect_start_x, self.currRect_end_x)]

        if (self.currRect_start_y == self.currRect_end_y):
            y_points = [self.currRect_start_y]
        elif (self.currRect_start_y > self.currRect_end_y):
            y_points = [n for n in range(
                self.currRect_end_y, self.currRect_start_y)]
        else:
            y_points = [n for n in range(
                self.currRect_start_y, self.currRect_end_y)]

        playerShape = self.player.shape
        player_x1 = playerShape.x1
        player_x2 = playerShape.x2
        player_y1 = playerShape.y1
        player_y2 = playerShape.y2

        enemyShape = self.enemy.shape
        enemy_x1 = enemyShape.x1
        enemy_x2 = enemyShape.x2
        enemy_y1 = enemyShape.y1
        enemy_y2 = enemyShape.y2

        # Check if wall is in player or enemy
        for x in x_points:
            for y in y_points:
                if x >= player_x1 and x <= player_x2 and y >= player_y1 and y <= player_y2:
                    return False
                elif x >= enemy_x1 and x <= enemy_x2 and y >= enemy_y1 and y <= enemy_y2:
                    return False

        # Check if wall is in a different wall
        for x in x_points:
            for y in y_points:
                for wall in self.walls:
                    if x >= wall.x1 and x <= wall.x2 and y >= wall.y1 and y <= wall.y2:
                        return False

        # Check if wall is in a waypoint
        for x in x_points:
            for y in y_points:
                for waypoint in self.waypoints:
                    if x >= waypoint.x1 and x <= waypoint.x2 and y >= waypoint.y1 and y <= waypoint.y2:
                        return False
        return True

    def valid_waypoint(self, waypoint):
        playerShape = self.player.shape
        enemyShape = self.enemy.shape

        # Check if waypoint is in player or enemy
        if waypoint.x1 >= playerShape.x1 and waypoint.x1 <= playerShape.x2 and waypoint.y1 >= playerShape.y1 and waypoint.y1 <= playerShape.y2:
            return False
        elif waypoint.x1 >= enemyShape.x1 and waypoint.x1 <= enemyShape.x2 and waypoint.y1 >= enemyShape.y1 and waypoint.y1 <= enemyShape.y2:
            return False

        # Check if waypoint in a wall
        for wall in self.walls:
            if waypoint.x1 >= wall.x1 and waypoint.x2 <= wall.x2 and waypoint.y1 >= wall.y1 and waypoint.y2 <= wall.y2:
                return False

        # Check if waypoint is in a waypoint
        for list_waypoint in self.waypoints:
            if waypoint.x1 == list_waypoint.x1 and waypoint.y1 == list_waypoint.y1:
                return False

        return True

    # Remove last Drawn Wall
    def clearLast(self, event):
        if self.object == 'WALL':
            if (len(self.walls) > 0):
                wall = self.walls[-1]
                for j in range(wall.x1, wall.x2 + 1):
                    for i in range(wall.y1, wall.y2 + 1):
                        self.pixels[i][j].is_movable_to = True
                self.delete(self.walls[-1].canvas_id)
                del self.walls[-1]

        if self.object == 'WAYPOINT':
            if (len(self.waypoints) > 0):
                waypoint = self.waypoints[-1]
                self.pixels[waypoint.y1][waypoint.x1].is_movable_to = True
                self.delete(self.waypoints[-1].canvas_id)
                del self.waypoints[-1]

    # Removes all Walls
    def clearAll(self, event):
        if self.object == 'WALL':
            if (len(self.walls) > 0):
                for wall in self.walls:
                    for j in range(wall.x1, wall.x2 + 1):
                        for i in range(wall.y1, wall.y2 + 1):
                            self.pixels[i][j].is_movable_to = True
                    self.delete(wall.canvas_id)
                self.walls = []

        if self.object == 'WAYPOINT':
            if (len(self.waypoints) > 0):
                for waypoint in self.waypoints:
                    self.pixels[waypoint.y1][waypoint.x1].is_movable_to = True
                    self.delete(waypoint.canvas_id)
                self.waypoints = []

    # Draws enemy square and player square
    def drawPlayers(self):
        playerShape = self.player.shape

        if playerShape.shapeType == 'RECTANGLE':
            # Draw Player
            canvas_id = self.create_rectangle(
                playerShape.x1, playerShape.y1, playerShape.x2, playerShape.y2, fill="green")
            self.player = Player(
                Shape(playerShape.x1, playerShape.y1, playerShape.x2, playerShape.y2, 'RECTANGLE', canvas_id))

        enemyShape = self.enemy.shape
        if enemyShape.shapeType == 'RECTANGLE':
            # Draw Enemy
            canvas_id = self.create_rectangle(
                enemyShape.x1, enemyShape.y1, enemyShape.x2, enemyShape.y2, fill="red")
            self.enemy = Enemy(
                Shape(enemyShape.x1, enemyShape.y1, enemyShape.x2, enemyShape.y2, 'RECTANGLE', canvas_id))
            # Update Pixel Array
            for j in range(self.enemy.shape.x1, self.enemy.shape.x2 + 1):
                for i in range(self.enemy.shape.y1, self.enemy.shape.y2 + 1):
                    self.pixels[i][j].is_movable_to = False

    def startGame(self, event):
        kdtree = KDTree(self.pixels)

    def astar(self):
        graph = AstarGraph(self.pixels, self.enemy)
        pathfinder = PathfinderSolver(graph)
        result = pathfinder.findShortestPath(
            self.pixels[62][62], self.pixels[412][812])

        if result.outcome == "SOLVED":
            print("DONE")
            self.print_path(result.solution)
        elif result.outcome == "UNSOLVABLE":
            print("Unsolvable!")
        else:
            print("Timed Out!")

    def print_path(self, solution):
        for i in range(len(solution) - 1):
            self.create_line(solution[i].x, solution[i].y,
                             solution[i+1].x, solution[i+1].y)

    def load_level(self, lines):
        # Make Player
        player_line = lines[0].strip()
        fields = re.split('\s', player_line)

        self.player = Player(Shape(
            int(fields[0]), int(fields[1]), int(fields[2]), int(fields[3]), fields[4]))

        # Make Enemy
        enemy_line = lines[1].strip()
        fields = re.split('\s', enemy_line)

        self.enemy = Enemy(Shape(int(fields[0]), int(
            fields[1]), int(fields[2]), int(fields[3]), fields[4]))

        # Fill Walls and Waypoints Array
        lines = lines[3:]
        walls = True
        for line in lines:
            line = line.strip()
            if line == 'Waypoints:':
                walls = False
            else:
                fields = re.split('\s', line)
                if walls:
                    self.walls.append(Shape(int(fields[0]), int(
                        fields[1]), int(fields[2]), int(fields[3]), fields[4]))
                else:
                    self.waypoints.append(Shape(int(fields[0]), int(
                        fields[1]), int(fields[2]), int(fields[3]), fields[4]))

        self.drawPlayers()
        self.draw_walls()

    def draw_walls(self):
        for wall in self.walls:
            draw_wall = self.create_rectangle(
                wall.x1, wall.y1, wall.x2, wall.y2, width=1, fill="blue")
            wall.canvas_id = draw_wall

            for j in range(wall.x1, wall.x2 + 1):
                for i in range(wall.y1, wall.y2 + 1):
                    self.pixels[i][j].is_movable_to = False
