class Shape:
    def __init__(self, x1, y1, x2, y2, shapeType, canvas_id=-1):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.shapeType = shapeType
        self.canvas_id = canvas_id

    def __str__(self):
        return "x1: " + str(self.x1) + ", x2: " + str(self.x2) + ", y1: " + str(self.y1) + ", y2: " + str(self.y2) + ", Shape: " + str(self.shapeType) + ", id: " + str(self.canvas_id)
