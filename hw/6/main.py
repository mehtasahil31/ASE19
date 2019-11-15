from Tbl import Tbl
from Num import Num
from Sym import Sym


def showt(tree, level=0):
    if not isinstance(tree, dict):
        for each in tree:
            showt(each, level)
    else:
        for _ in range(level):
            print("| ", end=" ")
        print("{0} = {1}...{2}".format(tree['text'], tree['low'], tree['high']), end=" ")
        if isinstance(tree['kids'], dict):
            print("{0} ({1})".format(tree['kids']['val'], tree['kids']['n']))
        else:
            for each in tree['kids']:
                print("")
                showt(each, level + 1)


if __name__ == "__main__":

    table = Tbl()
    table.read('auto.csv')
    table.createTree('auto.csv', Num)
    showt(table.treeData)

    table = Tbl()
    table.read('diabetes.csv')
    table.createTree('diabetes.csv', Sym)
    showt(table.treeData)
