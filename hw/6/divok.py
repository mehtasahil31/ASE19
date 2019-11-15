#!/usr/bin/env python3 
# vim: sta:et:sw=2:ts=2:sts=2

from div import Div
from lib import *

if __name__ == "__main__":
    seed(1)
    n = 10000
    d = Div([r() * 0.05 for _ in range(n)] +
            [0.2 + r() * 0.05 for _ in range(n)] +
            [0.4 + r() * 0.05 for _ in range(n)] +
            [0.6 + r() * 0.05 for _ in range(n)] +
            [0.8 + r() * 0.05 for _ in range(n)])

    for x in d.ranges:
        print("! %5s   %6.4f    %6.4f" % (x.n, x.lo, x.hi))
    print(d.b4.sd(), d.gain)

    print("")
    #  0                   1
    #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
    d = Div([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2])
    for x in d.ranges:
        print("! %5s   %6.4f    %6.4f" % (x.n, x.lo, x.hi))
    print(d.b4.sd(), d.gain)

print("")
#  0                   1
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
d = Div([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1])
for x in d.ranges:
    print("! %5s   %6.4f    %6.4f" % (x.n, x.lo, x.hi))
print(d.b4.sd(), d.gain)
