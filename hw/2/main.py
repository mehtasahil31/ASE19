from Tbl import Tbl
from Row import Row
from Num import Num

def main(part):

    if part == 1:
        s ="""
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

        for i in range(len(data)):
            row = data[i]
            if isinstance(row, list):
                if i == 0:
                    for j in range(len(row)):
                        tbl.cols.append(Num(count_tbl, j + 1, row[j], 0, 0, 0))
                        count_tbl += 1
                    tbl.rows.append(row)

                else:
                    row_for_tbl = []
                    for j in range(len(row)):
                        if row[j] == '?':
                            row[j] = tbl.cols[j].mean

                        tbl.cols[j].addToNum(row[j])
                        tbl.cols[j].updateMeanAndSdAdd(row[j])
                        row_for_tbl.append(row[j])
                    tbl.rows.append(Row(count_tbl, row_for_tbl))
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
            f.write("| | mu: " + str(i.mean) + "\n")
            f.write("| | n: " + str(i.count) + "\n")
            f.write("| | oid: " + str(i.oid) + "\n")
            f.write("| | sd: " + str(i.sd) + "\n")
            f.write("| | txt: " + str(i.txt) + "\n")
            k += 1
        k = 1
        f.write("t.oid" + str(tbl.oid) + "\n")
        f.write("t.rows\n")
        for i in range(1, len(tbl.rows)):
            f.write("| " + str(k) + "\n")
            f.write("| | cells\n")
            f.write("| | | " + ', '.join([str(elem) for elem in tbl.rows[i].lst]) + "\n")
            f.write("| | oid: " + str(tbl.rows[i].oid) + "\n")


for i in [1, 2, 3]:
    main(i)
