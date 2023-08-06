import numpy as np
import numba

default_bart_params = dict(m=200, alpha=0.95, beta=2, k=2, nu=3, q=0.9)

@numba.jit(nopython=True, cache=True, fastmath=True)
def bart_correlation_maxd_recursive(nminus, n0, nplus, d, alpha, beta, maxd):
    sump = 0.0
    p = len(nminus)
    for i in range(p):
        nminusi = nminus[i]
        n0i = n0[i]
        nplusi = nplus[i]
        
        if n0i == 0:
            sump += 1
        elif d >= maxd:
            sump += (nminusi + nplusi) / (nminusi + n0i + nplusi)
        else:
            sumn = 0
            for k in range(nminusi):
                nminus[i] = k
                sumn += bart_correlation_maxd_recursive(nminus, n0, nplus, d + 1, alpha, beta, maxd)
            nminus[i] = nminusi
            for k in range(nplusi):
                nplus[i] = k
                sumn += bart_correlation_maxd_recursive(nminus, n0, nplus, d + 1, alpha, beta, maxd)
            nplus[i] = nplusi
            sump += sumn / (nminusi + n0i + nplusi)
    
    pnt = alpha * (1 + d) ** -beta
    return 1 - pnt * (1 - sump / p)

@numba.guvectorize('(i8[:], i8[:], i8[:], f8, f8, i8, f8[:])', '(p),(p),(p),(),(),()->()', nopython=True)
def bart_correlation_maxd_vectorized(nminus, n0, nplus, alpha, beta, maxd, out):
    assert np.all(nminus >= 0)
    assert np.all(n0 >= 0)
    assert np.all(nplus >= 0)
    assert maxd >= 0
    if maxd == 0:
        out[0] = 1
    else:
        out[0] = bart_correlation_maxd_recursive(nminus, n0, nplus, 0, alpha, beta, maxd - 1)

def bart_correlation_maxd(splitsbefore, splitsbetween, splitsafter, alpha, beta, maxd):
    """
    Compute the BART prior correlation between two points.
    
    The correlation is computed approximately by limiting the maximum depth
    of the trees. Limiting trees to depth 1 is equivalent to setting beta to
    infinity.
    
    The function is fully vectorized.
    
    Parameters
    ----------
    splitsbefore : int (p,) array
        The number of splitting points less than the two points, separately
        along each coordinate.
    splitsbetween : int (p,) array
        The number of splitting points between the two points, separately along
        each coordinate.
    splitsafter : int (p,) array
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
    return bart_correlation_maxd_vectorized(splitsbefore, splitsbetween, splitsafter, alpha, beta, maxd)
