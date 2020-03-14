# Edge Class to hold weights and connections
class WeightedEdge:
    def __init__(self, pixelFrom, pixelTo, weight):
        self.pixelFrom = pixelFrom
        self.pixelTo = pixelTo
        self.weight = weight

    def __str__(self):
        return "From: " + self.pixelFrom.__str__ + "\n To: " + self.pixelTo.__str__ + "\n Weight: " + str(weight)
