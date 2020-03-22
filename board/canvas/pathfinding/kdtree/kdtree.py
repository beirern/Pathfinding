from .node import Node


class KDTree:
    def __init__(self, pixels):
        self.pixels = pixels
        self.smallest_distance = -1
        self.closest = None

        self.root = Node(None)

    def nearest(self, target, node=None, level=None):
        if node == None and level == None:
            self.closest = None
            self.smallest_distance = -1
            self.nearest(target, self.root, 0)

            return self.closest
        else:
            if node != None:
                if self.distance_to_point(node, target) <= self.smallest_distance or self.smallest_distance == -1:
                    self.closest = node.pixel
                    self.smallest_distance = self.distance_to_point(
                        node, target)

            if level % 2 == 0:
                if target.x <= node.pixel.x:
                    self.nearest(target, node.left, level + 1)
                    if (node.pixel.x - target.x) ** 2 <= self.smallest_distance:
                        self.nearest(target, node.right, level + 1)
                else:
                    self.nearest(target, node.right, level + 1)
                    if (node.pixel.x - target.x) ** 2 <= self.smallest_distance:
                        self.nearest(target, node.left, level + 1)
            else:
                if target.y <= node.pixel.y:
                    self.nearest(target, node.left, level + 1)
                    if (node.pixel.y - target.y) ** 2 <= self.smallest_distance:
                        self.nearest(target, node.right, level + 1)
                else:
                    self.nearest(target, node.right, level + 1)
                    if (node.pixel.y - target.y) ** 2 <= self.smallest_distance:
                        self.nearest(target, node.left, level + 1)

    def distance_to_point(self, pixel, target):
        return (pixel.x - target.x) ** 2 + (pixel.y - target.y) ** 2
