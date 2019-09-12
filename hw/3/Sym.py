from Col import Col
import math

class Sym(Col):

    def __init__(self):
        self.mode = ""
        self.most = 0
        self.cnt = {}
        self.count = 0

    def Sym1(self, v):
        self.count += 1
        if v not in self.cnt:
            self.cnt[v] = 0
        self.cnt[v] += 1

        temp = self.cnt[v]
        if temp > self.most:
            self.most = temp
            self.mode = v

    def SymEnt(self):
        entropy = 0.0
        for i in self.cnt:
            p = self.cnt[i] / self.count
            entropy -= p * math.log(p) / math.log(2)
        return entropy


input = ['a', 'a', 'a', 'a', 'b', 'b', 'c']

s = Sym()

for i in input:
    s.Sym1(i)

f = open("outpart1.txt", "w+")
f.write(str(s.SymEnt()))
f.close()