from Num import Num


class Row():
    "Row class describing each row in data"

    def __init__(self, cells, cooked=[], dom=0):
        # self.generate_oid()
        self.cells = cells
        self.cooked = cooked
        self.dom = dom

    def dominates(self, j, goals):
        z = 0.00001
        s1, s2, n = z, z, z + len(goals)
        for goal in goals:
            if isinstance(goal, Num):
                a, b = self.cells[goal.position], j.cells[goal.position]
                a, b = goal.norm(a), goal.norm(b)
                s1 -= 10 ** (goal.weight * (a - b) / n)
                s2 -= 10 ** (goal.weight * (b - a) / n)
        return s1/n - s2/n
