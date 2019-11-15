import random
from collections import defaultdict
from the import *
from div2 import *
from hw7 import hw7
from Tbl import Tbl, cells, cols, rows, file, hw6Print
from Num import Num

r = random.randint
seed = random.seed


class Hw8:
    def __init__(self, file_name):
        seed(1)
        self.file_c = cells(cols(rows(file(file_name))))
        self.t = Tbl()
        self.content()
        self.random_rows = self.random_rows()
        self.goals = self.get_goals()

    def printVal(self):
        v = self.row_sort()
        c = [x.column_name for x in self.t.cols]
        print("\t", end="\t")
        for x in c:
            print(x, end="\t")
        print()

        for x in v[-4:]:
            print("best", end="\t")
            for val in x[1].cells:
                print(val, end="\t")
            print()
        print()

        for x in v[:4]:
            print("worst", end="\t")
            for val in x[1].cells:
                print(val, end="\t")
            print()
        print()

    def row_sort(self):
        val = []
        for irw in self.random_rows:
            cnt = 0
            for jrw in self.random_rows:
                if irw.dominates(jrw, self.goals) < 0:
                    cnt += 1
            val.append((cnt, irw))
        val.sort(key=lambda x: x[0])
        return val

    def content(self):
        header = False
        for r in self.file_c:
            if not header:
                self.t.addCol(r)
                header = True
            else:
                self.t.addRow(r)

    def random_rows(self):
        return [self.t.rows[r(0, len(self.t.rows) - 1)] for _ in range(100)]

    def get_goals(self):
        return [self.t.cols[each] for each in self.t.col_info['goals']]

    def call_me(self):
        self.printVal()


def dist(col1, col2, goals):
    d, n, p = 0, 0, 2
    for i, c in enumerate(goals):
        n += 1
        d0 = None
        if isinstance(c, Num):
            d0 = c.dist(col1.leaves[i].mu, col2.leaves[i].mu)
        else:
            d0 = c.dist(col1.leaves[i].mode, col2.leaves[i].mode)
        d += d0 ** p
    return d ** (1 / p) / n ** (1 / p)


def dominate(c1, c2, goals):
    z = 0.00001
    s1, s2, n = z, z, z + len(goals)
    for i, g in enumerate(goals):
        if isinstance(g, Num):
            a, b = c1.leaves[i].mu, c2.leaves[i].mu
            a, b = g.norm(a), g.norm(b)
            s1 -= 10 ** (g.weight * (a - b) / n)
            s2 -= 10 ** (g.weight * (b - a) / n)
    return s1/n - s2/n


def envy():
    a = hw7('auto.csv')
    c = a.leaf_nodes
    ENMap, envyNodes = defaultdict(list), list()
    g = [a.tbl.cols[each] for each in a.tbl.col_info['goals']]
    for c1 in c:
        for c2 in c:
            if dominate(c1, c2, g) > 0:
                ENMap[c1].append(c2)
    for c1 in ENMap:
        mdist = float('inf')
        mEnvy = None
        for c2 in ENMap[c1]:
            d = dist(c1, c2, g)
            if d < mdist:
                mdist = d
                mEnvy = c2
        envyNodes.append((c1, mEnvy))
    for val in envyNodes:
        tbl = Tbl()
        cols = [col.column_name for col in val[0].tbl.cols]
        cols.append('!$nwcls')
        tbl.addCol(cols)
        for e in val[0].tbl.rows:
            c = e.cells
            c.append(0)
            tbl.addRow(c)
        for e in val[1].tbl.rows:
            c = e.cells
            c.append(1)
            tbl.addRow(c)
        try:
            tbl.tree()
            print ("CLUSTERS V/S ENVY CLUSTER")
            hw6Print(tbl.treeR)
            print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except:
            continue


# hw = Hw8('auto.csv')
# hw.call_me()
envy()
