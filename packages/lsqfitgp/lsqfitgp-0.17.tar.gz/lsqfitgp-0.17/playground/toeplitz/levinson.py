import jax
from jax import numpy as jnp
import numpy as np
from scipy import linalg

# adapted from SuperGauss/DurbinLevinson.h

def chol_solve(t, b):
    b = jnp.asarray(b)
    t = jnp.asarray(t)
    assert t.ndim == 1 and b.ndim == 2
    assert len(t) == len(b)

    ilb = jnp.zeros_like(b)
    n = len(t)
    phi1 = jnp.zeros(n)
    phi2 = jnp.zeros(n)
    
    nu = t[0]
    tlag = jnp.roll(t, -1)
    sqrt_nu = jnp.sqrt(nu)
    l0 = jnp.zeros(n).at[0].set(1 / sqrt_nu)
    
    ilb = ilb.at[0, :].set(l0 @ b)
    
    for i in range(1, n):
        
        # now:
        # phi1[i - 1:] == 0
        # phi2[i - 2:] == 0
        
        pi = i - 1
        rp = phi2 @ tlag
        phi1 = phi1.at[pi].set((tlag[pi] - rp) / nu)
        phi1 = phi1 - phi1[pi] * phi2
        
        # now:
        # phi1[i:] == 0
        # phi2[i - 1:] == 0

        nu = nu * (1 - phi1[pi]) * (1 + phi1[pi])
        
        phi2 = jnp.roll(phi1[::-1], i)

        # i-th row of L^-1
        li = -phi2.at[i].set(-1) / jnp.sqrt(nu)
        
        ilb = ilb.at[i, :].set(li @ b)

    return ilb

n = 10
m = 3
x = np.linspace(0, 3, n)
t = np.exp(-1/2 * (x - x[0]) ** 2)
b = np.random.randn(n, m)
a = linalg.toeplitz(t)
l = linalg.cholesky(a, lower=True)
ilb1 = chol_solve(t, b)
ilb2 = linalg.solve_triangular(l, b, lower=True)
np.testing.assert_allclose(ilb1, ilb2, rtol=1e-8)
