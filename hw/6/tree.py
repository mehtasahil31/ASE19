def tree(self, lst, y, yis, lvl=0):
    if len(lst) >= THE.tree.minObs * 2:
        # find the best column
        lo, cut, col = 10 ** 32, None, None
        for col1 in self.cols.indep:
            x = lambda row: row.cells[col1.pos]
            cut1, lo1 = col1.div(lst, x=x, y=y, yis=yis)
            if cut1:
                if lo1 < lo:
                    cut, lo, col = cut1, lo1, col1
        # if a cut exists
        if cut:
            # split data on best col, call i.tree on each split
            x = lambda row: row.cells[col.pos]
            return [o(lo=lo,
                      hi=hi,
                      n=len(kids),
                      txt=col.txt,
                      kids=self.tree(kids, y, yis, lvl + 1)
                      ) for lo, hi, kids in col.split(lst, x, cut)]
    return yis(lst, key=y)


def decisionTree(self):
    return self.tree(self.rows,
                     y=lambda z: z.cells[self.cols.klass.pos],
                     yis=Sym)


def regressionTree(self):
    return self.tree(self.rows,
                     y=lambda z: last(z.cells),
                     yis=Num)


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
