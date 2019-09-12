import random


class Col:
    # Initializing
    def __init__(self):
        self.n = 0


class Num(Col):

    # Initializing
    def __init__(self):
        super(Num, self).__init__()
        self.mu = self.m2 = self.sd = 0
        self.lo = 10**32
        self.hi = -1*self.lo

    # Calculating continuous mean and standard deviation of incoming stream of numbers
    def Num1(self, v):
        self.n += 1
        if self.lo > v:
            self.lo = v
        if self.hi < v:
            self.hi = v
        d = v - self.mu
        self.mu += d/self.n
        self.m2 += d*(v - self.mu)
        self.sd = self._NumSd()
        return v

    # Standard deviation helper function
    def _NumSd(self):
        if self.m2 < 0:
            return 0
        if self.n < 2:
            return 0
        return (self.m2/(self.n-1))**0.5

    # Normalizing the numbers
    def NumNorm(self,x):
        return (x-self.lo)/(self.hi-self.lo + 10**(-32))

    # Updating the mean and standard deviation after every number is removed.
    def NumLess(self, v):
        if self.n < 2:
            self.sd = 0
            return v
        self.n -= 1
        if self.lo > v:
            self.lo = v
        if self.hi < v:
            self.hi = v
        d = v - self.mu
        self.mu -= d / self.n
        self.m2 -= d * (v - self.mu)
        self.sd = self._NumSd()
        return v

class Sym(Col):
    pass

class Some(Col):
    pass

if __name__ == "__main__":

    # Initializing object and lists.
    X = Num()
    sd_inc = []
    mu_inc = []
    sd_dec = []
    mu_dec = []

    # Creating a list(size 100) of random numbers between 1 and 100 both inclusive.
    randomlist = [random.randint(1,101) for i in range(101)]

    # Passing numbers from randomlist one by and calculating mean and standard deviation,
    # storing cumulative mean and standard deviation after adding every 10 numbers.
    for i in range(100):
        X.Num1(randomlist[i])
        if (i+1)%10 == 0:
            sd_inc.append(X.sd)
            mu_inc.append(X.mu)

    # Removing numbers from randomlist one by one in reverse and calculating mean and standard deviation,
    # storing cumulative mean and standard deviation after removing every 10 numbers
    for i in range(99,8,-1):
        if (i+1) % 10 == 0:
            mu_dec.append(X.mu)
            sd_dec.append(X._NumSd())
        X.NumLess(randomlist[i])

    sd_dec = sd_dec[::-1]
    mu_dec = mu_dec[::-1]

    # Writing results in out.txt for comparison
    f = open("output.txt", "w+")
    f.write("List of 100 random number (between 1 to 100): " + str(randomlist))
    f.write("\n")
    f.write("\n")
    f.write("| While Adding  | While Subtracting |")
    f.write("\n")
    f.write("|  Mean  |  SD  |   Mean   |   SD   |")

    for i in range(len(sd_inc)):
        f.write("\n")
        f.write("| " +'{:.3f}'.format(mu_inc[i]) + " |" + '{:.3f}'.format(sd_inc[i]) + "|  " + '{:.3f}'.format(mu_dec[i]) + "  | " + '{:.3f}'.format(sd_dec[i]) + " |")

    f.close()






