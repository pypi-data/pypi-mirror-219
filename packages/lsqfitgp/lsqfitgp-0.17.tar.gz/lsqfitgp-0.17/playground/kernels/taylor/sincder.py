from jax import numpy as jnp
from matplotlib import pyplot as plt

def sincder1(x):
    return (x * jnp.cos(x) - jnp.sin(x)) / x ** 2

def sincder2(x):
    a = jnp.expm1(-2j * x + jnp.log1p(1j * x) - jnp.log1p(-1j * x))
    b = jnp.exp(1j * x) * (1 - 1j * x) / (2j * x ** 2)
    return jnp.real(a * b)
    
xtrue = jnp.logspace(-16, 0, 1000)
ytrue = sincder2(xtrue)
x = xtrue.astype('f')
y1 = sincder1(x)
y2 = sincder2(x)

fig, ax = plt.subplots(num='sincder', clear=True)

ax.plot(x, jnp.abs((y1 - ytrue) / ytrue))
ax.plot(x, jnp.abs((y2 - ytrue) / ytrue))
ax.set_xscale('log')
ax.set_yscale('log')

fig.show()
