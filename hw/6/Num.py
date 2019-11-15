from Col import Col
from the import THE

class Num(Col):
    "Num class as a subclass of Col"

    def __init__(self, column_name="", pos=0, weight=1):
        super().__init__(column_name, pos, weight)
        self.mu = 0
        self.m2 = 0
        self.lo = 10 ** 32
        self.hi = -1 * 10 ** 32
        self.sd = 0

    def addVal(self, number):
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

    def remove_from_behind(self):
        "Remove a value from behind the list"
        number = self.all_values.pop()
        self.removeVal(number)

    def remove_from_front(self):
        "Remove a value from front of the list"
        number = self.all_values.pop(0)
        self.removeVal(number)

    def removeVal(self, number):
        if self.n < 2:
            self.n, self.mu, self.m2 = 0, 0, 0
        else:
            self.n -= 1
            d = number - self.mu
            self.mu -= d / self.n
            self.m2 -= d * (number - self.mu)
            self.sd = 0 if self.n < 2 else (self.m2 / (self.n - 1 + 10 ** -32)) ** 0.5

    def num_like(self, x):
        "Determines how much Num class likes a symbol"
        var = self.sd ** 2
        denom = (3.14159 * 2 * var) ** 0.5
        num = 2.71828 ** (-(x - self.mu) ** 2 / (2 * var + 0.0001))
        return num / (denom + 10 ** -64)

    def variety(self):
        return self.sd

    def xpect(self, second_class):
        total_n = self.n + second_class.n
        return (self.sd * self.n / total_n) + (second_class.sd * second_class.n / total_n)

    def norm(self, val):
        return (val - self.lo) / (self.hi - self.lo + 10 ** -32)

    def dist(self, val1, val2):
        "Calculate distance between 2 rows"
        norm = lambda z: (z - self.lo) / (self.hi - self.lo + 10 ** -32)
        if val1 == THE.char.skip:
            if val2 == THE.char.skip: return 1
            val2 = norm(val2)
            val1 = 0 if val2 > 0.5 else 1
        else:
            val1 = norm(val1)
            if val2 == THE.char.skip:
                val2 = 0 if val1 > 0.5 else 1
            else:
                val2 = norm(val2)
        return abs(val1 - val2)
