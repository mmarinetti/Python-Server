# this is an implementation of the 'fib' functionality using a module.

last_1 = 1    #1. 1 assigned to last_1
last_2 = 1    #2. 1 assigned to last_2

def next():
    global last_1, last_2

    next_fib = last_1 + last_2        #
    last_1, last_2 = last_2, next_fib
    
    return next_fib
