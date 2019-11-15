from hw3 import *
from hw6 import *


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



if __name__ == "__main__":

# file_name = "../4/diabetes.csv"
	file1 = "auto.csv"
	#print(type(file_contents))
	table = Tbl()
	table.read(file1)
	table.createTree(file1, Num)
	showt(table.treeData)
	file2 = "diabetes.csv"
	table = Tbl()
	table.read(file2)
	table.createTree(file2, Sym)
	showt(table.treeData)
# for each in table.tree_result:
#     pretty_print(each)
