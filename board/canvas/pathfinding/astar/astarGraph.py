import math
from .weightedEdge import WeightedEdge
from .pixel import Pixel


# Graph for Astarpathfinder
class AstarGraph:
    # Takes in [][] of all pixels (The grid)
    # A reference to enemy to get height and width to determine valid neighbors
    def __init__(self, pixels, waypoints):
        self.pixels = pixels
        self.waypoints = waypoints
        self.edges = {}

        self.fillEdges()

    # Fills the edges List with all edges for grid
    # Each pixel has a List representing the edges in each direction
    # i.e. [UP, RIGHT, DOWN, LEFT]
    # (0, 2) -> [WE(0, 1), WE(1,2), WE(0, 3), None]
    def fillEdges(self):
        for waypoint in self.waypoints:
            self.edges[self.pixels[waypoint.y1][waypoint.x1]] = []
            for end_point in self.waypoints[waypoint]:
                self.edges[self.pixels[waypoint.y1][waypoint.x1]].append(WeightedEdge(self.pixels[waypoint.y1][waypoint.x1], self.pixels[end_point.y1][end_point.x1],
                                                                                      math.sqrt(math.pow(waypoint.y1 - end_point.y1, 2) + math.pow(waypoint.y2 - end_point.y2, 2))))

    # Returns valid neighbors
    # Returns the middle pixel in either direction of a valid direction
    # i.e. if enemy height = 5, would return the 3rd pixel left or right

    def neighbors(self, pixel):
        return self.edges[pixel]

    # Returns the manhatten distance squared, heuristic function
    def estimated_distance_to_goal(self, pixel, goal):
        return ((pixel.x - goal.x) ** 2 + (pixel.y - goal.y) ** 2)

    def __str__(self):
        return str(self.pixels)
