import jax
from jax import core

t = []

def f(x):
    global t
    t.append(x)
    return x

g = jax.jit(f)
h = jax.grad(f)
i = jax.jit(jax.grad(f))
j = jax.vmap(f)
k = jax.grad(jax.grad(f))
l = jax.jacfwd(f)
