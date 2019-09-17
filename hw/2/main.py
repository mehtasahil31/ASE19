from Tbl import Tbl
from Row import Row
from Num import Num


def main(part):

    if part == 1:
        s = """
        $cloudCover, $temp, $humid, $wind,  $playHours
        100, 68, 80, 0, 3
        0, 85, 85, 0, 0
        0, 80, 90, 10, 0
        60, 83, 86, 0, 4
        100, 70, 96, 0, 3
        100, 65, 70, 20, 0
        70, 64, 65, 15, 5
        0, 72, 95, 0, 0
        0, 69, 70, 0, 4
        80, 75, 80, 0, 3
        0, 75, 70, 18, 4
        60, 72, 83, 15, 5
        40, 81, 75, 0, 2
        100, 71, 91, 15, 0
        """

        tbl = Tbl(s)
        data = list(tbl.fromString(s))
        f = open("outpart1.txt", "w+")
        for i in data:
            f.write(str(i))
            f.write("\n")
        f.close()

    if part == 2:

        s = """
            $cloudCover, $temp, ?$humid, $wind,  $playHours
            100,        68,    80,    0,    3   # comments
            0,          85,    85,    0,    0
            0,          80,    90,    10,   0
            60,         83,    86,    0,    4
            100,        70,    96,    0,    3
            100,        65,    70,    20,   0
            70,         64,    65,    15,   5
            0,          72,    95,    0,    0
            0,          69,    70,    0,    4
            ?,          75,    80,    0,    3  
            0,          75,    70,    18,   4
            60,         72,    
            40,         81,    75,    0,    2    
            100,        71,    91,    15,   0	
            """

        tbl = Tbl(s)
        data = list(tbl.fromString(s))
        f = open("outpart2.txt", "w+")
        for i in data:
            f.write(str(i))
            f.write("\n")
        f.close()

    if part == 3:

        f = open("outpart3.txt", "w+")

        s = """
        $cloudCover, $temp, $humid, $wind,  $playHours
        100,         68,    80,     0,      3
        0,           85,    85,     0,      0
        0,           80,    90,     10,     0
        60,          83,    86,     0,      4
        100,         70,    96,     0,      3
        100,         65,    70,     20,     0
        70,          64,    65,     15,     5
        0,           72,    95,     0,      0
        0,           69,    70,     0,      4
        80,          75,    80,     0,      3
        0,           75,    70,     18,     4
        60,          72,    83,     15,     5
        40,          81,    75,     0,      2
        100,         71,    91,     15,     0
        """

        tbl = Tbl(s)
        count_tbl = 1
        data = list(tbl.fromString(s))
        f = open("outpart3.txt", "w+")
        for i in range(len(data)):
            row = data[i]
            if i == 0:
                for j in range(len(row)):
                    tbl.cols.append(Num(j + 1, count_tbl, row[j]))
                    count_tbl += 1
            else:
                table = []
                for j in range(len(row)):
                    if row[j] == '?':
                        row[j] = tbl.cols[j].mean
                    tbl.cols[j].Num1(row[j])
                    # tbl.cols[j].updateMeanAndSdAdd(row[j])
                    table.append(row[j])
                # tbl.rows.append(Row(count_tbl, table))
                count_tbl += 1

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
        k = 1
        f.write("t.oid: " + str(k) + "\n")
        f.write("t.rows\n")
        for i in tbl.Rows['cells'][1:]:
            f.write("| " + str(k) + "\n")
            f.write("| | cells\n")
            for j in range(len(i)):
                f.write("| | | " + str(j+1) + ":" + str(i[j]) + "\n")
            f.write("| | cooked\n")
            f.write("| | dom: 0\n")
            f.write("| | oid: " + str(k) + "\n")
            k += 1

        f.close()


for m in [1, 2, 3]:
    main(m)
