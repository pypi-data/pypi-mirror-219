import jax
from jax import numpy as jnp

def f(x, p):
    return x ** p

df = jax.grad(f)
ddf = jax.grad(df)

print(df(0., 1.))
print(ddf(0., 1.))
print(df(0., 0.))
