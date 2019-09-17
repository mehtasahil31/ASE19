class Abcd():

    def __init__(self, rx, data):
        self.known = {}
        self.a = {}
        self.b = {}
        self.c = {}
        self.d = {}
        self.rx = "rx" if rx == "" else rx
        self.data = "data" if data == "" else data
        self.yes = self.no = 0

    def Abcd1(self, want, got):

        if not self.known.get(want):
            self.known[want] = 1
            self.a[want] = self.yes + self.no
        else:
            self.known[want] += 1

        if not self.known.get(got):
            self.known[got] = 1
            self.a[got] = self.yes + self.no
        else:
            self.known[got] += 1

        if want == got:
            self.yes += 1
        else:
            self.no += 1

        for x in self.known:
            if want == x:
                if want == got:
                    if self.d.get(x):
                        self.d[x] += 1
                    else:
                        self.d[x] = 1
                else:
                    if self.b.get(x):
                        self.b[x] += 1
                    else:
                        self.b[x] = 1
            else:
                if x == got:
                    if self.c.get(x):
                        self.c[x] += 1
                    else:
                        self.c[x] = 1
                else:
                    if self.a.get(x):
                        self.a[x] += 1
                    else:
                        self.a[x] = 1

    def AbcdReport(self):

        p = " {: >4.2f}"
        q = " {: >4}"
        r = " {: >5}"
        s = " |"
        ds = "----"
        print(r.format("db") + s + r.format("rx") + s + r.format("num") + s + r.format("a") + s + r.format("b") + s + r.format("c") + s + r.format("d") + s
              + q.format("acc") + s + q.format("pre") + s + q.format("pd") + s + q.format("pf") + s + q.format("f") + s + q.format("g") + s + " class")
        print(r.format(ds) + s + r.format(ds) + s + r.format(ds) + s + r.format(ds) + s + r.format(ds) + s + r.format(ds) + s + r.format(ds) + s
              + q.format(ds) + s + q.format(ds) + s + q.format(ds) + s + q.format(ds) + s + q.format(ds) + s + q.format(ds) + s + " -----")

        for x in self.known:
            pd = pf = pn = prec = g = f = acc = 0
            a = self.a[x] if x in self.a else 0
            b = self.b[x] if x in self.b else 0
            c = self.c[x] if x in self.c else 0
            d = self.d[x] if x in self.d else 0

            if b + d > 0:
                pd = d / (b + d)
            if a + c > 0:
                pf = c / (a + c)
            if a + c > 0:
                pn = (b + d) / (a + c)
            if c + d > 0:
                prec = d / (c + d)
            if 1 - pf + pd > 0:
                g = 2 * (1 - pf) * pd / (1 - pf + pd)
            if prec + pd > 0:
                f = 2 * prec * pd / (prec + pd)
            if self.yes + self.no > 0:
                acc = self.yes / (self.yes + self.no)

            print(r.format(self.data) + s + r.format(self.rx) + s + r.format(self.yes + self.no) + s + r.format(a) + s + r.format(b) + s + r.format(c) + s +
                  r.format(d) + s + p.format(acc) + s + p.format(prec) + s + p.format(pd) + s + p.format(pf) + s + p.format(f) + s + p.format(g) + s + " " + x)



abcd = Abcd("rx", "data")

for i in range(6):
    abcd.Abcd1("yes", "yes")

for i in range(2):
    abcd.Abcd1("no", "no")

for i in range(5):
    abcd.Abcd1("maybe", "maybe")

abcd.Abcd1("maybe", "no")

abcd.AbcdReport()

