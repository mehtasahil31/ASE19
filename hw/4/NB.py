import math
import collections
from Abcd import Abcd
from Sym import Sym
from Num import Num

class NB:
    def __init__(self, tbl, wait):
        self.tbl = tbl
        self.wait = wait
        self.n = -1
        self.k = 1
        self.m = 2
        self.lst = []
        self.count = 0
        self.abo = Abcd()
        self.tbllist = collections.defaultdict(list)
        self.cols = collections.defaultdict(list)

    def train(self, t, lines):
        for idx, row in enumerate(lines):
            self.n+=1
            if idx == 0:
                continue
            if row[-1] not in self.cols:
                for rowIdx, _ in enumerate(row[:-1]):
                    if self.tbl.idx[rowIdx] in self.tbl.syms:
                        self.cols[row[-1]].append(Sym())
                    elif self.tbl.idx[rowIdx] in self.tbl.nums:
                        self.cols[row[-1]].append(Num())
            if idx <= self.wait:
                for c in range(len(row) - 1):
                    if self.tbl.idx[c] in self.tbl.syms:
                        self.cols[row[-1]][c].Sym2(row[c])
                    elif self.tbl.idx[c] in self.tbl.nums:
                        self.cols[row[-1]][c].num2(row[c])
            if idx > self.wait:
                expected = row[-1]
                result = self.classify(row, "")
                self.abo.Abcd1(expected, result)
            self.tbllist[row[-1]].append(row)
            self.count += 1
            self.lst.append(row)

    def classify(self, line, guess):
        most = float('-inf')
        for cls, row in self.tbllist.items():
            guess = cls if not guess else guess
            like = self.bayes_theorem(line, row, cls)
            if like > most:
                most = like
                guess = cls
        return guess

    def bayes_theorem(self, line, tbl, cls):
        like = prior = ((len(tbl) + self.k) / (self.n + self.k * len(self.tbllist)))
        like = math.log(like)
        for c in range(len(line) - 1):
            if self.tbl.idx[c] in self.tbl.nums:
                like += math.log(self.cols[cls][c].NumLike(line[c], line[-1], cls))
            elif self.tbl.idx[c] in self.tbl.syms:
                like += math.log(self.cols[cls][c].SymLike(line[c], prior, self.m, line[-1], cls))
        return like

    def dump(self):
        self.abo.AbcdReport()
