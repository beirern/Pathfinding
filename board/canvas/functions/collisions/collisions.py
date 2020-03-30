from board.canvas.shape import Shape


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


def valid__movable_area(self, x1, y1, direction, object, move=10):
    for i in range(1, move + 1):
        valid = True
        if direction == 'right':
            for j in range(0, object.height + 1):
                if x1 + i >= self.width:
                    return i - 2
                else:
                    if (self.pixels[y1 + j][x1 + i].is_movable_to == False):
                        return i - 2

        if direction == 'left':
            for j in range(0, object.height + 1):
                if x1 - i < 0:
                    return i - 2
                else:
                    if (self.pixels[y1 + j][x1 - i].is_movable_to == False):
                        return i - 2

        if direction == 'down':
            for j in range(0, object.width + 1):
                if y1 + i >= self.height:
                    return i - 2
                else:
                    if (self.pixels[y1 + i][x1 + j].is_movable_to == False):
                        return i - 2

        if direction == 'up':
            for j in range(0, object.width + 1):
                if y1 - i < 0:
                    return i - 2
                else:
                    if (self.pixels[y1 - i][x1 + j].is_movable_to == False):
                        return i - 2

    return move
