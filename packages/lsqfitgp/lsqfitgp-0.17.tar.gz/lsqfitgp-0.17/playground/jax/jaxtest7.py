import jax
from jax import numpy as jnp
import numpy

def f(x):
    u = numpy.array(5.)
    if numpy.all(u > 0):
        print('ciao!')
    return x

g = jax.jit(f)
g(0)
