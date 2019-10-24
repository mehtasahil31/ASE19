#!/usr/bin/env python3 
# vim: nospell:sta:et:sw=2:ts=2:sts=2
"""
Divide numbers.
"""

import math
from lib import THE, Pretty, same, first, last, ordered
from copy import deepcopy
from thing import Num, Sym


class Div2_2(Pretty):
    """
    Recursively divide a list of numns by finding splits
    that minimizing the expected value of the standard
    deviation (after the splits).
    """

    def __init__(self, lst, x=first, y=last):
        self.x = x
        self.y = y
        self.lst = ordered(lst, key=x)
        self.xtype = Num(self.lst,key=x)
        self.ytype = Sym(self.lst, key=y)
        self.gain = 0  # where we will be, once done
        #i.x = x  # how to get values from 'lst' items
        self.step = int(len(self.lst) ** THE.div.min)  # each split need >= 'step' items
        self.stop = x(last(self.lst))  # top list value
        self.start = x(first(self.lst))  # bottom list value
        self.ranges = []  # the generted ranges
        self.epsilon = self.xtype.sd() * THE.div.cohen  # bins must be seperated >= epsilon
        self.divide(1, len(self.lst), 1)
        self.gain /= len(self.lst)

    #TODO: check the argument passing thing
    def divide(self, lo, hi, rank):
        "Find a split between lo and hi, then recurse on each split."
        xleft = Num(key=self.x)
        yleft = Sym(key=self.y)
        xright = Num(self.lst[lo:hi], key=self.x)
        yright = Sym(self.lst[lo:hi], key=self.y)
        xb4 = deepcopy(xright)
        yb4 = deepcopy(yright)
        best = yb4.variety()
        cut = None
        for j in range(lo, hi):
            xleft + self.lst[j]
            yleft + self.lst[j]
            xright - self.lst[j]
            yright - self.lst[j]
            if xleft.n >= self.step:
                if xright.n >= self.step:
                    now = self.x(self.lst[j - 1])
                    after = self.x(self.lst[j])
                    if now == after: continue
                    if abs(xright.mu - xleft.mu) >= self.epsilon:
                        if after - self.start >= self.epsilon:
                            if self.stop - now >= self.epsilon:
                                xpect = yleft.xpect(yright)
                                if xpect * THE.div.trivial < best:
                                    best, cut = xpect, j
        if cut:
            rank = self.divide(lo, cut, rank) + 1
            rank = self.divide(cut, hi, rank)
        else:
            self.gain += xb4.n * xb4.variety()
            xb4.rank = rank
            self.ranges += [(xb4, yb4)]
        return rank
