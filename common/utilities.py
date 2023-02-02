def run_once(func):
    def inner(*args, **kwargs):
        if not inner.has_run:
            result = func(*args, **kwargs)
            inner.has_run = True
            return result

    inner.has_run = False
    return inner
