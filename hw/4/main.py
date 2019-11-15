from NB import NB
from Tbl import Tbl
from Col import Col
from ZeroR import ZeroR

# ZeroR

print("#--- zerorok --------------------")
t = Tbl("weathernon.csv")
rows = []
for lst in t.fromString(False, "file"):
    rows.append(lst)

c = Col()
t = c.colNum(t.rows)

zr = ZeroR()
zr.train(t, rows)
print("\nweathernon")
zr.dump()

t = Tbl("diabetes.csv")
rows = []
for lst in t.fromString(False, "file"):
    rows.append(lst)

c = Col()
t = c.colNum(t.rows)

zr = ZeroR()
zr.train(t, rows)
print("\ndiabetes")
zr.dump()

# NB

print("\n\n#--- Nbok ---------------------")
tbl = Tbl("weathernon.csv")
rows = []
for lst in tbl.fromString(False, "file"):
    rows.append(lst)
c = Col()
tbl.cols = c.colNum(tbl.rows)
nb = NB(tbl, 3)
nb.train(tbl, rows)
print("\nweathernon")
nb.dump()

print()
tbl = Tbl("diabetes.csv")
rows = []
for lst in tbl.fromString(False, "file"):
    rows.append(lst)
c = Col()

tbl.cols = c.colNum(tbl.rows)
nb = NB(tbl, 19)
nb.train(tbl, rows)
print("\ndiabetes")
nb.dump()