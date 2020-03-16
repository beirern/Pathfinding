# Edge Class to hold weights and connections
class WeightedEdge:
    def __init__(self, pixel_from, pixel_to, weight):
        self.pixel_from = pixel_from
        self.pixel_to = pixel_to
        self.weight = weight

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "\nFrom: " + str(self.pixel_from) + "\n To: " + str(self.pixel_to) + "\n Weight: " + str(self.weight) + "\n"
