# this is the sieve_iter implementation

class sieve(object):
    def __init__(self):
        self.primeslist = [2]
        self.start = self.primeslist[-1] + 1

    def __iter__(self):
        return self

    def next(self):
        while 1:
            isprime = True
            for i in self.primeslist:
                if self.start % i == 0:
                    isprime = False
            if isprime:
                self.primeslist.append(self.start)
                return self.start
            self.start += 1
