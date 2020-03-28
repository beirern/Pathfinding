import tkinter as tk
import re
import numpy as np
import math
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
        self.start_game = self.bind("<Tab>", self.startGame)
        self.set_binds()

        self.player = None
        self.enemy = None

    # Get start x and y on Click
    def buttonOneClick(self, event):
        if self.object == 'WALL' or (self.object == 'PLAYER' and self.player == None) or (self.object == 'ENEMY' and self.enemy == None):
            self.currRect = None
            self.currRect_start_x = event.x
            self.currRect_start_y = event.y

        if self.object == 'ARROW':
            # Make start arrow snap to near pixel
            self.currRect = None
            start_pixel = None
            smallest_distance = -1
            self.currRect_start_x = None
            self.currRect_start_y = None

            lower_loop_y = max(event.y - 10, 0)
            upper_loop_y = min(event.y + 11, self.height)
            lower_loop_x = max(event.x - 10, 0)
            upper_loop_x = min(event.x + 11, self.width)
            for y in range(lower_loop_y, upper_loop_y):
                for x in range(lower_loop_x, upper_loop_x):
                    for waypoint in self.waypoints:
                        if waypoint.x1 == self.pixels[y][x].x and waypoint.y1 == self.pixels[y][x].y:
                            if math.sqrt(math.pow(x - event.x, 2) + math.pow(y - event.y, 2)) < smallest_distance or smallest_distance == -1:
                                start_pixel = self.pixels[y][x]
                                smallest_distance = math.sqrt(math.pow(
                                    x - event.x, 2) + math.pow(y - event.y, 2))

            # Checks if start pixel was found
            # For whatever reason start_pixel != None does not work
            if not start_pixel == None:
                self.currRect_start_x = start_pixel.x
                self.currRect_start_y = start_pixel.y

    # Draw Rectangle as curser is moving

    def buttonOneMotion(self, event):
        if self.object == 'WALL' or (self.object == 'PLAYER' and self.player == None) or (self.object == 'ENEMY' and self.enemy == None) or self.object == 'ARROW':
            if (self.currRect):
                self.delete(self.currRect)
            self.currRect_end_x = event.x
            self.currRect_end_y = event.y
            if self.object == 'WALL':
                self.currRect = self.create_rectangle(self.currRect_start_x, self.currRect_start_y,
                                                      self.currRect_end_x, self.currRect_end_y, width=1, fill="blue")
            elif self.object == 'PLAYER':
                self.currRect = self.create_rectangle(
                    self.currRect_start_x, self.currRect_start_y, self.currRect_end_x, self.currRect_end_y, width=1, fill="green")
            elif self.object == 'ENEMY':
                self.currRect = self.create_rectangle(
                    self.currRect_start_x, self.currRect_start_y, self.currRect_end_x, self.currRect_end_y, width=1, fill="red")
            elif self.object == 'ARROW':
                if self.currRect_start_x and self.currRect_start_y:
                    self.currRect = self.create_line(
                        self.currRect_start_x, self.currRect_start_y, self.currRect_end_x, self.currRect_end_y, fill="black")

    # Draw final wall and save it on Release

    def buttonOneRelease(self, event):
        if self.object == 'WALL' or (self.object == 'PLAYER' and self.player == None) or (self.object == 'ENEMY' and self.enemy == None):
            if (self.currRect):
                self.delete(self.currRect)

            self.currRect_end_x = max(event.x, 0)
            self.currRect_end_y = max(event.y, 0)
            self.currRect_end_x = min(self.currRect_end_x, self.width - 1)
            self.currRect_end_y = min(self.currRect_end_y, self.height - 1)

            if (self.valid_wall()):
                if self.object == 'WALL':
                    self.currRect = self.create_rectangle(self.currRect_start_x, self.currRect_start_y,
                                                          self.currRect_end_x, self.currRect_end_y, width=1, fill="blue")
                    self.walls.append(Shape(self.currRect_start_x, self.currRect_start_y,
                                            self.currRect_end_x, self.currRect_end_y, 'RECTANGLE', self.currRect))
                    for j in range(self.walls[-1].x1, self.walls[-1].x2 + 1):
                        for i in range(self.walls[-1].y1, self.walls[-1].y2 + 1):
                            self.pixels[i][j].is_movable_to = False

                if self.object == 'PLAYER':
                    self.currRect = self.create_rectangle(
                        self.currRect_start_x, self.currRect_start_y, self.currRect_end_x, self.currRect_end_y, width=1, fill="green")
                    self.player = Player(Shape(self.currRect_start_x, self.currRect_start_y,
                                               self.currRect_end_x, self.currRect_end_y, 'RECTANGLE', self.currRect))
                    for j in range(self.player.shape.x1, self.player.shape.x2 + 1):
                        for i in range(self.player.shape.y1, self.player.shape.y2 + 1):
                            self.pixels[i][j].is_movable_to = False

                if self.object == 'ENEMY':
                    self.currRect = self.create_rectangle(
                        self.currRect_start_x, self.currRect_start_y, self.currRect_end_x, self.currRect_end_y, width=1, fill="red")
                    self.enemy = Player(Shape(self.currRect_start_x, self.currRect_start_y,
                                              self.currRect_end_x, self.currRect_end_y, 'RECTANGLE', self.currRect))
                    for j in range(self.enemy.shape.x1, self.enemy.shape.x2 + 1):
                        for i in range(self.enemy.shape.y1, self.enemy.shape.y2 + 1):
                            self.pixels[i][j].is_movable_to = False

        if self.object == 'WAYPOINT':
            x = max(event.x, 0)
            x = min(x, self.width - 1)
            y = max(event.y, 0)
            y = min(y, self.height - 1)

            if self.valid_waypoint(Shape(x, y, x, y, 'RECTANGLE')):
                waypoint = self.create_rectangle(
                    x, y, x, y, fill="yellow")
                self.waypoints[Shape(x, y, x, y, 'RECTANGLE', waypoint)] = []

                self.pixels[y][x].is_movable_to = False

        if self.object == 'ARROW':
            if self.currRect:
                self.delete(self.currRect)
            x = max(event.x, 0)
            x = min(x, self.width - 1)
            y = max(event.y, 0)
            y = min(y, self.height - 1)

            smallest_distance = -1
            end_pixel = None

            lower_loop_y = max(y - 10, 0)
            upper_loop_y = min(y + 11, self.height)
            lower_loop_x = max(x - 10, 0)
            upper_loop_x = min(x + 11, self.width)
            for loop_y in range(lower_loop_y, upper_loop_y):
                for loop_x in range(lower_loop_x, upper_loop_x):
                    for waypoint in self.waypoints:
                        if waypoint.x1 == self.pixels[loop_y][loop_x].x and waypoint.y1 == self.pixels[loop_y][loop_x].y:
                            if math.sqrt(math.pow(loop_x - x, 2) + math.pow(loop_y - y, 2)) < smallest_distance or smallest_distance == -1:
                                end_pixel = self.pixels[loop_y][loop_x]
                                smallest_distance = math.sqrt(math.pow(
                                    loop_x - x, 2) + math.pow(loop_y - y, 2))

            # Checks if start pixel was found
            # For whatever reason start_pixel != None does not work
            if not end_pixel == None and (end_pixel.x != self.currRect_start_x or end_pixel.y != self.currRect_start_y):
                self.currRect_end_x = end_pixel.x
                self.currRect_end_y = end_pixel.y

                if self.valid_line():
                    arrow = self.create_line(self.currRect_start_x, self.currRect_start_y,
                                             self.currRect_end_x, self.currRect_end_y, fill="black")
                    self.waypoints[Shape(self.currRect_start_x, self.currRect_start_y,
                                         self.currRect_start_x, self.currRect_start_y, 'RECTANGLE', -1)].append(Shape(self.currRect_end_x, self.currRect_end_y, self.currRect_end_x, self.currRect_end_y, 'RECTANGLE', arrow))

    def valid_line(self):
        # Vertical Line/Division by 0
        if self.currRect_start_x == self.currRect_end_x:
            slope = 0
            y_intercept = 0
        else:
            slope = (self.currRect_start_y - self.currRect_end_y) / \
                (self.currRect_start_x - self.currRect_end_x)
            y_intercept = self.currRect_start_y - slope * self.currRect_start_x

        for wall in self.walls:
            if slope == 0 and y_intercept == 0:
                # Check Top of Wall
                if wall.y1 >= min(self.currRect_start_y, self.currRect_end_y) and wall.y1 <= max(self.currRect_start_y, self.currRect_end_y):
                    x = self.currRect_start_x
                    if x == wall.x1 or x == wall.x2:
                        return False
                    if x > wall.x1 and x < wall.x2:
                        return False

                # Check Bottom of Wall
                if wall.y2 >= min(self.currRect_start_y, self.currRect_end_y) and wall.y2 <= max(self.currRect_start_y, self.currRect_end_y):
                    x = self.currRect_start_x
                    if x == wall.x1 or x == wall.x2:
                        return False
                    if x > wall.x1 and x < wall.x2:
                        return False
            else:
                # Check Left Side of Wall
                if wall.x1 >= min(self.currRect_start_x, self.currRect_end_x) and wall.x1 <= max(self.currRect_start_x, self.currRect_end_x):
                    y = slope * wall.x1 + y_intercept
                    if y == wall.y1 or y == wall.y2:
                        return False
                    if y > wall.y1 and y < wall.y2:
                        return False

                # Check Right Side of Wall
                if wall.x2 >= min(self.currRect_start_x, self.currRect_end_x) and wall.x2 <= max(self.currRect_start_x, self.currRect_end_x):
                    y = slope * wall.x2 + y_intercept
                    if y == wall.y1 or y == wall.y2:
                        return False
                    if y > wall.y1 and y < wall.y2:
                        return False

                # Check Top of Wall
                if wall.y1 >= min(self.currRect_start_y, self.currRect_end_y) and wall.y1 <= max(self.currRect_start_y, self.currRect_end_y):
                    x = (wall.y1 - y_intercept) / slope
                    if x == wall.x1 or x == wall.x2:
                        return False
                    if x > wall.x1 and x < wall.x2:
                        return False

                # Check Bottom of Wall
                if wall.y2 >= min(self.currRect_start_y, self.currRect_end_y) and wall.y2 <= max(self.currRect_start_y, self.currRect_end_y):
                    x = (wall.y2 - y_intercept) / slope
                    if x == wall.x1 or x == wall.x2:
                        return False
                    if x > wall.x1 and x < wall.x2:
                        return False

        return True

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

        if self.player != None:
            playerShape = self.player.shape
            player_x1 = playerShape.x1
            player_x2 = playerShape.x2
            player_y1 = playerShape.y1
            player_y2 = playerShape.y2

            for x in x_points:
                for y in y_points:
                    if x >= player_x1 and x <= player_x2 and y >= player_y1 and y <= player_y2:
                        return False

        if self.enemy != None:
            enemyShape = self.enemy.shape
            enemy_x1 = enemyShape.x1
            enemy_x2 = enemyShape.x2
            enemy_y1 = enemyShape.y1
            enemy_y2 = enemyShape.y2

            # Check if wall is in player or enemy
            for x in x_points:
                for y in y_points:
                    if x >= enemy_x1 and x <= enemy_x2 and y >= enemy_y1 and y <= enemy_y2:
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

        if self.object == 'WALL':
            # Check if wall is in an arrow
            wall = Shape(self.currRect_start_x, self.currRect_start_y,
                         self.currRect_end_x, self.currRect_end_y, 'RECTANGLE')
            for waypoint in self.waypoints:
                for arrow in self.waypoints[waypoint]:
                    if waypoint.x1 == arrow.x2:
                        slope = 0
                        y_intercept = 0
                    else:
                        slope = (waypoint.y1 - arrow.y2) / \
                            (waypoint.x1 - arrow.x2)
                        y_intercept = waypoint.y1 - slope * waypoint.x1

                    if slope == 0 and y_intercept == 0:
                        # Check Top of Wall
                        if wall.y1 >= min(waypoint.y1, arrow.y2) and wall.y1 <= max(waypoint.y1, arrow.y2):
                            x = waypoint.x1
                            if x == wall.x1 or x == wall.x2:
                                return False
                            if x > wall.x1 and x < wall.x2:
                                return False

                        # Check Bottom of Wall
                        if wall.y2 >= min(waypoint.y1, arrow.y2) and wall.y2 <= max(waypoint.y1, arrow.y2):
                            x = waypoint.x1
                            if x == wall.x1 or x == wall.x2:
                                return False
                            if x > wall.x1 and x < wall.x2:
                                return False
                    else:
                        # Check Left Side of Wall
                        if wall.x1 >= min(waypoint.x1, arrow.x2) and wall.x1 <= max(waypoint.x1, arrow.x2):
                            y = slope * wall.x1 + y_intercept
                            if y == wall.y1 or y == wall.y2:
                                return False
                            if y > wall.y1 and y < wall.y2:
                                return False

                        # Check Right Side of Wall
                        if wall.x2 >= min(waypoint.x1, arrow.x2) and wall.x2 <= max(waypoint.x1, arrow.x2):
                            y = slope * wall.x2 + y_intercept
                            if y == wall.y1 or y == wall.y2:
                                return False
                            if y > wall.y1 and y < wall.y2:
                                return False

                        # Check Top of Wall
                        if wall.y1 >= min(waypoint.y1, arrow.y2) and wall.y1 <= max(waypoint.y1, arrow.y2):
                            x = (wall.y1 - y_intercept) / slope
                            if x == wall.x1 or x == wall.x2:
                                return False
                            if x > wall.x1 and x < wall.x2:
                                return False

                        # Check Bottom of Wall
                        if wall.y2 >= min(waypoint.y1, arrow.y2) and wall.y2 <= max(waypoint.y1, arrow.y2):
                            x = (wall.y2 - y_intercept) / slope
                            if x == wall.x1 or x == wall.x2:
                                return False
                            if x > wall.x1 and x < wall.x2:
                                return False

        if self.currRect in self.walls:
            return False

        return True

    def valid_waypoint(self, waypoint):
        if waypoint in self.waypoints:
            return False
        return self.pixels[waypoint.y1][waypoint.x1].is_movable_to

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
                waypoint = self.waypoints.popitem()[0]
                self.pixels[waypoint.y1][waypoint.x1].is_movable_to = True
                self.delete(waypoint.canvas_id)

        if self.object == 'PLAYER':
            if self.player != None:
                self.delete(self.player.shape.canvas_id)
                self.player = None

        if self.object == 'ENEMY':
            if self.enemy != None:
                self.delete(self.enemy.shape.canvas_id)
                self.enemy = None

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
                    for end_point in self.waypoints[waypoint]:
                        self.delete(end_point.canvas_id)
                    self.delete(waypoint.canvas_id)
                self.waypoints = {}

        if self.object == 'ARROW':
            if (len(self.waypoints) > 0):
                for waypoint in self.waypoints:
                    for end_point in self.waypoints[waypoint]:
                        self.delete(end_point.canvas_id)
                    self.waypoints[waypoint] = []

    # Draws enemy square and player square
    def drawPlayers(self):
        playerShape = self.player.shape

        if playerShape.shapeType == 'RECTANGLE':
            # Draw Player
            canvas_id = self.create_rectangle(
                playerShape.x1, playerShape.y1, playerShape.x2, playerShape.y2, fill="green")
            self.player = Player(
                Shape(playerShape.x1, playerShape.y1, playerShape.x2, playerShape.y2, 'RECTANGLE', canvas_id))
            # Update Pixel Array
            for j in range(playerShape.x1, playerShape.x2 + 1):
                for i in range(playerShape.y1, playerShape.y2 + 1):
                    self.pixels[i][j].is_movable_to = False

        enemyShape = self.enemy.shape
        if enemyShape.shapeType == 'RECTANGLE':
            # Draw Enemy
            canvas_id = self.create_rectangle(
                enemyShape.x1, enemyShape.y1, enemyShape.x2, enemyShape.y2, fill="red")
            self.enemy = Enemy(
                Shape(enemyShape.x1, enemyShape.y1, enemyShape.x2, enemyShape.y2, 'RECTANGLE', canvas_id))
            # Update Pixel Array
            for j in range(enemyShape.x1, enemyShape.x2 + 1):
                for i in range(enemyShape.y1, enemyShape.y2 + 1):
                    self.pixels[i][j].is_movable_to = False

    def startGame(self, event):
        if self.player != None and self.enemy != None:
            kdtree = KDTree(self.pixels, self.waypoints)

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
        self.delete(tk.ALL)
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
        self.walls = []
        self.waypoints = {}
        lines = lines[3:]
        object = 'WALL'
        for line in lines:
            line = line.strip()
            if line == 'Waypoints:':
                object = 'WAYPOINT'
            elif line == 'Arrows:':
                object = 'ARROW'
            else:
                fields = re.split('\s', line)
                if object == 'WALL':
                    self.walls.append(Shape(int(fields[0]), int(
                        fields[1]), int(fields[2]), int(fields[3]), fields[4]))
                elif object == 'WAYPOINT':
                    curr_waypoint = Shape(int(fields[0]), int(
                        fields[1]), int(fields[2]), int(fields[3]), fields[4])
                    self.waypoints[curr_waypoint] = []

                elif object == 'ARROW':
                    curr_waypoint = Shape(int(fields[0]), int(
                        fields[1]), int(fields[2]), int(fields[3]), fields[4])
                    field0 = None
                    field1 = None
                    field2 = None
                    field3 = None
                    field4 = None
                    for index in range(6, len(fields)):
                        if index % 6 == 0:
                            field0 = int(fields[index])
                        if index % 6 == 1:
                            field1 = int(fields[index])
                        if index % 6 == 2:
                            field2 = int(fields[index])
                        if index % 6 == 3:
                            field3 = int(fields[index])
                        if index % 6 == 4:
                            field4 = fields[index]
                        if index % 6 == 5:
                            self.waypoints[curr_waypoint].append(
                                Shape(field0, field1, field2, field3, field4))

        self.drawPlayers()
        self.draw_walls()
        if self.editable == True:
            self.set_editable()

    def draw_walls(self):
        for wall in self.walls:
            draw_wall = self.create_rectangle(
                wall.x1, wall.y1, wall.x2, wall.y2, width=1, fill="blue")
            wall.canvas_id = draw_wall

            for j in range(wall.x1, wall.x2 + 1):
                for i in range(wall.y1, wall.y2 + 1):
                    self.pixels[i][j].is_movable_to = False

    def draw_waypoints(self):
        for waypoint in self.waypoints:
            draw_waypoint = self.create_rectangle(
                waypoint.x1, waypoint.y1, waypoint.x2, waypoint.y2, width=1, fill="yellow")
            waypoint.canvas_id = draw_waypoint

            for end_shape in self.waypoints[waypoint]:
                arrow = self.create_line(
                    waypoint.x1, waypoint.y1, end_shape.x2, end_shape.y2, fill="black")
                end_shape.canvas_id = arrow

    def hide_waypoints(self):
        for waypoint in self.waypoints:
            self.delete(waypoint.canvas_id)
            for arrow in self.waypoints[waypoint]:
                self.delete(arrow.canvas_id)

    def set_editable(self):
        self.editable = not self.editable

        if self.editable:
            self.set_binds()
            self.draw_waypoints()
        else:
            self.set_unbinds()
            self.hide_waypoints()

    def set_binds(self):
        # Left Click for making Objects
        self.left_click = self.bind("<Button-1>", self.buttonOneClick)
        self.left_motion = self.bind("<B1-Motion>", self.buttonOneMotion)
        self.left_release = self.bind(
            "<ButtonRelease-1>", self.buttonOneRelease)

        # Right Click Deletes Objects
        self.right_click = self.bind("<Button-3>", self.clearLast)
        self.right_double_click = self.bind("<Double-Button-3>", self.clearAll)

        # Unbind Tab (opposite to mouse binds)
        self.unbind("<Tab>", self.start_game)

    def set_unbinds(self):
        if self.left_click != None:
            # Unbind Left Click
            self.unbind("<Button-1>", self.left_click)
            self.unbind("<B1-Motion>", self.left_motion)
            self.unbind("<ButtonRelease-1>", self.left_release)

            # Unbind Right Click
            self.unbind("<Button-3>", self.right_click)
            self.unbind("<Double-Button-3>", self.right_double_click)

        # Tab to Start Game (Works opposite of mouse binds)
        self.start_game = self.bind("<Tab>", self.startGame)
