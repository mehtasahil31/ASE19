import random
from tbl import *
from thing import *
from the import *

r = random.random
seed = random.seed


def showt(tree, pre='', rnd=THE.tree.rnd):
    most = sorted(x.n for x in tree)[-1]
    for x in tree:
        after = ""
        s = x.txt + ' = ' + str(x.lo)
        if x.n == most:
            after, most = "*", None
        if x.lo != x.hi:
            s += ' .. ' + str(x.hi)
        if isa(x.kids, Thing):
            print(pre + s, after,
                  ":", x.kids.middle(rnd),
                  '(' + str(x.kids.n) + ')')
        else:
            print(pre + s, after)
            showt(x.kids, pre + '|   ')


if __name__ == "__main__":
    t = Tbl()
    fname = "diabetes.csv"
    #fname = "auto.csv"
    t.read(file(fname))

    result = t.decisionTree()
    showt(result)
