import sieve_gen

for n, i in zip(range(20), sieve_gen.sieve()):
    print i
