class PathfinderResult:
    def __init__(self, solution, outcome, solutionWeight):
        self.solution = solution
        self.outcome = outcome
        self.solutionWeight = solutionWeight

    def __str__(self):
        return "Solution: " + solution.__str__ + "\n Outcome:" + outcome + "\n Solution Weight: " + str(self.solutionWeight)
