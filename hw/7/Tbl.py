import jsonpickle
from Row import Row
import re
import json
from Num import Num
from Sym import Sym
from the import THE
import zipfile


class Tbl:
    "Table class for driving the tables comprising of Rows and Cols"

    def __init__(self):
        self.rows = list()
        self.cols = list()
        self.w = {'goals': [], 'nums': [], 'syms': [], 'xs': [], 'negative_weight': []}

    def dump(self):
        print("Table Object")
        print(json.dumps(json.loads(jsonpickle.encode(self)), indent=4, sort_keys=True))

    def addCol(self, column):
        for idx, col_name in enumerate(column):
            if bool(re.search(r"[<>$]", col_name)):
                self.w['nums'].append(idx)
                if bool(re.search(r"[<]", col_name)):
                    # Weight should be -1 for columns with < in their name
                    self.w['negative_weight'].append(idx)
                    self.cols.append(Num(col_name, idx, -1))
                else:
                    self.cols.append(Num(col_name, idx))
            else:
                self.w['syms'].append(idx)
                self.cols.append(Sym(col_name, idx))
            if bool(re.search(r"[<>!]", col_name)):
                self.w['goals'].append(idx)
            else:
                self.w['xs'].append(idx)

    def tbl_header(self):
        return [col.column_name for col in self.cols]

    def read(self, s, type="string"):
        content = None
        if type == "file":
            content = cells(cols(rows(file(s))))
        else:
            content = cells(cols(rows(fromString(s))))
        for idx, row in enumerate(content):
            if idx == 0:
                # Column names are here
                self.cols = []
                self.addCol(row)
            else:
                self.addRow(row)

    def addRow(self, row):
        for i in range(len(self.cols)):
            self.cols[i].add_new_value(row[i])
        self.rows.append(Row(row))


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
    for line in s.splitlines(): yield line


def file(fname):
    "read lines from a fie"
    with open(fname) as fs:
        for line in fs: yield line


def zipped(archive, fname):
    "read lines from a zipped file"
    with zipfile.ZipFile(archive) as z:
        with z.open(fname) as f:
            for line in f: yield line


def rows(src, sep=",", doomed=r'([\n\t\r ]|#.*)'):
    "convert lines into lists, killing whitespace and comments"
    linesize = None
    for n, line in enumerate(src):
        line = line.strip()
        line = re.sub(doomed, '', line)
        if line:
            line = line.split(sep)
            if linesize is None:
                linesize = len(line)

            # skip line if it doesn't match size
            if len(line) == linesize:
                yield line
            else:
                print("E> skipping line %s" % n)


def cols(src):
    "skip columns whose name contains '?'"
    valid_cols = None
    for cells in src:
        if valid_cols is None:  # Do this just for the first row
            valid_cols = [n for n, cell in enumerate(cells) if not THE.char.skip in cell]
        yield [cells[n] for n in valid_cols]


def cells(src):
    "convert strings into their right types"
    one = next(src)
    fs = [None] * len(one)  # [None, None, None, None]
    yield one  # the first line

    def ready(n, cell):
        if cell == THE.char.skip:
            return cell
        fs[n] = fs[n] or compiler(one[n])
        return fs[n](cell)

    for _, cells in enumerate(src):
        yield [ready(n, cell) for n, cell in enumerate(cells)]


def fromString(input_str):
    "read lines fro string"
    for line in input_str.splitlines():
        yield line
