class Pixel():
    def __init__(self, x, y, isWall):
        self.x = x
        self.y = y
        self.isWall = isWall

    def __str__(self):
        return "x: " + x + ", y: " + y + ", Wall: " + self.isWall
