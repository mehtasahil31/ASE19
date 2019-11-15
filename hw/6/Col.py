class Col():
    "Col class for each column in data"

    def __init__(self, column_name, pos, weight, rank=0):
        self.column_name = column_name
        self.pos = pos
        self.weight = weight
        self.rank = rank
        self.n = 0
        self.all_values = []
