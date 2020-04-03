import math
from board.canvas.shape import Shape
from board.canvas.player import Player
from board.canvas.enemy import Enemy
from board.canvas.functions.collisions import valid_line, valid_wall, valid_waypoint
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

        if (valid_wall(self)):
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

        if valid_waypoint(self, Shape(x, y, x, y, 'RECTANGLE')):
            waypoint = self.create_rectangle(
                x, y, x, y, fill="yellow")
            self.waypoints[Shape(x, y, x, y, 'RECTANGLE', waypoint)] = []

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

            if valid_line(self):
                arrow = self.create_line(self.currRect_start_x, self.currRect_start_y,
                                         self.currRect_end_x, self.currRect_end_y, fill="black")
                self.waypoints[Shape(self.currRect_start_x, self.currRect_start_y,
                                     self.currRect_start_x, self.currRect_start_y, 'RECTANGLE', -1)].append(Shape(self.currRect_end_x, self.currRect_end_y, self.currRect_end_x, self.currRect_end_y, 'RECTANGLE', arrow))
