import functools

import jax
from jax import numpy as jnp
from jax.scipy import special as jspecial
from matplotlib import pyplot as plt

@functools.partial(jax.custom_jvp, nondiff_argnums=(0, 1))
def sincder(n, m, x):
    start = (n + 1) // 2
    k = jnp.arange(start, start + m)
    sign = jnp.where(k % 2, -1, 1)
    c = sign * jnp.exp(jspecial.gammaln(1 + 2 * k) - jspecial.gammaln(1 + 1 + 2 * k) - jspecial.gammaln(1 + 2 * k - n))
    coeff = jnp.zeros(2 * len(c) - 1 + n % 2).at[n % 2::2].set(c)
    return jnp.polyval(coeff[::-1], x)

@sincder.defjvp
def sincder_jvp(n, m, primals, tangents):
    x, = primals
    xt, = tangents
    return sincder(n, m, x), sincder(n + 1, m, x) * xt

fig, ax = plt.subplots(num='sincder2', clear=True)

x = 0.5 * jnp.linspace(-1, 1, 1000)

for n in range(5):
    f = jnp.sinc
    for i in range(n):
        f = jax.grad(f)
    f = jax.vmap(f)
    y1 = f(x)
    y2 = jnp.pi ** n * sincder(n, 2, jnp.pi * x)
    ax.plot(x, y1, color=f'C{n}', label=f'{n}')
    ax.plot(x, y2, color=f'C{n}', linestyle='--')

fig.show()
