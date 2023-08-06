"""

Check the hypothesis that the space of valid autoregressive characteristic
polynomials is a simplex with vertices (1-x)^n (1+x)^(p-n) for n = 0, 1, ..., p.

The hypothesis turned out false.

"""

import numpy as np
from matplotlib import pyplot as plt
import jax
from jax import numpy as jnp

import lsqfitgp as lgp

class AR(lgp.AR):
    
    @staticmethod
    def phi_vertices(p):
        assert int(p) == p and p >= 0, p
        roots = jnp.where(jnp.arange(p + 1)[:, None] <= jnp.arange(p), 1, -1)
        return jax.vmap(lambda r: -jnp.atleast_1d(jnp.poly(r))[1:])(roots)
        # TODO possibly not accurate for large p, see phi_from_roots,
        # it can be probably written more efficiently with binomial power
        # expansion, and the output should be integer type
    
    @staticmethod
    def phi_from_baricentric(a, vertices):
        a = jnp.asarray(a)
        vertices = jnp.asarray(vertices)
        assert a.ndim == 1 and vertices.ndim == 2
        assert a.size == vertices.shape[0]
        assert vertices.shape[0] == vertices.shape[1] + 1
        return jnp.sum(a[:, None] * vertices, 0) / jnp.sum(a)
        # TODO rewrite as matmul
    
    @classmethod
    def baricentric_from_phi(cls, phi, vertices):
        phi = cls._process_phi(phi)
        mat = jnp.concatenate([vertices.T, jnp.ones((1,) + vertices.shape[:1])])
        rhs = jnp.concatenate([phi, jnp.ones(1)])
        return jnp.linalg.solve(mat, rhs)
        # TODO mat is integer, is there a specialized exact solve for integer
        # matrices?

p = 2
N = 10000

gen = np.random.default_rng(202207221232)
a = np.abs(gen.standard_normal((N, p + 1)))
vertices = AR.phi_vertices(p)
phi = jax.vmap(AR.phi_from_baricentric, (0, None))(a, vertices)
roots = jax.vmap(AR.inverse_roots_from_phi)(phi)

fig, ax = plt.subplots(num='convexphi', clear=True)

r = roots.reshape(-1)
ax.plot(r.real, r.imag, '.', alpha=.1)

theta = np.linspace(0, 2 * np.pi, 1000)
ax.plot(np.cos(theta), np.sin(theta), '--k')

ax.set_title(f'p = {p}')

fig.show()
