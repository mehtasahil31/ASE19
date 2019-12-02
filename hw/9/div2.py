from thing import same, first, last, ordered
from the import THE
import random
from Sym import Sym

r = random.random
seed = random.seed


class Div2:
    "Part 1 of splitting elements in List"

    def __init__(self, lst, x, y, ctypes, key_fn=same):
        self.ctypes = ctypes
        self.key_fn = key_fn
        self.lst = ordered(lst, key="", index=x)
        self.b4 = [class_type("", idx) for idx, class_type in enumerate(self.ctypes)]
        for row in self.lst:
            for idx, val in enumerate(row):
                self.b4[idx].add_new_value(val)
        self.x = x
        self.y = y
        self.step = int(len(self.lst)) ** THE.div.min
        self.gain = 0
        self.start = first(self.b4[self.y].all_values)
        self.stop = last(self.b4[self.y].all_values)
        self.ranges = []
        self.epsilon = self.b4[self.y].variety()
        self.epsilon *= THE.div.cohen
        low = 1
        high = self.b4[self.y].n
        self.rank, self.cut, self.best = self.divide(1, low, high, self.b4)
        self.gain /= self.b4[self.y].n

    def divide(self, rank, low, high, b4):
        "Find a split between low and high, then recurse on each split."
        left = dict()
        right = dict()
        best = b4[self.y].variety()
        cut = None
        left[self.x] = self.ctypes[self.x]()
        left[self.y] = self.ctypes[self.y]()
        right[self.x] = self.ctypes[self.x]()
        right[self.y] = self.ctypes[self.y]()
        for i in range(low, high):
            right[self.x].add_new_value(self.b4[self.x].all_values[i])
            right[self.y].add_new_value(self.b4[self.y].all_values[i])

        for j in range(low, high):
            left[self.x].add_new_value(self.b4[self.x].all_values[j])
            left[self.y].add_new_value(self.b4[self.y].all_values[j])
            right[self.x].delete_value(self.b4[self.x].all_values[j])
            right[self.y].delete_value(self.b4[self.y].all_values[j])

            if left[self.y].n >= self.step:
                if right[self.y].n >= self.step:
                    now = self.key_fn(self.b4[self.y].all_values[j - 1])
                    after = self.key_fn(self.b4[self.y].all_values[j])
                    if now == after:
                        continue
                    xpect = None
                    if isinstance(self.b4[self.y], Sym):
                        if abs(ord(right[self.y].mode) - ord(left[self.y].mode)) >= self.epsilon:
                            if ord(after) - ord(self.start) >= self.epsilon:
                                if ord(self.stop) - ord(now) >= self.epsilon:
                                    xpect = left[self.y].xpect(right[self.y])
                    else:
                        if abs(right[self.y].mu - left[self.y].mu) >= self.epsilon:
                            if after - self.start >= self.epsilon:
                                if self.stop - now >= self.epsilon:
                                    xpect = left[self.y].xpect(right[self.y])
                    if xpect:
                        if xpect * THE.div.trivial < best:
                            best, cut = xpect, j

        if cut:
            low_b4 = [class_type("", idx) for idx, class_type in enumerate(self.ctypes)]
            high_b4 = [class_type("", idx) for idx, class_type in enumerate(self.ctypes)]
            for each in range(len(low_b4)):
                for x in range(low, cut):
                    low_b4[each].add_new_value(self.b4[each].all_values[x])

            for each in range(len(high_b4)):
                for x in range(cut, high):
                    high_b4[each].add_new_value(self.b4[each].all_values[x])
            rank, c, b = self.divide(rank, low, cut, low_b4)
            rank += 1
            rank, _, _ = self.divide(rank, cut, high, high_b4)
        else:
            self.gain += b4[self.y].n * b4[self.y].variety()
            b4[self.x].rank = rank
            b4[self.y].rank = rank
            self.ranges.append(b4)
        return rank, cut, best
