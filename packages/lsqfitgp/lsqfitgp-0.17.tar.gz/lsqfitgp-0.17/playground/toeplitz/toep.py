from lsqfitgp import _toeplitz
import numpy as np
from scipy import linalg

def rtol(x):
    return 1e-4 if x.dtype == np.float32 else 1e-8
    
def atol(x):
    return np.finfo(x.dtype).eps * np.max(x)

def maket(n):
    x = np.linspace(0, 3, n)
    t = np.pi * np.exp(-1/2 * x ** 2)
    dx = x[1] - x[0] if len(x) > 1 else np.empty(())
    difft = t[:-1] * np.expm1(-dx * (x[:-1] + dx / 2))
    np.testing.assert_allclose(np.diff(t), difft, rtol=rtol(t), atol=atol(x))
    return t, difft

def makeb(*shape):
    assert len(shape) <= 2
    n = shape[0]
    gen = np.random.default_rng(n + 202206041955)
    return gen.standard_normal(shape)

def catch(job):
    try:
        return job()
    except np.linalg.LinAlgError as exc:
        print(', '.join(exc.args))
        
def checkchol(t, b, lb, prefix):
    if l is None:
        pass
    elif not np.all(np.isfinite(l)):
        order, = np.nonzero(np.any(np.isnan(l), 0))
        order = order[0]
        print(f'{order + 1}-th minor is not positive definite')
    else:
        assert l.dtype == m.dtype, (l.dtype, m.dtype)
        ml = l @ l.T
        np.testing.assert_allclose(ml, m, rtol=rtol(ml))
        e = np.linalg.norm(ml - m, 2)
        print(f'error {prefix}: {e:.3g}')

def checkdiff(n, jit=False, eps=0, dtype='f4'):
    dtype = np.dtype(dtype)
    t, difft = maket(n, dtype)
    m = linalg.toeplitz(t)
    assert m.dtype == dtype
    cholesky = _toeplitz.cholesky_jit if jit else _toeplitz.cholesky
    l1 = catch(lambda: cholesky(t, diageps=eps))
    checkchol(l1, m, 'w/o diff')
    l2 = catch(lambda: cholesky(t, difft=difft, diageps=eps))
    checkchol(l2, m, 'w/ diff')

def checkchol2(t, b, ub, prefix):
    if ub is None:
        pass
    elif not np.all(np.isfinite(ub)):
        ub = ub.reshape(ub.shape[0], -1)
        order, = np.nonzero(np.any(np.isnan(ub), 1))
        order = order[0]
        print(f'{order + 1}-th minor is not positive definite')
    else:
        qref = b.T @ linalg.matmul_toeplitz(t, b)
        q = ub.T @ ub
        erel = (q - qref) / qref
        print(f'relative error on quadratic form {prefix}: {erel:.2g}')

def checkdiff2(n, jit=True, eps=0, dtype='f4'):
    t, difft = maket(n)
    b = makeb(n)
    cholesky = _toeplitz.cholesky_jit if jit else _toeplitz.cholesky
    ub1 = catch(lambda: cholesky(t.astype(dtype), b.astype(dtype), diageps=eps, lower=False))
    checkchol2(t, b, ub1, 'w/o diff')
    ub2 = catch(lambda: cholesky(t.astype(dtype), b.astype(dtype), difft=difft.astype(dtype), diageps=eps, lower=False))
    checkchol2(t, b, ub2, 'w/ diff')
