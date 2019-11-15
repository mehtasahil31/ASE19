from Col import Col
import math
import collections


class Sym(Col):

    def __init__(self):
        self.mode = ""
        self.most = 0
        self.cnt = collections.defaultdict(int)
        self.e = 0
        self.n = 0
        self.col = []

    def Sym1(self, column):
        self.__init__()
        for element in column:
            self.n += 1
            self.cnt[element] += 1
            tmp = self.cnt[element]
            if tmp > self.most:
                self.most = tmp
                self.mode = element
        self.e = self.symEnt(len(column))
        return self.e

    def symEnt(self, n):
        e = 0
        for element in self.cnt:
            p = self.cnt[element] / n
            e -= p * (math.log(p) / math.log(2))
        return e

    def Sym2(self, val):
        self.n += 1
        self.cnt[val] += 1
        tmp = self.cnt[val]
        if tmp > self.most:
            self.most = tmp
            self.mode = val
        self.col.append(val)
        self.e = self.symEnt2()
        return self.e

    def symEnt2(self):
        e = 0
        for element in self.cnt:
            p = self.cnt[element] / len(self.col)
            if p:
                e -= p * (math.log(p) / math.log(2))
        return e

    def SymLike(self, x, prior, m, l, cls):
        f = self.cnt[x]
        if cls == l:
            self.Sym2(x)
        return (f + m * prior) / (self.n + m)
