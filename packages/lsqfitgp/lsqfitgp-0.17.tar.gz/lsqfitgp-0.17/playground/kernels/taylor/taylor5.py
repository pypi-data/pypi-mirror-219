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

def kvmod(nu, x):
    factor = jnp.pi / (2 * jnp.sin(jnp.pi * nu))
    return factor * (ivmod(-nu, x) - (x / 2) ** (2 * nu) * ivmod(nu, x))

def kvmod2(nu, x):
    return (x / 2) ** nu * _patch_jax.kv(nu, x)

def ivmodx2_nearzero(nu, x2):
    return taylor(coefgen_iv, (nu,), 0, 5, x2 / 4)

def kvmodx2_nearzero(nu, x2):
    factor = jnp.pi / (2 * jnp.sin(jnp.pi * nu))
    return factor * (ivmodx2_nearzero(-nu, x2) - (x2 / 4) ** nu * ivmodx2_nearzero(nu, x2))

def kvmodx2(nu, x2):
    assert int(nu) != nu, nu
    nearzero = kvmodx2_nearzero(nu, x2)
    x = jnp.sqrt(x2)
    normal = (x / 2) ** nu * _patch_jax.kv(nu, x)
    return jnp.where(jnp.abs(x) < 1e-2, nearzero, normal)

fig, ax = plt.subplots(num='taylor5', clear=True)

def deriv(f, i, a):
    if i == 0:
        return f
    else:
        return deriv(jax.grad(f, a), i - 1, a)
        
def vec1(f):
    return jax.vmap(f, (None, 0), 0)

x = 0.01 * jnp.linspace(0, 1, 1000)
nu = 2.5

for n in range(5):
    f1 = deriv(kvmod2, n, 1)
    f2 = deriv(lambda v, x: kvmodx2(v, x ** 2), n, 1)
    f1 = vec1(f1)
    f2 = vec1(f2)
    y1 = f1(nu, x)
    y2 = f2(nu, x)
    ax.plot(x, y1, color=f'C{n}', label=f'{n}')
    ax.plot(x, y2, color=f'C{n}', linestyle='--')

ax.set_ylim(-1, 3)

fig.show()
