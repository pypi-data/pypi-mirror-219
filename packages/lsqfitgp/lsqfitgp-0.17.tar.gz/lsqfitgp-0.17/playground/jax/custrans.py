import jax
from jax.interpreters import ad
from jax import custom_transpose
from jax import test_util

@custom_transpose.custom_transpose
def f(x, y):
    return x * y

@f.def_transpose
def ft(ct, x, y):
    assert ad.is_undefined_primal(x) ^ ad.is_undefined_primal(y)
    if ad.is_undefined_primal(x):
        return ct * y, None
    else:
        return None, ct * x

@jax.custom_jvp
def g(x, y, z):
    return f(x, y) + z

@g.defjvp
def g_jvp(primals, tangents):
    x, y, z = primals
    xdot, ydot, zdot = tangents
    primal = g(*primals)
    tgx = f(xdot, y)
    tgy = f(x, ydot)
    return primal, tgx + tgy + zdot

test_util.check_grads(g, (1., 2., 3.), order=2, modes='fwd')
