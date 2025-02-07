import functools
import time

def timer(func):
    """
    If you decorate a function with this, it will time the period taken to run the decorated function.
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time ({func.__name__}): {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer