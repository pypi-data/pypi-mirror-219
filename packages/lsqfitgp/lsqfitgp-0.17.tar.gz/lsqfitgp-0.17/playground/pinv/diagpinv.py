from scipy import linalg
import numpy as np

def assert_close_matrices(actual, desired, *, rtol=0, atol=0):
    actual = np.asarray(actual)
    desired = np.asarray(desired)
    assert actual.shape == desired.shape
    if actual.size == 0:
        return
    actual = np.atleast_1d(actual)
    desired = np.atleast_1d(desired)
    
    dnorm = linalg.norm(desired, 2)
    adnorm = linalg.norm(actual - desired, 2)
    ratio = adnorm / dnorm if dnorm else np.nan
    msg = f"""\
matrices actual and desired are not close in 2-norm
norm(desired) = {dnorm:.2g}
norm(actual - desired) = {adnorm:.2g}  (atol = {atol:.2g})
ratio = {ratio:.2g}  (rtol = {rtol:.2g})"""
    assert adnorm <= atol + rtol * dnorm, msg

def eval_matrix_difference(expr1, expr2):
    actual = np.asarray(eval(expr1))
    desired = np.asarray(eval(expr2))
    assert actual.shape == desired.shape
    actual = np.atleast_1d(actual)
    desired = np.atleast_1d(desired)
    dnorm = linalg.norm(desired, 2)
    adnorm = linalg.norm(actual - desired, 2)
    ratio = adnorm / dnorm if dnorm else np.nan
    print(f'norm({expr1} - {expr2}) / norm({expr2}) = {ratio:.2g}')

def pinv_svd(a):
    u, s, vh = linalg.svd(a, full_matrices=False)
    eps = np.max(s) * np.finfo(s.dtype).eps * max(a.shape)
    si = np.where(s > eps, 1 / np.where(s, s, 1), 0)
    return (vh.T * si) @ u.T
    
def pinv_diag(a):
    n, m = a.shape
    transpose = n < m
    if transpose:
        a = a.T
    # a+ = (at a)+ at
    # at a = v w vt
    w, v = linalg.eigh(a.T @ a)
    eps = np.max(np.abs(w)) * np.finfo(w.dtype).eps * len(w)
    wi = np.where(w > eps, 1 / np.where(w, w, 1), 0)
    ai = np.linalg.multi_dot([v * wi, v.T, a.T])
    if transpose:
        ai = ai.T
    return ai

def pinv_chol(a, *, order=1, epsfac=1024):
    n, m = a.shape
    transpose = n < m
    if transpose:
        a = a.T
    
    # a+ = sum n=1^∞  (at a + eI)^-n e^(n-1) at
    # at a + eI = l lt
    
    aa = a.T @ a
    eps = np.max(np.sum(np.abs(aa), axis=0)) * np.finfo(aa.dtype).eps * len(aa)
    eps *= epsfac
    aa[np.diag_indices_from(aa)] += eps
    l = linalg.cholesky(aa, lower=True)
    
    term = a.T
    ai = 0
    for i in range(order):
        l_1term = linalg.solve_triangular(l, term, lower=True)
        term = linalg.solve_triangular(l.T, l_1term, lower=False)
        ai += eps ** i * term
    
    if transpose:
        ai = ai.T
    return ai

n = 1000
m = 100
gen = np.random.default_rng(202301301424)
a = gen.standard_normal((n, m))
a[:, :50] = a[:, :1]

ai = pinv_svd(a)
ai2 = pinv_diag(a)
ai3 = pinv_chol(a, order=2, epsfac=128000)

eval_matrix_difference('ai2', 'ai')
eval_matrix_difference('ai3', 'ai')
print()
eval_matrix_difference('a @ ai @ a', 'a')
eval_matrix_difference('a @ ai2 @ a', 'a')
eval_matrix_difference('a @ ai3 @ a', 'a')
print()
eval_matrix_difference('ai @ a @ ai', 'ai')
eval_matrix_difference('ai2 @ a @ ai2', 'ai2')
eval_matrix_difference('ai3 @ a @ ai3', 'ai3')
print()
eval_matrix_difference('a @ ai', '(a @ ai).T')
eval_matrix_difference('a @ ai2', '(a @ ai2).T')
eval_matrix_difference('a @ ai3', '(a @ ai3).T')
print()
eval_matrix_difference('ai @ a', '(ai @ a).T')
eval_matrix_difference('ai2 @ a', '(ai2 @ a).T')
eval_matrix_difference('ai3 @ a', '(ai3 @ a).T')
