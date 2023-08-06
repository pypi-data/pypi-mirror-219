import gvar
import numpy as np

rng = np.random.default_rng(0)
n = 100
m = 101
a = rng.standard_normal((n + m, n + m))
cov = a.T @ a
c1 = cov[:n, :n]
c2 = cov[n:, n:]
c12 = cov[:n, n:]

x1 = gvar.gvar(np.zeros(n), c1, fast=True)
indices = np.arange(n)
rng.shuffle(indices)
x2 = gvar.gvar(np.zeros(m), c2, x1[indices], c12[indices], fast=True)
x = np.concatenate([x1, x2])

xcov = gvar.evalcov(x)
np.testing.assert_equal(xcov, cov)

y = gvar.gvar(np.zeros(n + m), cov, [], np.empty((0, n + m)), fast=True)
ycov = gvar.evalcov(y)
np.testing.assert_equal(ycov, cov)
