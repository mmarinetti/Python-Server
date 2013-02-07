import sieve_iter

for n, i in zip(range(3), sieve_iter.sieve()):
    print i
