import functools
import jax

def value_and_ops(f, *ops, has_aux=False, **kw):
    if not ops:
        return f
    def fop(*args, **kw):
        y = f(*args, **kw)
        if has_aux:
            y, aux = y
            return y, (aux,)
        else:
            return y, ()
    def nextfop(fop):
        def nextfop(*args, **kw):
            y, aux = fop(*args, **kw)
            return y, aux + (y,)
        return nextfop
    for op in ops:
        fop = op(nextfop(fop), has_aux=True, **kw)
    @functools.wraps(f)
    def lastfop(*args, **kw):
        y, aux = fop(*args, **kw)
        if has_aux:
            return aux[1:] + (y,), aux[0]
        else:
            return aux + (y,)
    return lastfop

def f(x):
    print('ciao')
    return 1/2 * x ** 2, 'ciao'

fg = value_and_ops(f, jax.grad, jax.grad, jax.grad, has_aux=True)

print(fg(3.))
