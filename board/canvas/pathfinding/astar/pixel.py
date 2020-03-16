class Pixel():
    def __init__(self, x, y, index, is_movable_to):
        self.x = x
        self.y = y
        self.index = index
        self.is_movable_to = is_movable_to

    def __eq__(self, value):
        if isinstance(value, Pixel):
            return self.index == value.index
        return False

    def __ne__(self, value):
        if isinstance(value, Pixel):
            return self.index != value.index
        return False

    def __lt__(self, value):
        if isinstance(value, Pixel):
            return self.index < value.index
        return False

    def __gt__(self, value):
        if isinstance(value, Pixel):
            return self.index > value.index
        return False

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y) + ", Index: " + str(self.index) + ", Can Move To: " + str(self.is_movable_to)
