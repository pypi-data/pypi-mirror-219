import functools

import jax
from jax import numpy as jnp

class Cippa:
    pass

def oldinit(self, x):
    self.x = x
    
# @functools.partial(jax.custom_jvp, nondiff_argnums=(0,))
# def init(self, x):
#     oldinit(self, x)
#     return 0.
#
# @init.defjvp
# def initjvp(self, primals, tangents):
#     x, = primals
#     x_dot, = tangents
#     return init(self, x), x_dot

def notracer(x):
    if isinstance(x, jax.core.Tracer):
        return notracer(x.primal)
    else:
        return x
    
def __init__(self, x):
    oldinit(self, notracer(x))
    self._x = x
    
def oldciao(self, a):
    return self.x * a

@functools.partial(jax.custom_jvp, nondiff_argnums=(0,))
def ciaoimpl(self, x, a):
    return oldciao(self, a)

@ciaoimpl.defjvp
def ciaojvp(self, primals, tangents):
    x, a = primals
    x_dot, a_dot = tangents
    return ciaoimpl(self, x, a), x_dot * a + x * a_dot

def ciao(self, a):
    return ciaoimpl(self, self._x, a)

Cippa.__init__ = __init__
Cippa.ciao = ciao

@functools.partial(jax.custom_jvp, nondiff_argnums=(0,))
def f(a, x):
    print(a)
    return x

@f.defjvp
def fjvp(a, primals, tangents):
    x, = primals
    x_dot, = tangents
    return f(a, x), x_dot

jax.grad(lambda x: Cippa(x).ciao(2.))(3.)
# def g(x):
#     return f('cippa', x)
# print(jax.grad(g)(2.))
