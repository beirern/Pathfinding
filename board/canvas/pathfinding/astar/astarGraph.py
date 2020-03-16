from .weightedEdge import WeightedEdge
from .pixel import Pixel


# Graph for Astarpathfinder
class AstarGraph:
    # Takes in [][] of all pixels (The grid)
    # A reference to enemy to get height and width to determine valid neighbors
    def __init__(self, pixels, enemy):
        self.pixels = pixels
        self.neighbor_height = enemy.shape.height
        self.neighbor_width = enemy.shape.width
        self.edges = []

        self.fillEdges()

    # Fills the edges List with all edges for grid
    # Each pixel has a List representing the edges in each direction
    # i.e. [UP, RIGHT, DOWN, LEFT]
    # (0, 2) -> [WE(0, 1), WE(1,2), WE(0, 3), None]
    def fillEdges(self):
        for i in range(len(self.pixels)):
            for j in range(len(self.pixels[0])):
                self.edges.append([])
                # UP
                if i != 0:
                    if self.pixels[i-1][j].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i-1][j], 1))
                    else:
                        self.edges[-1].append(None)
                else:
                    self.edges[-1].append(None)
                # RIGHT
                if j != len(self.pixels[0]) - 1:
                    if self.pixels[i][j+1].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i][j+1], 1))
                    else:
                        self.edges[-1].append(None)
                else:
                    self.edges[-1].append(None)
                # DOWN
                if i != len(self.pixels) - 1:
                    if self.pixels[i+1][j].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i+1][j], 1))
                    else:
                        self.edges[-1].append(None)
                else:
                    self.edges[-1].append(None)
                # LEFT
                if j != 0:
                    if self.pixels[i][j-1].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i][j-1], 1))
                    else:
                        self.edges[-1].append(None)
                else:
                    self.edges[-1].append(None)

    # Returns valid neighbors
    # Returns the middle pixel in either direction of a valid direction
    # i.e. if enemy height = 5, would return the 3rd pixel left or right

    def neighbors(self, pixel):
        valid_neighbors = []
        half_height = int(self.neighbor_height / 2)
        half_width = int(self.neighbor_width / 2)

        # TOP is index 0 for list of edges
        top = self.pixels[pixel.y - half_height][pixel.x]
        if top.y != 0:
            valid_spot = True
            for j in range(top.x - half_width, top.x + half_width + 1):
                if self.edges[self.pixels[top.y][j].index][0] == None:
                    valid_spot = False

            if valid_spot:
                valid_edge = WeightedEdge(pixel, Pixel(
                    pixel.x, pixel.y - 1, pixel.y * len(self.pixels[0]) + pixel.x, True), 1)
                valid_neighbors.append(valid_edge)

        # RIGHT is index 1 for list of edges
        right = self.pixels[pixel.y][pixel.x + half_width]
        if right.x != len(self.pixels[0]):
            valid_spot = True
            for i in range(right.y - half_height, right.y + half_height + 1):
                if self.edges[self.pixels[i][right.x].index][1] == None:
                    valid_spot = False

            if valid_spot:
                valid_edge = WeightedEdge(pixel, Pixel(
                    pixel.x + 1, pixel.y, pixel.y * len(self.pixels[0]) + pixel.x, True), 1)
                valid_neighbors.append(valid_edge)

        # BOTTOM is index 2 for list of edges
        bottom = self.pixels[pixel.y + half_height][pixel.x]
        if bottom.y != len(self.pixels):
            valid_spot = True
            for j in range(bottom.x - half_width, bottom.x + half_width + 1):
                if self.edges[self.pixels[bottom.y][j].index][2] == None:
                    valid_spot = False

            if valid_spot:
                valid_edge = WeightedEdge(pixel, Pixel(
                    pixel.x, pixel.y + 1, pixel.y * len(self.pixels[0]) + pixel.x, True), 1)
                valid_neighbors.append(valid_edge)

        # LEFT is index 3 for list of edges
        left = self.pixels[pixel.y][pixel.x - half_width]
        if left.x != 0:
            valid_spot = True
            for i in range(left.y - half_height, left.y + half_height + 1):
                if self.edges[self.pixels[i][left.x].index][3] == None:
                    valid_spot = False

            if valid_spot:
                valid_edge = WeightedEdge(pixel, Pixel(
                    pixel.x - 1, pixel.y, pixel.y * len(self.pixels[0]) + pixel.x, True), 1)
                valid_neighbors.append(valid_edge)

        return valid_neighbors

    # Returns the manhatten distance squared, heuristic function
    def estimated_distance_to_goal(self, pixel, goal):
        return ((pixel.x - goal.x) ** 2 + (pixel.y - goal.y) ** 2)

    def __str__(self):
        return str(self.pixels)
