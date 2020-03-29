from board.canvas.player import Player
from board.canvas.enemy import Enemy
from board.canvas.shape import Shape


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
