import functools
import click
def eros_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ctx = args[0]
        if not ctx.obj.get('eros'):
            return False
        return func(*args, **kwargs)
    return wrapper
