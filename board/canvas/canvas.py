import tkinter as tk
import numpy as np
from .pixel import Pixel
from .enemy import Enemy
from .player import Player


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

        self.player = Player(800, 400, 25, 25)
        self.enemy = Enemy(50, 50, 25, 25)
        self.drawPlayers()

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

        if (self.validWall()):
            self.currRect = self.create_rectangle(self.start_x, self.start_y,
                                                  self.end_x, self.end_y, width=1, fill="blue")
            self.walls.append(self.currRect)

    # Helper Method to check if a wall will cover up a player
    def validWall(self):
        if (self.start_x > self.end_x):
            x_points = [n for n in range(self.end_x, self.start_x)]
        else:
            x_points = [n for n in range(self.start_x, self.end_x)]

        if (self.start_y > self.end_y):
            y_points = [n for n in range(self.end_y, self.start_y)]
        else:
            y_points = [n for n in range(self.start_y, self.end_y)]

        player_x1 = self.player.x
        player_x2 = self.player.x + self.player.width
        player_y1 = self.player.y
        player_y2 = self.player.y + self.player.height

        enemy_x1 = self.enemy.x
        enemy_x2 = self.enemy.x + self.enemy.width
        enemy_y1 = self.enemy.y
        enemy_y2 = self.enemy.y + self.enemy.height

        # Check if wall is in player or enemy
        for x in x_points:
            for y in y_points:
                if x >= player_x1 and x <= player_x2 and y >= player_y1 and y <= player_y2:
                    return False
                elif x >= enemy_x1 and x <= enemy_x2 and y >= enemy_y1 and y <= enemy_y2:
                    return False

        return True

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

            self.drawPlayers()

    # Draws enemy square and player square
    def drawPlayers(self):
        self.create_rectangle(self.player.x, self.player.y, self.player.x +
                              self.player.width, self.player.y + self.player.height, fill="red")
        self.create_rectangle(self.enemy.x, self.enemy.y, self.enemy.x +
                              self.enemy.width, self.enemy.y + self.enemy.height, fill="green")
