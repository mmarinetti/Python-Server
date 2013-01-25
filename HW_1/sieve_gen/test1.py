import sieve_gen

for n, i in zip(range(9), sieve_gen.sieve()):
    print i
