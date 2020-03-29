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
