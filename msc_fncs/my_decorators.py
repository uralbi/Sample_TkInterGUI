import time
from msc_fncs.fncs import min_sec


def timing(func):
    def wrapper(*args, **kwargs):
        bgn = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'{"-"*10}| Time consumed:', f"{min_sec(end-bgn)} |{'-'*10}")
    return wrapper