# this is the implementation of the sieve generator

primeslist = [2]

def sieve():
    start = primeslist[-1] + 1
    while 1:
        isprime = True
        for i in primeslist:
            if start % i == 0:
                isprime = False
        if isprime:
            primeslist.append(start)
            yield start
        start += 1
