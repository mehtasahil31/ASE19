import re
import zipfile


class Tbl:

    def __init__(self, fname):
        self.fname = fname
        self.rows = []
        self.cols = []
        self.oid = 1
        self.goals = []
        self.xs = []
        self.syms = []
        self.nums = []
        self.q = []
        self.w = {}
        self.idx = {}

    def compiler(self, x):
        try:
            int(x)
            return int
        except:
            try:
                float(x)
                return float
            except ValueError:
                return str

    def string(self, s):
        for line in s.splitlines():
            yield line

    def file(self, fname):
        with open(fname) as fs:
            for line in fs:
                yield line

    def zipped(self, archive, fname):
        with zipfile.ZipFile(archive) as z:
            with z.open(fname) as f:
                for line in f: yield line

    def row(self, src,
            sep=",",
            doomed=r'([\n\t\r ]|#.*)'):
        for line in src:
            line = line.strip()
            line = re.sub(doomed, '', line)
            if line:
                yield line.split(sep)
            else:
                yield line

    def cells(self, src):
        oks = None
        prev = 0
        for n, cells in enumerate(src):
            if not cells:
                continue
            if not prev:
                prev = len(cells)
            if prev != len(cells):
                print("E> Skipping line ", n + 1)
                continue
            if n == 0:
                self.column_type(cells)
                new_arr = []
                keep = 0
                for i in range(len(cells)):
                    if i not in self.q:
                        new_arr.append(cells[i])
                        self.idx.update({keep: i + 1})
                        keep += 1
                yield new_arr
            else:
                new_arr = []
                for cell in range(len(cells)):
                    if '?' in cells[cell]:
                        cells[cell] = 0
                for i in range(len(cells)):
                    if i not in self.q:
                        new_arr.append(cells[i])
                oks = [self.compiler(cell) for cell in new_arr]
                yield [f(cell) for f, cell in zip(oks, new_arr)]

    def column_type(self, cells):
        SKIPCOL = "\\?"
        NUMCOL = "[<>\\$]"
        GOALCOL = "[<>!]"

        for idx, col in enumerate(cells):
            if re.findall(SKIPCOL, col):
                self.q.append(idx)
                continue
            if re.findall(NUMCOL, col):
                self.nums.append(idx + 1)
            else:
                self.syms.append(idx + 1)
            if re.findall(GOALCOL, col):
                self.goals.append(idx + 1)
            else:
                self.xs.append(idx + 1)

        for idx, col in enumerate(cells):
            if '<' in col:
                self.w[idx + 1] = -1
            elif '>' in col:
                self.w[idx + 1] = 1

    def fromString(self, part, t):
        if not part:
            if t == 'file':
                for lst in self.cells(self.row(self.file(self.fname))):
                    self.rows.append(lst)
                    yield lst
            else:
                for lst in self.cells(self.row(self.string(self.fname))):
                    self.rows.append(lst)
                    yield lst
