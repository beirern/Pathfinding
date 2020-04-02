from board.canvas.shape import Shape


class Enemy():
    def __init__(self, shape, path=None, path_index=0):
        self.shape = shape
        self.path = path
        self.path_index = path_index

    def __str__(self):
        return str(self.shape)
