# Edge Class to hold weights and connections
class WeightedEdge:
    def __init__(self, pixelFrom, pixelTo, weight):
        self.pixelFrom = pixelFrom
        self.pixelTo = pixelTo
        self.weight = weight

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "From: " + str(self.pixelFrom) + "\n To: " + str(self.pixelTo) + "\n Weight: " + str(self.weight) + "\n"
