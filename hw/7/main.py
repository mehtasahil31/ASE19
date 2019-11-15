import random, math
from Num import Num
from Tbl import Tbl, cells, cols, rows, file

seed = random.seed


class Tree:
    def __init__(self):
        self.children = []
        self.leaves = []
        self.level = 0
        self.isRoot = False
        self.splitCount = 0


def printt(root):
    if not root.isRoot:
        for _ in range(root.level):
            print("|. ", end=" ")
    print(root.splitCount)
    if len(root.children) == 0:
        for _ in range(root.level - 1):
            print("|. ", end=" ")
        for col in root.leaves:
            print(col.column_name + " = ", end=" ")
            if isinstance(col, Num):
                print("{0} ({1})".format(col.mu, col.sd), end=" ")
            else:
                print("{0} ({1})".format(col.mode, col.entropy), end=" ")
        print("")
    else:
        for each in root.children:
            printt(each)
    if root.isRoot:
        for col in root.leaves:
            print(col.column_name + " = ", end=" ")
            if isinstance(col, Num):
                print("{0} ({1})".format(col.mu, col.sd), end=" ")
            else:
                print("{0} ({1})".format(col.mode, col.entropy), end=" ")


def dist(row1, row2, cols):
    d, n, p = 0, 0, 2
    for col in cols:
        n += 1
        d0 = col.dist(row1.cells[col.position], row2.cells[col.position])
        d += d0 ** p
        d += d0 ** p
    return d ** (1 / p) / n ** (1 / p)


def cos(x, y, z, d, cols):
    return (dist(x, z, cols) ** 2 + d ** 2 - dist(y, z, cols) ** 2) / (2 * d)


class hw7:
    def __init__(self, file_name):
        seed(1)
        self.file_contents = cells(cols(rows(file(file_name))))
        self.tbl = Tbl()
        self.file_processing()
        self.tree = self.split(self.tbl, 0)
        printt(self.tree)

    def file_processing(self):
        for idx, row in enumerate(self.file_contents):
            if idx:
                self.tbl.addRow(row)
            else:
                self.tbl.addCol(row)

    def split(self, tbl, level):
        node = Tree()
        if len(tbl.rows) < 2 * pow(len(self.tbl.rows), 1 / 2):
            for each in tbl.w['goals']:
                node.leaves.append(tbl.cols[each])
            node.level, node.splitCount = level, len(tbl.rows)
        else:
            best_tuple, best_points = self.pivotPoints(tbl)
            tbl_left, tbl_right = Tbl(), Tbl()
            self.getSingleNode(best_points, tbl_left, level, tbl_right, node, tbl)
        return node

    def getSingleNode(self, best_points, left_tbl, level, right_tbl, node, tbl):
        left_tbl.addCol([col.column_name for col in tbl.cols])
        right_tbl.addCol([col.column_name for col in tbl.cols])
        for idx, each in enumerate(tbl.rows):
            if idx in best_points:
                right_tbl.addRow(each.cells)
            else:
                left_tbl.addRow(each.cells)
        splitCount = len(left_tbl.rows) + len(right_tbl.rows)
        node.children.append(self.split(left_tbl, level + 1))
        node.children.append(self.split(right_tbl, level + 1))
        node.splitCount = splitCount
        node.level = level

    def mapper(self, tbl):
        cols = [tbl.cols[col] for col in tbl.w['xs']]
        random_point = random.randint(0, len(tbl.rows) - 1)
        first_pivot_idx = self.firstPivot(cols, random_point, tbl)
        second_pivot_idx, second_pivot_pts = self.secPivot(cols, first_pivot_idx, tbl)
        d = second_pivot_pts[math.floor(len(second_pivot_pts) * 0.9)][1]
        return first_pivot_idx, second_pivot_idx, d

    def firstPivot(self, cols, random_point, tbl):
        first_pivot_pts = []
        for row in range(0, len(tbl.rows)):
            d = dist(tbl.rows[random_point], tbl.rows[row], cols)
            first_pivot_pts.append((row, d))
        first_pivot_pts.sort(key=lambda x: x[1])
        first_pivot_idx = first_pivot_pts[math.floor(len(first_pivot_pts) * 0.9)][0]
        return first_pivot_idx

    def secPivot(self, cols, first_pivot_idx, tbl):
        second_pivot_pts = []
        for row in range(0, len(tbl.rows)):
            d = dist(tbl.rows[first_pivot_idx], tbl.rows[row], cols)
            second_pivot_pts.append((row, d))
        second_pivot_pts.sort(key=lambda x: x[1])
        second_pivot_idx = second_pivot_pts[math.floor(len(second_pivot_pts) * 0.9)][0]
        return second_pivot_idx, second_pivot_pts

    def pivotPoints(self, tbl):
        counter = 10
        initial = len(tbl.rows)
        best_tuple = None
        best_points = None
        while counter > 0:
            counter -= 1
            tuple = self.mapper(tbl)
            all_list = self.sortedlist(tuple, tbl)
            length = len(all_list)
            index = (length - 1) // 2
            median_distance = self.meandist(all_list, index, length)
            point_set = self.get_point_set(all_list, median_distance)
            right = abs(len(point_set) - (length - len(point_set)))
            if right < initial:
                initial, best_points, best_tuple = right, point_set, tuple
        return best_tuple, best_points

    def get_point_set(self, all_list, median_distance):
        pointset = set()
        for point in all_list:
            if point[1] < median_distance:
                pointset.add(point[0])
        return pointset

    def meandist(self, all_list, index, length):
        if length % 2:
            median_distance = all_list[index][1]
        else:
            median_distance = (all_list[index][1] + all_list[index + 1][1]) / 2.0
        return median_distance

    def sortedlist(self, pivot_tuple, tbl):
        all_list = []
        cols = [tbl.cols[col] for col in tbl.w['xs']]
        for row in range(0, len(tbl.rows)):
            dist = cos(tbl.rows[pivot_tuple[0]], tbl.rows[pivot_tuple[1]], tbl.rows[row], pivot_tuple[2], cols)
            all_list.append((row, dist))
        all_list.sort(key=lambda x: x[1])
        return all_list

    def op(filename):
        print(filename.split('.')[0])
        hw_7 = hw7(filename)


if __name__ == '__main__':
    hw7.op('pom310000.csv')
    hw7.op('xomo10000.csv')
