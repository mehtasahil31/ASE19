import re
import zipfile


class Tbl():

    def __init__(self, s):
        self.Rows = {'cells': self.create_rows(s), 'cooked': []}
        self.cols = []
        self.sym = []
        self.oid = None
        self.num = []
        self.syms = []
        self.goals = []
        self.xs = []
        self.weights = {}
        self.ignore = []

    def compiler(self, x):
        "return something that can compile strings of type x"
        try:
            int(x); return int
        except ValueError:
            try:
                float(x); return float
            except ValueError:
                return str

    def string(self, s):
        "read lines from a string"
        for line in s.splitlines():
            yield line

    def file(self, fname):
        "read lines from a fie"
        with open(fname) as fs:
            for line in fs:
                yield line

    def zipped(self, archive, fname):
        # read lines from a zipped file
        with zipfile.ZipFile(archive) as z:
            with z.open(fname) as f:
                for line in f:
                    yield line

    def rows(self, src, sep=",", doomed=r'([\n\t\r ]|#.*)'):
        # convert lines into lists, killing whitespace and comments
        for line in src:
            line = line.strip()
            line = re.sub(doomed, '', line)
            if line:
                yield [l for l in line.split(sep) if l]

    def cells(self, src):
        "convert strings into their right types"
        dropcol = []
        length = 0
        for n, cells in enumerate(src):
            if n == 0:
                length = len(cells)
                yield cells
            else:
                oks = [self.compiler(cell) for cell in cells]
                for c in dropcol:
                    if c < len(oks):
                        del oks[c]

                if len(oks) < length:
                    yield "E>Skipping Line " + str(n)
                else:
                    yield [f(cell) for f, cell in zip(oks, cells)]

    def fromString(self, s):
        "putting it all together"
        for lst in self.cells(self.rows(self.string(s))):
            yield lst

    def create_rows(self, s):
        lists = []
        for lst in self.fromString(s):
            lists.append(lst)
        return lists
    
    def updateTbl(self, row_num, row):
        #tbl = Tbl(s)
        #count_tbl = 1
        #data = list(tbl.fromString(s))
        #Function gets row directly as input
        classes = len(row)
        #for i in range(len(data)):
        #row = data[i]
        if row_num == 0:
            for j in range(len(row)):
                if row[j][0] != "?":
                    if row[j][0] in "<>$":
                        self.num.append(j)
                        self..cols.append(Num(j + 1, count_tbl, row[j]))
                    else:
                        self.syms.append(j)
                        self.sym.append(Sym(j + 1, count_tbl, row[j]))

                    if row[j][0] in "<>!":
                        self.goals.append(j+1)
                    else:
                        self.xs.append(j+1)

                    if row[j][0] == "<":
                        self.weights[j+1] = -1

                    count_tbl += 1
                else:
                    self.ignore.append(j)
        else:
            for j in range(len(row)):
                if j not in set(self.ignore):
                    if row[j] == '?':
                        row[j] = self.cols[j].mean
                    if j in set(num):
                        self..cols[self.num.index(j)].Num1(row[j])
                    else:
                        self.sym[self.syms.index(j)].Sym1(row[j])
                    #table.append(row[j])
            count_tbl += 1
