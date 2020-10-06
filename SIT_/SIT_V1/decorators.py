import time
#

def adjust_voltage_val(func):
    def wrapper(*args, **kwargs):
        if func(*args, **kwargs)[0] >= 1.5:
            v_min = func(*args, **kwargs)[0]
            v_min = 0.25 * 2.0
            return 'Value exceeding min threshold!\nAdjusted to: {}'.format(v_min)
        if func(*args, **kwargs)[-1] >= 5.0:
            v_max = func(*args, **kwargs)[-1]
            v_max = 2.5 * 2.0
            return 'Value exceeding max threshold!\nAdjusted to: {}'.format(v_max)
        else:
            return func(*args, **kwargs)
    return wrapper

def delta_t(func):
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        func(*args, **kwargs)
        end = time.monotonic()
        elapsed = end - start
        return elapsed, func(*args, **kwargs)
    return wrapper

def trinket_high(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) / 65536
    return wrapper