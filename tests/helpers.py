

def strip_wrappers(fn):
    """ For decorated fn, return function with stirpped decorator """
    if not hasattr(fn, 'func_closure') or not fn.func_closure:
        return fn
    for f in fn.func_closure:
        f = f.cell_contents
        if hasattr(f, '__call__'):
            return strip_wrappers(f)
    return fn
