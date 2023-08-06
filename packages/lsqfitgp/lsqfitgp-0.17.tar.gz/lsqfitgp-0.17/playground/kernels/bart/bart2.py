import functools

from jax import numpy as jnp
import jax
from jax import lax

@functools.partial(jax.jit, static_argnums=(5, 6))
def bart_correlation_maxd_recursive(nminus, n0, nplus, alpha, beta, maxd, d):
    
    p = len(nminus)

    if d >= maxd:
        return 1.
        
    elif d + 1 >= maxd:
        nout = nminus + nplus
        sump = jnp.sum(jnp.where(n0, nout / (nout + n0), 1))
    
    # TODO hardcode d + 2 case
    
    else:
        val = (0., nminus, n0, nplus)
        def loop(i, val):
            sump, nminus, n0, nplus = val
    
            nminusi = nminus[i]
            n0i = n0[i]
            nplusi = nplus[i]
            
            val = (0., nminus, n0, nplus, i, nminusi)
            def loop(k, val):
                sumn, nminus, n0, nplus, i, nminusi = val
                
                nminus = nminus.at[jnp.where(k < nminusi, i, i + p)].set(k)
                nplus = nplus.at[jnp.where(k >= nminusi, i, i + p)].set(k - nminusi)
                
                sumn += bart_correlation_maxd_recursive(nminus, n0, nplus, alpha, beta, maxd, d + 1)
                
                nminus = nminus.at[i].set(nminusi)
                nplus = nplus.at[i].set(nplusi)
                
                return sumn, nminus, n0, nplus, i, nminusi
            
            sumn, nminus, n0, nplus, _, _ = lax.fori_loop(0, nminusi + nplusi, loop, val)
    
            sump += jnp.where(n0i, sumn / (nminusi + n0i + nplusi), 1)
    
            return sump, nminus, n0, nplus

        sump, _, _, _ = lax.fori_loop(0, p, loop, val)

    pnt = alpha / (1 + d) ** beta
    return 1 - pnt * (1 - sump / p)

bart_correlation_maxd_vectorized = jax.vmap(bart_correlation_maxd_recursive, [
    0, 0, 0, None, None, None, None,
])
    
def bart_correlation_maxd(splitsbefore, splitsbetween, splitsafter, alpha, beta, maxd):
    """
    Compute the BART prior correlation between two points.
    
    The correlation is computed approximately by limiting the maximum depth
    of the trees. Limiting trees to depth 1 is equivalent to setting beta to
    infinity.
        
    Parameters
    ----------
    splitsbefore : int (..., p) array
        The number of splitting points less than the two points, separately
        along each coordinate.
    splitsbetween : int (..., p) array
        The number of splitting points between the two points, separately along
        each coordinate.
    splitsafter : int (..., p) array
        The number of splitting points greater than the two points, separately
        along each coordinate.
    alpha, beta : scalar
        The hyperparameters of the branching probability.
    maxd : int
        The maximum depth of the trees. The root has depth zero.
    
    Return
    ------
    corr : scalar
        The prior correlation.
    """
    args = [splitsbefore, splitsbetween, splitsafter]
    args = list(map(jnp.asarray, args))
    for a in args:
        assert a.ndim >= 1
    p = args[0].shape[-1]
    for a in args:
        assert a.shape[-1] == p
    args = jnp.broadcast_arrays(*args)
    shape = args[0].shape[:-1]
    args = [a.reshape(-1, p) for a in args]
    out = bart_correlation_maxd_vectorized(*args, alpha, beta, maxd, 0)
    return out.reshape(shape)
