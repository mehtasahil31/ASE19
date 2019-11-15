import re, json, jsonpickle, zipfile
from Num import Num
from Sym import Sym
from Row import Row
from the import THE
from div2 import Div2
from div2 import Div2, column_name_fn


class Tbl:
    "Table class for driving the tables comprising of Rows and Cols"

    def __init__(self):
        self.rows = list()  # Will hold Row objects for each row
        self.cols = list()  # Will hold Num objects for each column
        self.col_info = {'goals': [], 'nums': [], 'syms': [], 'xs': [], 'negative_weight': []}

    def dump(self):
        # replaced manual printing with JSON output
        print("Table Object")
        # Single line output to JSON
        print(json.dumps(json.loads(jsonpickle.encode(self)), indent=4, sort_keys=True))

    def addCol(self, column):
        for idx, col_name in enumerate(column):
            if bool(re.search(r"[<>$]", col_name)):
                self.col_info['nums'].append(idx)
                if bool(re.search(r"[<]", col_name)):
                    self.col_info['negative_weight'].append(idx)
                    self.cols.append(Num(col_name, idx, -1))
                else:
                    self.cols.append(Num(col_name, idx))
            else:
                self.col_info['syms'].append(idx)
                self.cols.append(Sym(col_name, idx))
            if bool(re.search(r"[<>!]", col_name)):
                self.col_info['goals'].append(idx)
            else:
                self.col_info['xs'].append(idx)

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

    def tree(i):
        class_index = i.col_info["goals"][0]
        class_type = Sym if class_index in i.col_info["syms"] else Num
        func1 = lambda row: row.cells
        data = list(map(func1, i.rows))
        i.treeR = i.get_tree(data, class_index, class_type, 0)

    def get_tree(i, data_rows, class_index, class_type, level):
        if len(data_rows) >= THE.tree.minObs:
            low, cut, column = 10 ** 32, None, None
            column_types = []
            for col in i.cols:
                if isinstance(col, Num):
                    column_types.append(Num)
                else:
                    column_types.append(Sym)
            for col in i.cols:
                if col.position == class_index:
                    continue
                x = Div2(data_rows, col.position, class_index, column_types, column_name_fn)
                cut1, low1 = x.cut, x.best
                if cut1 and low1:
                    if low1 < low:
                        cut, low, column = cut1, low1, col
            if cut:
                return [treeR(low, high, len(kids), column.column_name,
                              i.get_tree(kids, class_index, class_type, level + 1)) for low, high, kids in
                        i.split(data_rows, cut, column)]
        return leaf_result(data_rows[len(data_rows) // 2][class_index], len(data_rows))

    def split(i, data_rows, cut, column):
        left_half, low = data_rows[:cut], data_rows[cut][column.position]
        right_half, high = data_rows[cut:], data_rows[cut + 1][column.position]
        return [(-float('inf'), low, left_half), (high, float('inf'), right_half)]


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


def rows(src, sep=THE.char.sep, doomed=THE.char.doomed):
    "convert lines into lists, killing whitespace and comments"
    linesize = None
    for n, line in enumerate(src):
        line = line.strip()
        line = re.sub(doomed, '', line)
        if line:
            line = line.split(sep)
            # update the linesize for first time
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
            return cell  # skip over '?'
        fs[n] = fs[n] or compiler(one[n])  # ensure column 'n' compiles
        return fs[n](cell)  # compile column 'n'

    for _, cells in enumerate(src):
        yield [ready(n, cell) for n, cell in enumerate(cells)]


def fromString(input_str):
    "read lines fro string"
    for line in input_str.splitlines():
        yield line


def treeR(low, high, n, text, kids):
    return {"low": low, "high": high, "n": n, "text": text, "kids": kids}


def leaf_result(classval, rows):
    if classval == 'p':
        classval = 'tested_positive'
    if classval == 'n':
        classval = 'tested_negative'
    return {'val': classval, 'n': rows}


def hw6Print(tree, level=0):
    if isinstance(tree, list):
        for each in tree:
            hw6Print(each, level)
    else:
        for _ in range(level):
            print("|", end=" ")
        print("{0}={1}.....{2}".format(tree['text'], tree['low'], tree['high']), end=" ")
        if not isinstance(tree['kids'], list):
            print("{0} ({1})".format(tree['kids']['val'], tree['kids']['n']))
        else:
            for each in tree['kids']:
                print()
                hw6Print(each, level + 1)
