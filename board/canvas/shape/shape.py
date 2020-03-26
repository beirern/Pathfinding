class Shape:
    def __init__(self, x1, y1, x2, y2, shapeType, canvas_id=-1):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)
        self.height = self.y2 - self.y1 + 1
        self.width = self.x2 - self.x1 + 1
        self.shapeType = shapeType
        self.canvas_id = canvas_id

    def __str__(self):
        return str(self.x1) + ' ' + str(self.y1) + ' ' + str(self.x2) + ' ' + str(self.y2) + ' ' + str(self.shapeType) + ' ' + str(self.canvas_id)

    def __repr__(self):
        return str(self)
