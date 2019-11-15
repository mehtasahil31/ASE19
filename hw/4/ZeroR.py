from Sym import Sym
from Abcd import Abcd

class ZeroR():

    def __init__(self):
        self.goals = []
        self.symo = Sym()
        self.abcdo = Abcd()

    def train(self, t, rows):
        for idx, row in enumerate(rows):
            if idx == 0:
                continue
            if idx > 2:
                expected = row[len(row) - 1]
                self.symo.Sym1(self.goals)
                result = self.classify()
                self.abcdo.Abcd1(expected, result)
            self.goals.append(t[-1][idx - 1])

    def classify(self):
        return self.symo.mode

    def dump(self):
        self.abcdo.AbcdReport()
