import heapq
import threading
from .pathfinderResult import PathfinderResult


# Class that uses aStarGraph to find the shortest path
class PathfinderSolver:
    def __init__(self, graph):
        self.graph = graph
        self.queue = []
        self.dist_to = {}
        self.previous = {}
        self.minutes = 0
        self.timeout = False

    # Finds the shortest path from a start pixel to an end pixel
    def findShortestPath(self, start, end):
        solution = []

        # Timeout will be called after 10 minutes
        # Each minute
        self.timeout_timer = threading.Timer(2.0, self.time_up)

        self.timeout_timer.start()
        print("Starting Search...")

        if start == end:
            return PathfinderResult([start, end], "SOLVED", 0)

        for edge in self.graph.neighbors(start):
            self.dist_to[edge.pixel_to] = edge.weight
            self.previous[edge.pixel_to] = start
            self.queue.append(
                (self.dist_to[edge.pixel_to] + self.graph.estimated_distance_to_goal(edge.pixel_to, end), edge.pixel_to))

        heapq.heapify(self.queue)
        while len(self.queue) != 0:
            if self.timeout:
                self.timeout_timer.cancel()
                return PathfinderResult([], "TIMEOUT", 0)
            pixel = heapq.heappop(self.queue)[1]
            if pixel == end:
                solution_weight = self.dist_to[pixel]
                temp = pixel
                while temp != start:
                    solution.insert(0, temp)
                    temp = self.previous[temp]
                solution.insert(0, start)
                self.timeout_timer.cancel()
                return PathfinderResult(solution, "SOLVED", solution_weight)
            for edge in self.graph.neighbors(pixel):
                if edge.pixel_to in self.dist_to:
                    if edge.weight + self.dist_to[edge.pixel_from] < self.dist_to[edge.pixel_to]:
                        self.dist_to[edge.pixel_to] = edge.weight + \
                            self.dist_to[edge.pixel_from]
                        self.previous[edge.pixel_to] = pixel
                        # Remove the old priority
                        for tuple in self.queue:
                            if tuple.count(edge.pixel_to) == 1:
                                self.queue.remove(tuple)
                        # Add new priority
                        self.queue.append(
                            (self.dist_to[edge.pixel_to] + self.graph.estimated_distance_to_goal(edge.pixel_to, end), edge.pixel_to))
                else:
                    self.dist_to[edge.pixel_to] = edge.weight + \
                        self.dist_to[edge.pixel_from]
                    self.previous[edge.pixel_to] = pixel
                    self.queue.append(
                        (self.dist_to[edge.pixel_to] + self.graph.estimated_distance_to_goal(edge.pixel_to, end), edge.pixel_to))
            heapq.heapify(self.queue)

        self.timeout_timer.cancel()
        return PathfinderResult([], "UNSOLVED", 0)

    # Timeout after 10 minutes
    def time_up(self):
        self.timeout_timer.cancel()
        self.timeout = True
