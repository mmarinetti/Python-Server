# an implementation of Eratosthenes' Sieve:
#   http://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

_primeslist = [2]

def _is_prime(primes, n):
    for i in primes:
        if n % i == 0:
            return False
    return True

def next():
    start = _primeslist[-1] + 1
    while 1:
        if _is_prime(_primeslist, start):
            _primeslist.append(start)
            return start

        start += 1

for n in range(10):
    print next()
