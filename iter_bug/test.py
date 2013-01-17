import fib

def test1():
    f = fib.fib()
    i = iter(f)
    assert i.next() == 2

def test2():
    f = fib.fib()
    i = iter(f)
    i.next()
    assert i.next() == 3

def test3():
    f = fib.fib()
    i = iter(f)
    i.next()
    i.next()
    assert i.next() == 5

test1()
test2()
test3()

