from .node import Node


class KDTree:
    def __init__(self, pixels, waypoints):
        self.pixels = pixels
        self.waypoints = waypoints
        self.smallest_distance = -1
        self.closest = None

        self.root = Node(None)

        for waypoint in waypoints:
            self.add(waypoint)

    def add(self, waypoint, node=None, level=None):
        if node == None and level == None:
            if self.root.pixel == None:
                self.root = Node(self.pixels[waypoint.y1][waypoint.x1])
            else:
                if waypoint.x1 <= self.root.pixel.x:
                    self.root.left = self.add(waypoint, self.root.left, 1)
                else:
                    self.root.right = self.add(waypoint, self.root.right, 1)
        else:
            if node == None:
                node = Node(self.pixels[waypoint.y1][waypoint.x1])
            else:
                if level % 2 == 0:
                    if waypoint.x1 <= node.pixel.x:
                        node.left = self.add(waypoint, node.left, level + 1)
                    else:
                        node.right = self.add(waypoint, node.right, level + 1)
                else:
                    if waypoint.y1 <= node.pixel.y:
                        node.left = self.add(waypoint, node.left, level + 1)
                    else:
                        node.right = self.add(waypoint, node.right, level + 1)
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
