from Col import Col
from collections import defaultdict
from the import THE


class Sym(Col):
    "Sym class as a subclass of Col"

    def __init__(self, column_name="", position=0, weight=1):
        super().__init__(column_name, position, weight)
        self.counts_map = defaultdict(int)
        self.mode = None
        self.most = 0
        self.entropy = None

    def dist(self, x, y):
        "Calculate distance between 2 rows"
        if x == THE.char.skip and y == THE.char.skip:
            return 1
        if x != y:
            return 1
        return 0
