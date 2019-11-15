from sys import path
from math import log
import random,re 
from hw3 import Row, Col, Num, Sym, cells, cols, rows, file, fromString
from the import *
from div2 import Div2
r= random.random
seed=random.seed

def leaf(klass, rows):
	return {
		'val' : 'p' if klass == 'tested_positive' else 'n',
			'n' : rows
	}

class Tbl:
	def __init__(self):
		self.rows = [] 
		self.cols = [] 
		self.metadata = {'goals': [], 'nums': [], 'syms': [], 'xs' : [], 'weight' : []}
		self.treeData = None
		self.types = []
	
	def addCol(self, column):

		for idx,col_name in enumerate(column):
			if bool(re.search(r"[<>$]",col_name)):
				self.metadata['nums'].append(idx)
				self.types.append(Num)
				if bool(re.search(r"[<]", col_name)):
					self.metadata['weight'].append(idx)
					self.cols.append(Num(col_name,idx,-1))
				else:
					self.cols.append(Num(col_name,idx))
			else:
				self.metadata['syms'].append(idx)
				self.types.append(Sym)
				self.cols.append(Sym(col_name,idx))
			if bool(re.search(r"[<>!]",col_name)):
				self.metadata['goals'].append(idx)
			else:
				self.metadata['xs'].append(idx)
	def addRow(self,row): 
	
		for i in range(len(self.cols)):
			self.cols[i].addVal(row[i])
		self.rows.append(Row(row))
	
	def read(self, f):
		
		data = cells(cols(rows(file(f))))
		for i, row in enumerate(data):
			if i == 0:
				self.addCol(row)
			else:
				self.addRow(row)

	def getGoalIdx(self):
		return self.metadata["goals"][0]
	
	def getClassChar(self,label):
		if label == "tested_positive":
			return 'p'
		else:
			return 'n'

	def createTree(self):
		y = self.getGoalIdx()
		yis = Sym if y in self.metadata["syms"] else Num
		mapper = lambda row: row.cells
		lst = list(map(mapper, self.rows))
		if yis == Sym:
			for row in lst:
				row[y] = self.getClassChar(row[y])
		self.treeData = self.tree(lst, y,yis, 0)

	def tree(self, lst, y, yis, level):
		if len(lst) >= THE.tree.minObs*2:
			low, cut, column = 10**32, None, None
			for col in self.cols:
				if col.pos != y:
					x = Div2(lst, col.pos, y, self.types)
					cut1, low1 = x.cut, x.best
					if cut1 and low1:
						if low1 < low:
   							cut, low, column = cut1, low1, col
			if cut:
				return [{"low":low, "high":high, "n":len(kids), "text":column.column_name, "kids":self.tree(kids, y, yis, level + 1)} for low,high, kids in self.split(lst, cut, column)]                        
		return leaf(lst[len(lst)//2][y], len(lst))


	def split(self, data_rows, cut, column):
		left_half,low = data_rows[:cut],data_rows[cut][column.pos]
		right_half,high = data_rows[cut:], data_rows[cut+1][column.pos]
		return [(-float('inf'), low, left_half),(high, float('inf'), right_half)]

def showt(tree, level = 0):
	if not isinstance(tree, dict):
		for each in tree:
			showt(each, level)
	else:
		for _ in range(level):
			print ("| ", end = " ")
		print ("{0} = {1}...{2}".format(tree['text'], tree['low'], tree['high']), end = " ")        
		if isinstance(tree['kids'], dict):
			print ("{0} ({1})".format(tree['kids']['val'],tree['kids']['n']))
		else:
			for each in tree['kids']:
				print ("")
				showt(each, level + 1)
		

