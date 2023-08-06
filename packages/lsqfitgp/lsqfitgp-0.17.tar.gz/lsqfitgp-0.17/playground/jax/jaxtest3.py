import jax
from jax import numpy as jnp
import numpy as np

import lsqfitgp as lgp

def f(a, x):
    print(a)
    return 2 * x

g = jax.vmap(jax.grad(f, 1), in_axes=(None, 0))

print(g(lgp.StructuredArray(np.zeros(1, 'f8,f8')), jnp.ones(1)))

def f(x, *, a):
    print(a)
    return 3 * x

g = jax.vmap(jax.grad(f))

print(g(jnp.ones(1), a=lgp.StructuredArray(np.zeros(1, 'f8,f8'))))

def f(x):
    assert x['a'].shape == ()
    print(x.get('c'))
    return x['a'] + 2 * x['b']

g = jax.vmap(f)

print(g(dict(a=jnp.ones(5), b=jnp.arange(5.), c=lgp.StructuredArray(np.zeros(5, 'f8,f8')))))

u = jax.vmap(jax.grad(f))
print(u(dict(a=jnp.ones(5), b=jnp.arange(5.), c=lgp.StructuredArray(np.zeros(5, 'f8,f8')))))

def f(x):
    return x['f0'] + 2.3 * x['f1']

def g(x, f1):
    x['f1'] = f1
    return f(x)

h = jax.jacfwd(g, 1)

i = jax.vmap(h)

def j(x):
    return i(x, x['f1'])

print(j(lgp.StructuredArray(np.ones(5, 'f8,f8'))))
