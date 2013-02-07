last_1 = 1    #1. 1 assigned to last_1
last_2 = 1    #2. 1 assigned to last_2

def next():
    global last_1, last_2

    next_fib = last_1 + last_2        #4. last_1+last_2 assigned to next_fib
    last_1, last_2 = last_2, next_fib #5. last_2 assigned to last_1 and
                                      #   next_fib assigned to last_2
    return next_fib                   #6. return next_fib

print next()    #3. print 2
print next()    #7. print 3
print next()    #11. print 5
