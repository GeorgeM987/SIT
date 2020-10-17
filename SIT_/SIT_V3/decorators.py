def trinket_high(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) / 65536
    return wrapper