class Pixel():
    def __init__(self, x, y, index, is_movable_to):
        self.x = x
        self.y = y
        self.index = index
        self.is_movable_to = is_movable_to

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y) + ", Index: " + str(self.index) + ", Can Move To: " + str(self.is_movable_to)
