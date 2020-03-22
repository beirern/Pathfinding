from .node import Node


class KDTree:
    def __init__(self, pixels):
        self.pixels = pixels
        self.smallest_distance = -1
        self.closest = None

        self.root = Node(None)

        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                self.add(pixels[i][j])

    def add(self, pixel, node=None, level=None):
        if node == None and level == None:
            if self.root.pixel == None:
                self.root = Node(pixel)
            else:
                if pixel.x <= self.root.pixel.x:
                    self.root.left = self.add(pixel, self.root.left, 1)
                else:
                    self.root.right = self.add(pixel, self.root.right, 1)
        else:
            if node == None:
                node = Node(pixel)
            else:
                if level % 2 == 0:
                    if pixel.x <= node.pixel.x:
                        node.left = self.add(pixel, node.left, level + 1)
                    else:
                        node.right = self.add(pixel, node.right, level + 1)
                else:
                    if pixel.y <= node.pixel.y:
                        node.left = self.add(pixel, node.left, level + 1)
                    else:
                        node.right = self.add(pixel, node.right, level + 1)
            return node

    def nearest(self, target, node=None, level=None):
        if node == None and level == None:
            self.closest = None
            self.smallest_distance = -1
            self.nearest(target, self.root, 0)

            return self.closest
        else:
            if node != None:
                if self.distance_to_point(node.pixel, target) <= self.smallest_distance or self.smallest_distance == -1:
                    self.closest = node.pixel
                    self.smallest_distance = self.distance_to_point(
                        node.pixel, target)

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
