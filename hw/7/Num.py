from Col import Col


class Num(Col):
    "Num class as a subclass of Col"

    def __init__(self, column_name="", position=0, weight=1):
        super().__init__(column_name, position, weight)
        self.mu = 0
        self.m2 = 0
        self.lo = 10 ** 32
        self.hi = -1 * 10 ** 32
        self.sd = 0

    def add_new_value(self, number):
        "Add new value to the list and update the paramaters"
        self.all_values.append(number)
        if number < self.lo:
            self.lo = number
        if number > self.hi:
            self.hi = number

        self.n += 1
        d = number - self.mu
        self.mu += d / self.n
        self.m2 += d * (number - self.mu)
        self.sd = 0 if self.n < 2 else (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5

    def dist(self, x, y):
        "Calculate distance between 2 rows"
        norm = lambda z: (z - self.lo) / (self.hi - self.lo + 10 ** -32)
        if x == "?":
            if y == "?": return 1
            y = norm(y)
            x = 0 if y > 0.5 else 1
        else:
            x = norm(x)
            if y == "?":
                y = 0 if x > 0.5 else 1
            else:
                y = norm(y)
        return abs(x - y)
