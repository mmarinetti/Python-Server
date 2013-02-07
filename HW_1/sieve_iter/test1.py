import sieve_iter

for n, i in zip(range(9), sieve_iter.sieve()):
    print i
