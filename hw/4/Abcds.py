class Abcds():

    def __init_(learner, wait):
        self.learner = learner  #learner can be ZeroR or Nb, whatever we pass in main function
        self.abcd = Abcd()
        #TODO Add default cases for train and classify functions
        #self.train = learner.train
        #self.classify = learner.classify
        if wait == "":
            self.wait = 20
        else:
            self.wait = wait
    
    def Abcds1(s,got, want):
        #row: list of elements in a row. single item of tbl.fromString(s). See how this is implemented
        data = self.tbl.fromString(s)
	for row_num, row in enumerate(data):
		if row_num > self.wait:
		    got = self.learner.classify()
		    #TODO: implement a class function
		    want = row[-1]
		    self.abcd.Abcd1(want, got)
		self.learner.train(row, row_num)
        
