import sieve_gen

for i in sieve_gen.sieve():
    print i
    if i > 20:
        break

