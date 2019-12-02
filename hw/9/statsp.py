"""
T-test (parametric Significance Test)
Assuming the populations are bell-shaped curve, when are two curves not significantly different?
Note that many distributions are not normal so I use this tTest as a heuristic
for speed critical calculations. E.g. in the inner inner loop of some search
where I need a quick opinion about whether or not  "this" the same as "that".
But when assessing experimental results after all the algorithms have terminated,
I use a much safer, but somewhat slower, procedure (  and cliffsdelta).
"""


class Num:
    "An Accumulator for numbers"

    def __init__(i, inits=[]):
        i.n = i.m2 = i.mu = 0.0
        for x in inits: i.add(x)

    def s(i): return (i.m2 / (i.n - 1)) ** 0.5

    def add(i, x):
        i._median = None
        i.n += 1
        delta = x - i.mu
        i.mu += delta * 1.0 / i.n
        i.m2 += delta * (x - i.mu)

    def same(i, j, conf=0.95, small=0.38):
        return i.tTestSame(j, conf) or hedges(i, j, small)

    def tTestSame(i, j, conf=0.95):
        nom = abs(i.mu - j.mu)
        s1, s2 = i.s(), j.s()
        denom = ((s1 / i.n + s2 / j.n) ** 0.5) if s1 + s2 else 1
        df = min(i.n - 1, j.n - 1)
        return criticalValue(df, conf) >= nom / denom


# The above needs a magic threshold )(on the last line) for sayng enough is enough

def criticalValue(df, conf=0.95,
                  xs=[1, 2, 5, 10, 15, 20, 25, 30, 60, 100],
                  ys={0.9: [3.078, 1.886, 1.476, 1.372, 1.341, 1.325, 1.316, 1.31, 1.296, 1.29],
                      0.95: [6.314, 2.92, 2.015, 1.812, 1.753, 1.725, 1.708, 1.697, 1.671, 1.66],
                      0.99: [31.821, 6.965, 3.365, 2.764, 2.602, 2.528, 2.485, 2.457, 2.39, 2.364]}):
    return interpolate(df, xs, ys[conf])


def interpolate(x, xs, ys):
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    x0, y0 = xs[0], ys[0]
    for x1, y1 in zip(xs, ys):
        if x < x0 or x > xs[-1] or x0 <= x < x1:
            break
        x0, y0 = x1, y1
    gap = (x - x0) / (x1 - x0)
    return y0 + gap * (y1 - y0)


"""
Hedge's rule (using g):
- Still parametric
- Modifies Delta; w.r.t. the standard deviation of both samples.
- Adds a correction factor c for small sample sizes.
In their review of use of effect size in SE, Kampenses et al. report that many 
papers use something like g >= 0.38 as the boundary between small effects and bigger effects. 
See  equations 2,3,4 and Figure 9. or Systematic Review of Effect Size in
Software Engineering Experiments  Kampenes, Vigdis By, et al. 
Information and Software Technology 49.11 (2007): 1073-1086. 
"""


def hedges(i, j, small=0.38):
    """
    Hedges effect size test.
    Returns true if the "i" and "j" difference is only a small effect.
    "i" and "j" are   objects reporing mean (i.mu), standard deviation (i.s)
    and size (i.n) of two  population of numbers.
    """
    num = (i.n - 1) * i.s() ** 2 + (j.n - 1) * j.s() ** 2
    denom = (i.n - 1) + (j.n - 1)
    sp = (num / denom) ** 0.5
    delta = abs(i.mu - j.mu) / sp
    c = 1 - 3.0 / (4 * (i.n + j.n - 2) - 1)
    return delta * c < small
