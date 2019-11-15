from sys import path
from math import log
import random, re, os
from hw3 import Row, Col, Num, Sym, cells, cols, rows, file, fromString
from lib import *
from the import *
from div2 import Div2
from hw6 import Tbl, showt
from collections import defaultdict
from hw7 import RandomProjections
r= random.randint
seed=random.seed

class rowSorter:
    def __init__(self, file_name):
        seed(1)
        self.data = cells(cols(rows(file(file_name))))
        self.tbl = Tbl()
        self.fillTable()
        self.random_rows = [self.tbl.rows[random.randint(0,len(self.tbl.rows)-1)] for i in range(100)]
        self.goals = [self.tbl.cols[i] for i in self.tbl.metadata['goals']]
        
    def fillTable(self):
        for i, row in enumerate(self.data):
            if i == 0:
                self.tbl.addCol(row)
            else:
                self.tbl.addRow(row)

    def printValues(self):
        records = self.sortRows()
        cols = [i.column_name for i in self.tbl.cols]
        print("\t" , end = "\t")
        for i in cols:
            print(i, end= "\t")
        print("")
        numValues = 4
        for r in records[-numValues:]:
            print("best", end = "\t")
            for c in r[1].cells:
                print(c, end = "\t")
            print("")
        print("")
        for r in records[:numValues]:
            print("worst", end = "\t")
            for c in r[1].cells:
                print(c, end = "\t")
            print("")
        
    def sortRows(self):
        records = []
        for i in self.random_rows:
            count = 0
            for j in self.random_rows:
                count += int(i.dominates(j,self.goals)<0)
            records.append((count, i))
        records.sort(key = lambda x: x[0])
        return records

#Check if any of the two centroid_list dominates the other
# TODO: goal.position instead of i?
def dominates(c1, c2, goals):
    z = 0.00001
    s1, s2, n = z,z,z+len(goals)
    for i, goal in enumerate(goals):
        if isinstance(goal, Num):
            a,b = c1.leaves[i].mu, c2.leaves[i].mu
            a,b = goal.norm(a), goal.norm(b)
            s1 -= 10**(goal.weight * (a-b)/n)
            s2 -= 10**(goal.weight * (b-a)/n)
    return (s1/n - s2/n)

def distance(col1, col2, goals):
    d, n, p = 0, 0, 2
    for i, col in enumerate(goals):
        n += 1
        d0 = None
        if isinstance(col, Num):
            d0 = col.dist(col1.leaves[i].mu, col2.leaves[i].mu)
        else:
            d0 = col.dist(col1.leaves[i].mode, col2.leaves[i].mode)
        d += d0**p
    return d**(1/p) / n**(1/p)         


def findEnvyCentroids(envies, centroid_list, goals):
	
    for c1 in centroid_list:
        for c2 in centroid_list:
            if dominates(c1, c2, goals) > 0:
                envies[c1].append(c2)
    return envies

def findClosestNodes(envies, goals):
	
    closest = []
    for c1 in envies.keys():
        distMin, envyMax = float('inf'), None
        for c2 in envies[c1]:
            dist = distance(c1,c2,goals)
            if dist < distMin:
                distMin = dist
                envyMax = c2 
        closest.append((c1, envyMax))
    return closest[:]
	
def envy():
    RP = RandomProjections('auto.csv')
    centroid_list = RP.leaf_nodes
    goals = [RP.tbl.cols[i] for i in RP.tbl.metadata['goals']]
    
    envies = defaultdict(list)
    envies = findEnvyCentroids(envies, centroid_list, goals)
    closest = findClosestNodes(envies, goals)
 
    for i, c in enumerate(closest):
        newTbl = Tbl()
        cols = [col.column_name for col in c[0].tbl.cols]
        cols.append('!$new_class')
        newTbl.addCol(cols)
        for row in c[0].tbl.rows:
            cells = row.cells
            cells.append(0)
            newTbl.addRow(cells)
        
        for row in c[1].tbl.rows:
            cells = row.cells
            cells.append(1)
            newTbl.addRow(cells)
       
        try:
            newTbl.createTree()
            print ("CLUSTERS V/S ENVY CLUSTER")
            showt(newTbl.treeData)
            print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except:
            pass


if __name__ == "__main__":
    #r = rowSorter('auto.csv') 
    #r.printValues()
    envy()
