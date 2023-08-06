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

def coefgen_jv(s, e, nu):
    k = jnp.arange(s, e)
    m = k // 2
    return jnp.where(k % 2, 0, (-1) ** m / jnp.exp(jspecial.gammaln(1 + m) + jspecial.gammaln(1 + m + nu)))

def jvmod(nu, x):
    return taylor(coefgen_jv, (nu,), 0, 10, x / 2)

def jvmod2(nu, x):
    return (x / 2) ** -nu * _patch_jax.jv(nu, x)

fig, ax = plt.subplots(num='taylor', clear=True)

def deriv(f, i, a):
    if i == 0:
        return f
    else:
        return deriv(jax.grad(f, a), i - 1, a)
        
def vec1(f):
    return jax.vmap(f, (None, 0), 0)

x = 0.5 * jnp.linspace(0, 0.01, 1000)
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
