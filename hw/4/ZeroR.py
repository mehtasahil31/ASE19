class ZeroR():

    def __init__(self,s):
        self.tbl = Tbl(s)
    
    def train(self, row_num, row):
        self.tbl.updateTbl(row_num, row)
    
    def classify():
        return self.tbl.cols.getClassMode()
