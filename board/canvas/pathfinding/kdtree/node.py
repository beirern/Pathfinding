class Node:
    def __init__(self, pixel):
        self.pixel = pixel
        self.left = None
        self.right = None

    def __str__(self):
        return "Pixel: " + str(self.pixel) + " Right: " + str(self.left) + " Left: " + str(self.right)
