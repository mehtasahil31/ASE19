from Tbl import Tbl
from Num import Num
from Sym import Sym

def main():

    s = """
        outlook, ?$temp,  <humid, wind, !play
        rainy, 68, 80, FALSE, yes # comments
        sunny, 85, 85,  FALSE, no
        sunny, 80, 90, TRUE, no
        overcast, 83, 86, FALSE, yes
        rainy, 70, 96, FALSE, yes
        rainy, 65, 70, TRUE, no
        overcast, 64, 65, TRUE, yes
        sunny, 72, 95, FALSE, no
        sunny, 69, 70, FALSE, yes
        rainy, 75, 80, FALSE, yes
        sunny, 75, 70, TRUE, yes
        overcast, 72, 90, TRUE, yes
        overcast, 81, 75, FALSE, yes
        rainy, 71, 91, TRUE, no
        """

    tbl = Tbl(s)
    count_tbl = 1
    num = []
    syms = []
    goals = []
    xs = []
    table = []
    weights = {}
    ignore = []
    data = list(tbl.fromString(s))
    classes = len(data[0])
    for i in range(len(data)):
        row = data[i]
        if i == 0:
            for j in range(len(row)):
                if row[j][0] != "?":
                    if row[j][0] in "<>$":
                        num.append(j)
                        tbl.cols.append(Num(j + 1, count_tbl, row[j]))
                    else:
                        syms.append(j)
                        tbl.sym.append(Sym(j + 1, count_tbl, row[j]))

                    if row[j][0] in "<>!":
                        goals.append(j+1)
                    else:
                        xs.append(j+1)

                    if row[j][0] == "<":
                        weights[j+1] = -1

                    count_tbl += 1
                else:
                    ignore.append(j)
        else:
            table = []
            for j in range(len(row)):
                if j not in set(ignore):
                    if row[j] == '?':
                        row[j] = tbl.cols[j].mean
                    if j in set(num):
                        tbl.cols[num.index(j)].Num1(row[j])
                    else:
                        tbl.sym[syms.index(j)].Sym1(row[j])
                        pass
                    table.append(row[j])
            count_tbl += 1

    f = open("outpart3.txt", "w+")
    f.write("t.cols\n")
    k = 1
    for i in tbl.cols:
        f.write("| " + str(k) + "\n")
        f.write("| | add: Num1\n")
        f.write("| | col: " + str(i.pos) + "\n")
        f.write("| | hi: " + str(i.hi) + "\n")
        f.write("| | lo: " + str(i.lo) + "\n")
        f.write("| | m2: " + str(i.m2) + "\n")
        f.write("| | mu: " + str(i.mu) + "\n")
        f.write("| | n: " + str(i.n) + "\n")
        f.write("| | oid: " + str(i.oid) + "\n")
        f.write("| | sd: " + str(i.sd) + "\n")
        f.write("| | txt: " + str(i.txt) + "\n")
        k += 1

    for i in tbl.sym:
        f.write("| " + str(k) + "\n")
        f.write("| | add: Sym1\n")
        f.write("| | cnt\n")
        for x in i.cnt:
            f.write("| | | " + str(x) + ": " + str(i.cnt[x]) + "\n")
        f.write("| | col: " + str(i.pos) + "\n")
        f.write("| | mode: " + str(i.mode) + "\n")
        f.write("| | most: " + str(i.most) + "\n")
        f.write("| | n: " + str(i.count) + "\n")
        f.write("| | oid: " + str(i.oid) + "\n")
        f.write("| | txt: " + str(i.txt) + "\n")
        k += 1

    f.write("t.my\n")
    f.write("| class: " + str(classes) + "\n")
    f.write("| goals\n")
    for x in goals:
        f.write("| | " + str(x) + "\n")
    f.write("| nums\n")
    for i in num:
        f.write("| | " + str(i + 1) + "\n")
    f.write("| syms\n")
    for i in syms:
        f.write("| | " + str(i + 1) + "\n")
    f.write("| w \n")
    for x in weights:
        f.write("| | " + str(x) + ": " + str(weights[x]) + "\n")
    f.write("| xnums\n")
    f.write("| xs\n")
    for x in xs:
        f.write("| | " + str(x) + "\n")
    f.write("| xsyms\n")
    for x in xs:
        f.write("| | " + str(x) + "\n")


main()
