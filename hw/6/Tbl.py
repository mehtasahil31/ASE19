from lib import *
from Row import Row
from the import THE
import re
from Num import Num
from Sym import Sym
from div2 import Div2
import zipfile


class Tbl:
    def __init__(self):
        self.rows = []
        self.cols = []
        self.metadata = {'goals': [], 'nums': [], 'syms': [], 'xs': [], 'weight': []}
        self.treeData = None
        self.types = []

    def read(self, f):

        data = cells(cols(rows(file(f))))
        for i, row in enumerate(data):
            if i == 0:
                for idx, col_name in enumerate(row):
                    if bool(re.search(r"[<>$]", col_name)):
                        self.metadata['nums'].append(idx)
                        self.types.append(Num)
                        if bool(re.search(r"[<]", col_name)):
                            self.metadata['weight'].append(idx)
                            self.cols.append(Num(col_name, idx, -1))
                        else:
                            self.cols.append(Num(col_name, idx))
                    else:
                        self.metadata['syms'].append(idx)
                        self.types.append(Sym)
                        self.cols.append(Sym(col_name, idx))
                    if bool(re.search(r"[<>!]", col_name)):
                        self.metadata['goals'].append(idx)
                    else:
                        self.metadata['xs'].append(idx)
            else:
                for i in range(len(self.cols)):
                    self.cols[i].addVal(row[i])
                self.rows.append(Row(row))

    def getGoalIdx(self):
        return self.metadata["goals"][0]

    def getClassChar(self, label):
        if label == "tested_positive":
            return 'p'
        else:
            return 'n'

    def createTree(self, f, yis):
        y = self.getGoalIdx()
        lst = list(cells(rows(file(f))))[1:]
        if yis == Sym:
            for row in lst:
                row[y] = self.getClassChar(row[y])
        self.treeData = self.tree(lst, y, yis, 0)

    def tree(self, lst, y, yis, level):
        if len(lst) >= THE.tree.minObs * 2:
            low, cut, column = 10 ** 32, None, None
            for col in self.cols:
                if col.pos != y:
                    x = Div2(lst, col.pos, y, self.types)
                    cut1, low1 = x.cut, x.best
                    if cut1 and low1:
                        if low1 < low:
                            cut, low, column = cut1, low1, col
            if cut:
                return [{"low": low, "high": high, "n": len(kids), "text": column.column_name,
                         "kids": self.tree(kids, y, yis, level + 1)} for low, high, kids in
                        self.split(lst, cut, column)]
        return leaf(lst[len(lst) // 2][y], len(lst))

    def split(self, data_rows, cut, column):
        left_half, low = data_rows[:cut], data_rows[cut][column.pos]
        right_half, high = data_rows[cut:], data_rows[cut + 1][column.pos]
        return [(-float('inf'), low, left_half), (high, float('inf'), right_half)]


# -----------------------------------------
# iterators

def cells(src):
    "convert strings into their right types"
    one = next(src)
    fs = [None] * len(one)  # [None, None, None, None]
    yield one  # the first line

    def ready(n, cell):
        if cell == THE.char.skip:
            return cell  # skip over '?'
        fs[n] = fs[n] or prep(one[n])  # ensure column 'n' compiles
        return fs[n](cell)  # compile column 'n'

    for _, cells in enumerate(src):
        yield [ready(n, cell) for n, cell in enumerate(cells)]


def prep(x):
    "return a function that can compile things of type 'x'"

    def num(z):
        f = float(z)
        i = int(f)
        return i if i == f else f

    for c in [THE.char.num, THE.char.less, THE.char.more]:
        if c in x:
            return num
    return str


def compiler(x):
    "return something that can compile strings of type x"
    """return something that can compile strings"""

    def num(z):
        f = float(z)
        i = int(f)
        return i if i == f else f

    for c in [THE.char.num, THE.char.less, THE.char.more]:
        if c in x:
            return num
    return str


def string(s):
    "read lines from a string"
    for line in s.splitlines():
        yield line


def file(fname):
    "read lines from a fie"
    with open(fname) as fs:
        for line in fs: yield line


def zipped(archive, fname):
    "read lines from a zipped file"
    with zipfile.ZipFile(archive) as z:
        with z.open(fname) as f:
            for line in f: yield line


def rows(src, sep=THE.char.sep, doomed=THE.char.doomed):
    "convert lines into lists, killing whitespace and comments"
    linesize = None
    for n, line in enumerate(src):
        line = line.strip()
        line = re.sub(doomed, '', line)
        if line:
            line = line.split(sep)
            if linesize is None:
                linesize = len(line)

            if len(line) == linesize:
                yield line
            else:
                print("E> skipping line %s" % n)


def cols(src):
    "skip columns whose name contains '?'"
    usedCol = None
    for cells in src:
        if usedCol is None:
            usedCol = [n for n, cell in enumerate(cells)
                       if not THE.char.skip in cell]
        yield [cells[n] for n in usedCol]


def fromString(input_str):
    "read lines fro string"
    for line in input_str.splitlines():
        yield line


def leaf(klass, rows):
    
    if klass == 'p':
        klass = 'tested_positive'
    elif klass == 'n':
        klass = 'tested_negative' 
    return {'val': klass, 'n': rows}
