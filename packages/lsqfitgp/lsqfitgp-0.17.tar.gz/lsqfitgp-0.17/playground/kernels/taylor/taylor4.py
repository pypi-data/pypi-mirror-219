import functools

import jax
from jax import numpy as jnp
from jax.scipy import special as jspecial
from matplotlib import pyplot as plt

from lsqfitgp import _patch_jax

@functools.partial(jax.custom_jvp, nondiff_argnums=(0, 1, 2, 3))
def taylor(coefgen, args, n, m, x):
    c = coefgen(n, n + m, *args)
    k = jnp.arange(n, n + m)
    c = c * jnp.exp(jspecial.gammaln(1 + k) - jspecial.gammaln(1 + k - n))
    return jnp.polyval(c[::-1], x)

@taylor.defjvp
def taylor_jvp(coefgen, args, n, m, primals, tangents):
    x, = primals
    xt, = tangents
    return taylor(coefgen, args, n, m, x), taylor(coefgen, args, n + 1, m, x) * xt

def sgngamma(x):
    return jnp.where((x > 0) | (x % 2 < 1), 1, -1)

def coefgen_iv(s, e, nu):
    m = jnp.arange(s, e)
    u = 1 + m + nu
    return sgngamma(u) * jnp.exp(-jspecial.gammaln(1 + m) - jspecial.gammaln(u))

def ivmod(nu, x):
    return taylor(coefgen_iv, (nu,), 0, 5, (x / 2) ** 2)

def ivmod2(nu, x):
    return (x / 2) ** -nu * _patch_jax.iv(nu, x)

fig, ax = plt.subplots(num='taylor4', clear=True)

def deriv(f, i, a):
    if i == 0:
        return f
    else:
        return deriv(jax.grad(f, a), i - 1, a)
        
def vec1(f):
    return jax.vmap(f, (None, 0), 0)

x = 5 * jnp.linspace(0, 1, 1000)
nu = -1.3

for n in range(5):
    f1 = deriv(ivmod2, n, 1)
    f2 = deriv(ivmod, n, 1)
    f1 = vec1(f1)
    f2 = vec1(f2)
    y1 = f1(nu, x)
    y2 = f2(nu, x)
    ax.plot(x, y1, color=f'C{n}', label=f'{n}')
    ax.plot(x, y2, color=f'C{n}', linestyle='--')

ax.set_ylim(-1, 5)

fig.show()
