from Col import Col
import math

class Num(Col):
    def __init__(self):
        Col.__init__(self)
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.hi = -1 * 10 ** 32
        self.lo = 1 * 10 ** 32
        self.count = 0

    # Function to calculate the SD using variance
    def _numSd(self, count):
        if count == 1:
            self.sd = 0
        else:
            self.sd = (self.m2 / (count - 1)) ** 0.5

    def _numSd2(self):
        if self.count == 1:
            self.sd = 0
        else:
            self.sd = (self.m2 / (self.count - 1)) ** 0.5

    # Method to incrementally update mean and standard deviation
    def num1(self, arr):
        count = 0
        for i in range(len(arr)):
            if arr[i] > self.hi:
                self.hi = arr[i]
            if arr[i] < self.lo:
                self.lo = arr[i]
            count += 1
            delta = arr[i] - self.mu
            self.mu += (delta / count)
            delta2 = arr[i] - self.mu
            # Calculation of square mean distance
            self.m2 += delta * delta2
            self._numSd(count)
        return round(self.mu, 2), round(self.sd, 2), round(self.m2, 2), count, self.hi, self.lo

    def num2(self, val):
        if val > self.hi:
            self.hi = val
        if val < self.lo:
            self.lo = val
        self.count += 1
        delta = val - self.mu
        self.mu += (delta / self.count)
        delta2 = val - self.mu
        self.m2 += delta * delta2
        self._numSd2()

    def NumLike(self, x, m, cls):
        var = self.sd ** 2
        denom = math.sqrt(math.pi * 2 * var)
        num = (2.71828 ** (-(x - self.mu) ** 2) / (2 * var + 0.0001))
        if m == cls:
            self.num2(x)
        return num / (denom + 10 ** (-64)) + 10 ** (-64)
