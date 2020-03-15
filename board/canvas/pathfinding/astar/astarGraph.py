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

    def fillEdges(self):
        for i in range(len(self.pixels)):
            for j in range(len(self.pixels[0])):
                self.edges.append([])
                if i != 0:
                    if self.pixels[i-1][j].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i-1][j], 0))
                if i != len(self.pixels) - 1:
                    if self.pixels[i+1][j].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i+1][j], 0))
                if j != 0:
                    if self.pixels[i][j-1].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i][j-1], 0))
                if j != len(self.pixels[0]) - 1:
                    if self.pixels[i][j+1].is_movable_to:
                        self.edges[-1].append(WeightedEdge(self.pixels[i]
                                                           [j], self.pixels[i][j+1], 0))

    # Returns valid neighbors
    # Returns the middle pixel in either direction of a valid direction
    # i.e. if enemy height = 5, would return the 3rd pixel left or right

    def neighbors(self, pixel):
        valid_neighbors = []
        half_height = int(self.neighbor_height / 2)
        half_width = int(self.neighbor_width / 2)

        bottom = self.pixels[pixel.y - half_height][pixel.x]
        if bottom.y != 0:
            valid_spot = True
            for j in range(bottom.x - half_width + 1, bottom.x + half_width):
                if len(self.edges[self.pixels[bottom.y][j].index]) != 1:
                    valid_spot = False
            if valid_spot:
                if not (self.pixels[bottom.y - 1][bottom.x - half_width].is_movable_to and self.pixels[bottom.y - 1][bottom.x + half_width].is_movable_to):
                    valid_spot = False

            if valid_spot:
                valid_edge = self.edges[bottom.index]
                valid_neighbors.append(valid_edge)

        top = self.pixels[pixel.y + half_height][pixel.x]
        if top.y != len(self.pixels):
            valid_spot = True
            for j in range(top.x - half_width + 1, top.x + half_width):
                if len(self.edges[self.pixels[top.y][j].index]) != 1:
                    valid_spot = False
            if valid_spot:
                if not (self.pixels[top.y + 1][top.x - half_width].is_movable_to and self.pixels[top.y + 1][top.x + half_width].is_movable_to):
                    valid_spot = False

            if valid_spot:
                valid_edge = self.edges[top.index]
                valid_neighbors.append(valid_edge)

        left = self.pixels[pixel.y][pixel.x - half_width]
        if left.x != 0:
            valid_spot = True
            for i in range(left.y - half_height + 1, left.y + half_height):
                if len(self.edges[self.pixels[i][left.x].index]) != 1:
                    valid_spot = False
            if valid_spot:
                if not (self.pixels[left.y - half_height][left.x - 1].is_movable_to and self.pixels[left.y + half_height][left.x - 1].is_movable_to):
                    valid_spot = False

            if valid_spot:
                valid_edge = self.edges[left.index]
                valid_neighbors.append(valid_edge)

        right = self.pixels[pixel.y][pixel.x + half_width]
        if right.x != len(self.pixels[0]):
            valid_spot = True
            for i in range(right.y - half_height + 1, right.y + half_height):
                if len(self.edges[self.pixels[i][right.x].index]) != 1:
                    valid_spot = False
            if valid_spot:
                if not (self.pixels[right.y - half_height][right.x + 1].is_movable_to and self.pixels[right.y + half_height][right.x + 1].is_movable_to):
                    valid_spot = False

            if valid_spot:
                valid_edge = self.edges[right.index]
                valid_neighbors.append(valid_edge)

        return valid_neighbors

    # Returns the manhatten distance squared, heuristic function
    def estimatedDistancetoGoal(self, pixel, goal):
        return ((pixel.x - goal.x) ** 2 + (pixel.y - goal.y) ** 2)

    def __str__(self):
        return str(self.pixels)
