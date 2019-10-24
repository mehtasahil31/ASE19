def tree(i,lst,y,yis,lvl=0):
    if len(lst) >= THE.tree.minObs*2:
      # find the best column
      lo, cut, col = 10**32, None, None
      for col1 in i.cols.indep:
        x = lambda row: row.cells[col1.pos]
        cut1, lo1 = col1.div(lst, x=x, y=y, yis=yis)
        if cut1:
          if lo1 < lo:
            cut, lo, col = cut1, lo1, col1
      # if a cut exists
      if cut:
        # split data on best col, call i.tree on each split
        x = lambda row: row.cells[col.pos]
        return [o(lo   = lo,
                  hi   = hi,
                  n    = len(kids),
                  txt  = col.txt,
                  kids = i.tree(kids,y,yis,lvl+1)
                ) for lo,hi,kids in col.split(lst, x, cut)]
    return yis(lst,key=y)