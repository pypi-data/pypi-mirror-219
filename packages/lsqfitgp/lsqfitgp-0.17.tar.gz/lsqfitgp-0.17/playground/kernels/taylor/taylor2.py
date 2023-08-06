import functools

import jax
from jax import numpy as jnp
from jax.scipy import special as jspecial
from matplotlib import pyplot as plt

from lsqfitgp import _patch_jax

@functools.partial(jax.custom_jvp, nondiff_argnums=(0, 1, 2, 3))
def taylor_even(coefgen, args, n, m, x):
    start = (n + 1) // 2
    c = coefgen(start, start + m, *args)
    k = 2 * jnp.arange(start, start + m)
    c = c * jnp.exp(jspecial.gammaln(1 + k) - jspecial.gammaln(1 + k - n))
    coeff = jnp.zeros(2 * len(c) - 1 + n % 2).at[n % 2::2].set(c)
    return jnp.polyval(coeff[::-1], x)

@taylor_even.defjvp
def taylor_even_jvp(coefgen, args, n, m, primals, tangents):
    x, = primals
    xt, = tangents
    return taylor_even(coefgen, args, n, m, x), taylor_even(coefgen, args, n + 1, m, x) * xt

def coefgen_jv(s, e, nu):
    m = jnp.arange(s, e)
    return (-1) ** m / jnp.exp(jspecial.gammaln(1 + m) + jspecial.gammaln(1 + m + nu))

def jvmod(nu, x):
    return taylor_even(coefgen_jv, (nu,), 0, 5, x / 2)

def jvmod2(nu, x):
    return (x / 2) ** -nu * _patch_jax.jv(nu, x)

fig, ax = plt.subplots(num='taylor2', clear=True)

def deriv(f, i, a):
    if i == 0:
        return f
    else:
        return deriv(jax.grad(f, a), i - 1, a)
        
def vec1(f):
    return jax.vmap(f, (None, 0), 0)

x = 5 * jnp.linspace(0, 1, 1000)
nu = 1.3

for n in range(5):
    f1 = deriv(jvmod2, n, 1)
    f2 = deriv(jvmod, n, 1)
    f1 = vec1(f1)
    f2 = vec1(f2)
    y1 = f1(nu, x)
    y2 = f2(nu, x)
    ax.plot(x, y1, color=f'C{n}', label=f'{n}')
    ax.plot(x, y2, color=f'C{n}', linestyle='--')

ax.set_ylim(-1, 1)

fig.show()
