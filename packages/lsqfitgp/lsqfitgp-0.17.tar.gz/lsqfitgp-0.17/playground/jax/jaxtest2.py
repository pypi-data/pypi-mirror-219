import functools

import jax
from jax import numpy as jnp

import lsqfitgp as lgp

indentation = 0
def trace(fun):
    if hasattr(fun, '_traced'):
        return fun
    @functools.wraps(fun)
    def tracefun(*args, **kw):
        global indentation
        space = '    ' * indentation
        arglist = ', '.join(list(map(repr, args)) + [f'{k}={v!r}' for k, v in kw.items()])
        print(space + fun.__name__ + '(' + arglist + ')')
        indentation += 1
        rt = fun(*args, **kw)
        indentation -= 1
        out = ('\n' + space).join(repr(rt).split('\n'))
        print(space + '-> ' + out)
        return rt
    tracefun._traced = True
    return tracefun

def f(x):
    d = lgp._linalg.EigCutFullRank(jnp.array([[x]]))
    return d.quad(jnp.array([2.]), jnp.array([3.]))

g = jax.grad(f)
# print(g(1.))

@jax.custom_jvp
def f(x):
    return jnp.sum(x)

@f.defjvp
def fjvp(primals, tangents):
    x, = primals
    xdot, = tangents
    return f(x), jnp.ones(len(x)).reshape(xdot.shape) @ ((jnp.eye(len(x)) @ xdot).T / jnp.ones(len(x)))

print(jax.jacfwd(f)(jnp.ones(3)))
print(jax.jacrev(f)(jnp.ones(3)))
