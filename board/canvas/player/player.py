from board.canvas.shape import Shape


class Player():
    def __init__(self, shape):
        self.shape = shape

    def __str__(self):
        return self.shape.__str__()
