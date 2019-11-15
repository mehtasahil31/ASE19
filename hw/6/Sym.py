from Col import Col
from collections import defaultdict
from the import THE
import math


class Sym(Col):
    "Sym class as a subclass of Col"

    def __init__(self, column_name="", pos=0, weight=1):
        super().__init__(column_name, pos, weight)
        self.counts_map = defaultdict(int)
        self.mode = None
        self.most = 0
        self.entropy = None

    def addVal(self, value):
        "Add new value to column"
        self.all_values.append(value)
        self.counts_map[value] += 1
        self.n += 1
        if self.counts_map[value] > self.most:
            self.most = self.counts_map[value]
            self.mode = value

    def remove_from_behind(self):
        "Remove a character from front"
        char = self.all_values.pop()
        self.removeVal(char)

    def remove_from_front(self):
        "Remove a character from front"
        char = self.all_values.pop(0)
        self.removeVal(char)

    def removeVal(self, char):
        if self.n < 2:
            self.mode, self.n, self.entropy, self.most = None, 0, None, 0
        else:
            self.n -= 1
            if char == self.mode:
                # change mode
                self.counts_map[char] -= 1
                temp_count = 0
                temp_char = None
                for each in self.counts_map:
                    if self.counts_map[each] > temp_count:
                        temp_count = self.counts_map[each]
                        temp_char = each
                self.mode = temp_char
                self.most = temp_count
            else:
                self.counts_map[char] -= 1

    def findEntropy(self):
        "Calculate Entropy"
        entropy = 0
        for key, value in self.counts_map.items():
            if value != 0:
                probability = float(value / self.n)
                entropy -= probability * math.log2(probability)
        self.entropy = entropy

    def sym_like(self, x, prior, m=2):
        "Calculates how much a symbol is liked by Sym Class"
        freq = self.counts_map[x] if x in self.counts_map else 0
        return (freq + m * prior) / (self.n + m)

    def variety(self):
        if not self.entropy:
            self.findEntropy()
        return self.entropy

    def xpect(self, second_class):
        if not self.entropy:
            self.findEntropy()
        if not second_class.entropy:
            second_class.findEntropy()
        total_n = self.n + second_class.n
        return (self.entropy * self.n / total_n) + (second_class.entropy * second_class.n / total_n)

    def dist(self, x, y):
        "Calculate distance between 2 rows"
        if x == THE.char.skip and y == THE.char.skip:
            return 1
        if x != y:
            return 1
        return 0
