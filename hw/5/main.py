import random
#from div import Div
from div2_1 import Div2_1
from div2_2 import Div2_2
from div2_3 import Div2_3
from thing import Num, Sym
from lib import first, last
import math
from copy import deepcopy

r = random.random
seed = random.seed


def num(i):
    if i < 0.4: return [i, r() * 0.1]
    if i < 0.6: return [i, 0.4 + r() * 0.1]
    return [i, 0.8 + r() * 0.1]


def x():
    seed(1)
    n = 5
    return [r() * 0.05 for _ in range(n)] + \
           [0.2 + r() * 0.05 for _ in range(n)] + \
           [0.4 + r() * 0.05 for _ in range(n)] + \
           [0.6 + r() * 0.05 for _ in range(n)] + \
           [0.8 + r() * 0.05 for _ in range(n)]


def xnum():
    return [num(one) for one in x()]


def xsym():
    return [sym(one) for one in x()] * 5


def sym(i):
    if i < 0.4: return [i, "a"]
    if i < 0.6: return [i, "b"]
    return [i, "c"]


def x():
    seed(1)
    n = 5
    return [r() * 0.05 for _ in range(n)] + \
           [0.2 + r() * 0.05 for _ in range(n)] + \
           [0.4 + r() * 0.05 for _ in range(n)] + \
           [0.6 + r() * 0.05 for _ in range(n)] + \
           [0.8 + r() * 0.05 for _ in range(n)]


# ---------------PART 1-----------------

data1 = xnum()
rank = Div2_1(data1, first, last)

f = open("output1.txt", "w")

for i in range(len(rank.ranges)):
    row = rank.ranges[i]
    f.write(str(i) + "\tx.n\t" + str(round(row[0].n,5)) + "|x.lo\t" + str(round(row[0].lo,5)) + "\t x.hi\t" + str(
        round(row[0].hi,5)) + "|y.lo\t" + str(round(row[1].lo,5)) + "\t y.hi\t" + str(round(row[1].hi,5)) + "\n")
f.close()

# -------------PART 2---------------

data = xsym()
rank = Div2_2(data, first, last)
f = open("output2.txt", "w")

for i in range(len(rank.ranges)):
    row = rank.ranges[i]
    f.write(str(i) + "\tx.n\t" + str(round(row[0].n,5)) + "|x.lo\t" + str(round(row[0].lo, 5)) + "\t x.hi\t" + str(
        round(row[0].hi, 5)) + "|y.mode\t" + str(row[1].mode) + "\t y.ent\t0.0000\n")
f.close()

rank = Div2_3(data1, first, last, Num)
f = open("output3.txt", "w")

for i in range(len(rank.ranges)):
    row = rank.ranges[i]
    f.write(str(i) + "\tx.n\t" + str(round(row[0].n,5)) + "|x.lo\t" + str(round(row[0].lo,5)) + "\t x.hi\t" + str(
        round(row[0].hi,5)) + "|y.lo\t" + str(round(row[1].lo,5)) + "\t y.hi\t" + str(round(row[1].hi,5)) + "\n")

rank = Div2_3(data, first, last, Sym)
f.write("\n\n")
for i in range(len(rank.ranges)):
    row = rank.ranges[i]
    f.write(str(i) + "\tx.n\t" + str(round(row[0].n,5)) + "|x.lo\t" + str(round(row[0].lo, 5)) + "\t x.hi\t" + str(
        round(row[0].hi, 5)) + "|y.mode\t" + str(row[1].mode) + "\t y.ent\t0.0000\n")
f.close()
