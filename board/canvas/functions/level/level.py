import tkinter as tk
import re
from board.canvas.enemy import Enemy
from board.canvas.player import Player
from board.canvas.shape import Shape
from board.canvas.pathfinding.astar.pixel import Pixel
from board.canvas.functions.level.draw import drawPlayers, draw_walls


def load(self, lines):
    self.delete(tk.ALL)
    # Make Player
    player_line = lines[0].strip()
    fields = re.split('\s', player_line)

    self.player = Player(Shape(
        int(fields[0]), int(fields[1]), int(fields[2]), int(fields[3]), fields[4]))

    # Make Enemy
    enemy_line = lines[1].strip()
    if enemy_line != 'None':
        fields = re.split('\s', enemy_line)

        self.enemy = Enemy(Shape(int(fields[0]), int(
            fields[1]), int(fields[2]), int(fields[3]), fields[4]))

    # Set up array of Pixels
    self.pixels = []
    for i in range(self.height):
        self.pixels.append([])
        for j in range(self.width):
            self.pixels[-1].append(Pixel(j,
                                         i, i * len(self.pixels[0]) + j, True))

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

    drawPlayers(self)
    draw_walls(self)
    if self.editable == True:
        self.set_editable()
