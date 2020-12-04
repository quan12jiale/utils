# -*- coding: utf-8 -*-
import time
import functools

@functools.lru_cache(maxsize=5)
def fib(n : int):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

if __name__ == "__main__":
    t1 = time.time()
    fib(30)
    print('Time taken: {}'.format(time.time()-t1))
